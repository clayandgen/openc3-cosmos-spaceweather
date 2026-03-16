<template>
  <v-expansion-panels v-if="alert.productId" variant="accordion" flat>
    <v-expansion-panel>
      <v-expansion-panel-title class="px-3 py-2">
        <div class="d-flex align-center ga-2">
          <v-chip
            size="small"
            label
            :color="badgeColor"
            class="font-weight-bold text-uppercase"
          >
            {{ alert.productId }}
          </v-chip>
          <span class="text-body-2">Latest Alert</span>
          <span class="text-caption text-medium-emphasis">
            {{ formattedTime }}
          </span>
        </div>
      </v-expansion-panel-title>
      <v-expansion-panel-text>
        <v-divider class="mb-3" />
        <pre class="text-body-2 alert-message">{{ formattedMessage }}</pre>
      </v-expansion-panel-text>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script>
export default {
  props: {
    alert: { type: Object, required: true },
    formattedTime: { type: String, default: '' },
  },
  computed: {
    badgeColor() {
      const id = (this.alert.productId || '').toUpperCase()
      if (id.startsWith('EF') || id.includes('WAR')) return 'deep-orange'
      if (id.startsWith('K0') && id.endsWith('W')) return 'yellow-darken-2'
      if (id.startsWith('K0') && id.endsWith('A')) return 'red-darken-3'
      if (id.startsWith('A') || id.startsWith('TI')) return 'blue-darken-2'
      if (id.startsWith('BHI') || id.startsWith('SUM')) return 'green-darken-2'
      return undefined
    },
    formattedMessage() {
      if (!this.alert.message) return ''
      return this.alert.message.replace(/\r\n/g, '\n').trim()
    },
  },
}
</script>

<style scoped>
.alert-message {
  white-space: pre-wrap;
  word-wrap: break-word;
  max-height: 200px;
  overflow-y: auto;
  opacity: 0.85;
  font-family: 'Roboto Mono', monospace;
}
</style>
