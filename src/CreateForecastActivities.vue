<template>
  <v-dialog v-model="show" max-width="600" @click:outside="close">
    <v-card>
      <v-card-title class="d-flex align-center">
        <v-icon class="mr-2">mdi-calendar-plus</v-icon>
        Create Forecast Activities
      </v-card-title>
      <v-card-text>
        <p class="text-body-2 text-medium-emphasis mb-4">
          Create "Reserve" activities on a Calendar timeline for each day in the 3-day forecast
          that has notable space weather activity.
        </p>
        <v-select
          v-model="selectedTimeline"
          :items="timelines"
          item-title="name"
          item-value="name"
          label="Timeline"
          :loading="loadingTimelines"
          :error-messages="timelineError"
          variant="outlined"
          density="compact"
          class="mb-3"
        />
        <div class="text-subtitle-2 mb-2">Forecast Activities to Create</div>
        <v-table density="compact">
          <thead>
            <tr>
              <th class="checkbox-col">
                <v-checkbox-input
                  v-model="allSelected"
                  @update:model-value="toggleAll"
                  hide-details
                  density="compact"
                />
              </th>
              <th class="date-col">Date</th>
              <th>Summary</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in activities" :key="index">
              <td class="checkbox-col">
                <v-checkbox
                  :model-value="selected[index]"
                  @update:model-value="selected[index] = $event"
                  hide-details
                  density="compact"
                />
              </td>
              <td class="text-body-2 date-col">{{ item.date }}</td>
              <td class="text-caption">{{ item.summary }}</td>
            </tr>
          </tbody>
        </v-table>
      </v-card-text>
      <v-alert
        v-if="successMessage"
        type="success"
        variant="tonal"
        density="compact"
        class="mx-4 mb-2"
      >
        {{ successMessage }}
      </v-alert>
      <v-card-actions class="px-4 pb-4">
        <v-spacer />
        <v-btn v-if="successMessage" variant="text" @click="close">Close</v-btn>
        <template v-else>
          <v-btn variant="text" @click="close">Cancel</v-btn>
          <v-btn
            color="primary"
            variant="flat"
            :loading="creating"
            :disabled="!selectedTimeline || !hasSelected"
            @click="createActivities"
          >
            Create {{ selectedCount }} Activities
          </v-btn>
        </template>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { Api } from '@openc3/js-common/services'

export default {
  props: {
    modelValue: { type: Boolean, default: false },
    forecast: { type: Array, required: true },
    scales: { type: Object, required: true },
  },
  emits: ['update:modelValue', 'created'],
  data() {
    return {
      timelines: [],
      selectedTimeline: null,
      loadingTimelines: false,
      timelineError: '',
      creating: false,
      selected: [],
      allSelected: true,
      successMessage: '',
    }
  },
  computed: {
    show: {
      get() { return this.modelValue },
      set(val) { this.$emit('update:modelValue', val) },
    },
    activities() {
      return this.forecast.map((day) => {
        const parts = []
        const g = day.gScale || '0'
        if (day.rMinor && parseInt(day.rMinor) > 0) {
          parts.push(`Radio: ${day.rMinor}% minor / ${day.rMajor}% major`)
        }
        if (day.sProb && parseInt(day.sProb) > 0) {
          parts.push(`Radiation: ${day.sProb}%`)
        }
        if (day.gScale && parseInt(day.gScale) > 0) {
          parts.push(`Geomagnetic: G${day.gScale} ${day.gText}`)
        }
        return {
          date: day.date,
          title: `R${this.scales.r.scale || 0} | S${this.scales.s.scale || 0} | G${g}`,
          summary: parts.length > 0 ? parts.join('\n') : 'No notable activity',
          hasActivity: parts.length > 0,
        }
      })
    },
    hasSelected() {
      return this.selected.some(Boolean)
    },
    selectedCount() {
      return this.selected.filter(Boolean).length
    },
  },
  watch: {
    modelValue(val) {
      if (val) {
        this.successMessage = ''
        this.timelineError = ''
        this.selected = this.activities.map((a) => a.hasActivity)
        this.allSelected = this.selected.every(Boolean)
        this.loadTimelines()
      }
    },
  },
  methods: {
    close() {
      this.show = false
    },
    toggleAll(val) {
      this.selected = this.selected.map(() => val)
    },
    async loadTimelines() {
      this.loadingTimelines = true
      this.timelineError = ''
      try {
        const { data } = await Api.get('/openc3-api/timeline')
        this.timelines = data
        if (data.length === 1) {
          this.selectedTimeline = data[0].name
        }
      } catch (e) {
        this.timelineError = 'Failed to load timelines'
      } finally {
        this.loadingTimelines = false
      }
    },
    async createActivities() {
      this.creating = true
      this.timelineError = ''
      try {
        const selected = this.activities.filter((_, i) => this.selected[i])
        const now = new Date()
        for (const activity of selected) {
          const dayStart = new Date(`${activity.date}T00:00:00Z`)
          const start = dayStart > now ? dayStart : new Date(now.getTime() + 60000)
          await Api.post(
            `/openc3-api/timeline/${this.selectedTimeline}/activities`,
            {
              data: {
                start: start.toISOString(),
                stop: `${activity.date}T23:59:59+00:00`,
                kind: 'reserve',
                data: {
                  customTitle: activity.title,
                  notes: `Space Weather Forecast:\n${activity.summary}`,
                },
              },
            },
          )
        }
        this.successMessage = `Successfully created ${selected.length} activit${selected.length === 1 ? 'y' : 'ies'} on "${this.selectedTimeline}"`
        this.$emit('created')
      } catch (e) {
        this.timelineError = e?.response?.data?.message || 'Failed to create activities'
      } finally {
        this.creating = false
      }
    },
  },
}
</script>

<style scoped>
.checkbox-col {
  width: 48px;
}
.date-col {
  width: 140px;
}
</style>
