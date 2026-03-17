<template>
  <v-container class="pa-3 spaceweather-container">
    <!-- Header -->
    <div class="d-flex justify-space-between align-center pb-2 mb-3 header-divider">
      <div>
        <span class="text-h6 font-weight-bold">Space Weather Dashboard</span>
        <div v-if="lastRefreshedDisplay" class="text-caption text-medium-emphasis">
          Last refreshed: {{ lastRefreshedDisplay }}
        </div>
      </div>
      <div class="d-flex align-center ga-3">
        <v-btn
          size="small"
          variant="outlined"
          :loading="refreshing"
          @click="refresh"
        >
          Refresh Now
        </v-btn>
        <a
          class="text-caption text-blue-lighten-2 text-decoration-none"
          href="https://www.swpc.noaa.gov"
          target="_blank"
          rel="noopener noreferrer"
        >
          NOAA SWPC &rarr;
        </a>
      </div>
    </div>

    <div v-if="!scalesLoaded" class="text-center py-8 text-medium-emphasis font-italic">
      No telemetry values found, click "Refresh Now" or send the GET_ALERTS / GET_SCALES commands to receive latest Space Weather data
    </div>

    <template v-else>
      <!-- Current Conditions -->
      <div class="text-subtitle-2 text-medium-emphasis mb-2">
        Current Conditions
        <span v-if="currentConditionsTime" class="text-caption ml-2">
          ({{ currentConditionsTime }})
        </span>
      </div>
      <v-row dense class="mb-4">
        <v-col v-for="scale in currentScales" :key="scale.key" cols="4">
          <scale-card :scale="scale" />
        </v-col>
      </v-row>

      <!-- 3-Day Forecast -->
      <forecast-table :forecast="forecast" />

      <!-- Add to Calendar (Enterprise only) -->
      <template v-if="enterprise">
        <div class="d-flex justify-end mb-3">
          <v-btn
            size="small"
            variant="tonal"
            prepend-icon="mdi-calendar-plus"
            @click="showCreateActivities = true"
          >
            Add Forecast to Calendar
          </v-btn>
        </div>
        <create-forecast-activities
          v-model="showCreateActivities"
          :forecast="forecast"
          :scales="scales"
        />
      </template>

      <!-- Latest Alert -->
      <latest-alert
        :alert="alert"
        :formatted-time="formatUserTime(alert.dateTime)"
      />
    </template>
  </v-container>
</template>

<script>
import { Widget } from '@openc3/vue-common/widgets'
import { TimeFilters } from '@openc3/vue-common/util'
import { Api, OpenC3Api } from '@openc3/js-common/services'
import ScaleCard from './ScaleCard'
import ForecastTable from './ForecastTable'
import LatestAlert from './LatestAlert'
import CreateForecastActivities from './CreateForecastActivities'

const SCALE_IMPACTS = {
  R: [
    '',
    'Minor HF radio fade on sunlit side',
    'Limited HF radio blackout, GPS scintillation',
    'Wide-area HF radio blackout for ~1 hr',
    'HF radio blackout for 1-2 hrs, GPS issues',
    'Complete HF radio blackout for hours',
  ],
  S: [
    '',
    'Minor impacts on HF radio in polar regions',
    'Infrequent single-event upsets in satellites',
    'Elevated radiation risk for astronauts',
    'Blackout of HF radio, increased radiation risk',
    'Unavoidable high radiation hazard to astronauts',
  ],
  G: [
    '',
    'Weak power grid fluctuations, aurora at high latitudes',
    'High-latitude power systems may need correction, aurora to ~55 deg',
    'Intermittent GPS and HF radio issues, aurora to ~50 deg',
    'Widespread voltage control problems, GPS degraded for hours',
    'Grid collapse possible, GPS unusable, aurora to ~40 deg',
  ],
}

const SCALE_LABELS = { R: 'Radio Blackout', S: 'Solar Radiation', G: 'Geomagnetic Storm' }

const SCALE_DESCRIPTIONS = {
  R: 'Measures disruption to high-frequency (HF) radio communication and GPS signals caused by solar X-ray flares. Affects aviation, maritime, and emergency communications.',
  S: 'Measures energetic particle bombardment from solar events. Poses radiation risk to astronauts and airline passengers on polar routes, and can cause satellite electronics damage.',
  G: "Measures disturbances in Earth's magnetic field caused by solar wind. Can affect power grids, satellite operations, GPS accuracy, and determines how far south the aurora is visible.",
}

export default {
  components: { ScaleCard, ForecastTable, LatestAlert, CreateForecastActivities },
  mixins: [Widget, TimeFilters],
  data() {
    return {
      scales: {
        currentDate: null,
        currentTime: null,
        r: { scale: null, text: null },
        s: { scale: null, text: null },
        g: { scale: null, text: null },
        today: { rMinor: null, rMajor: null, sProb: null, gScale: null, gText: null },
        tomorrow: { date: null, rMinor: null, rMajor: null, sProb: null, gScale: null, gText: null },
        day3: { date: null, rMinor: null, rMajor: null, sProb: null, gScale: null, gText: null },
      },
      alert: { productId: null, dateTime: null, message: null },
      enterprise: false,
      showCreateActivities: false,
      refreshing: false,
      api: null,
      target: 'SPACEWEATHER',
      updater: null,
      lastRefreshed: null,
    }
  },
  computed: {
    scalesLoaded() {
      return this.scales.r.scale !== null
    },
    currentScales() {
      return ['R', 'S', 'G'].map((key) => {
        const data = this.scales[key.toLowerCase()]
        return {
          key,
          value: data.scale,
          text: data.text,
          label: SCALE_LABELS[key],
          description: SCALE_DESCRIPTIONS[key],
          impact: SCALE_IMPACTS[key][parseInt(data.scale) || 0],
        }
      })
    },
    forecast() {
      return [
        { date: this.scales.currentDate || 'Today', ...this.scales.today },
        { date: this.scales.tomorrow.date || 'Tomorrow', ...this.scales.tomorrow },
        { date: this.scales.day3.date || 'Day 3', ...this.scales.day3 },
      ]
    },
    currentConditionsTime() {
      if (!this.scales.currentDate || !this.scales.currentTime) return ''
      const d = new Date(`${this.scales.currentDate}T${this.scales.currentTime}Z`)
      if (isNaN(d.getTime())) return `${this.scales.currentDate} ${this.scales.currentTime} UTC`
      return this.formatDateTimeHMS(d, this.screenTimeZone)
    },
    lastRefreshedDisplay() {
      if (!this.lastRefreshed) return ''
      return this.formatDateTimeHMS(this.lastRefreshed, this.screenTimeZone)
    },
  },
  created() {
    this.api = new OpenC3Api()
    this.target = this.parameters[0] || 'SPACEWEATHER'
    Api.get('/openc3-api/info').then(({ data }) => {
      this.enterprise = data.enterprise
    }).catch(() => {})
    this.update()
    this.updater = setInterval(() => this.update(), 3600000)
  },
  unmounted() {
    if (this.updater) {
      clearInterval(this.updater)
      this.updater = null
    }
  },
  methods: {
    async update() {
      await Promise.all([
        this.api
          .get_tlm_packet(this.target, 'SCALES_RESPONSE', 'CONVERTED')
          .then((data) => {
            if (!data) return
            const pkt = Object.fromEntries(data)
            this.scales.currentDate = pkt.CURRENT_DATESTAMP
            this.scales.currentTime = pkt.CURRENT_TIMESTAMP
            this.scales.r = { scale: pkt.R_SCALE, text: pkt.R_TEXT }
            this.scales.s = { scale: pkt.S_SCALE, text: pkt.S_TEXT }
            this.scales.g = { scale: pkt.G_SCALE, text: pkt.G_TEXT }
            this.scales.today = {
              rMinor: pkt.TODAY_R_MINOR_PROB,
              rMajor: pkt.TODAY_R_MAJOR_PROB,
              sProb: pkt.TODAY_S_PROB,
              gScale: pkt.TODAY_G_SCALE,
              gText: pkt.TODAY_G_TEXT,
            }
            this.scales.tomorrow = {
              date: pkt.TOMORROW_DATE,
              rMinor: pkt.TOMORROW_R_MINOR_PROB,
              rMajor: pkt.TOMORROW_R_MAJOR_PROB,
              sProb: pkt.TOMORROW_S_PROB,
              gScale: pkt.TOMORROW_G_SCALE,
              gText: pkt.TOMORROW_G_TEXT,
            }
            this.scales.day3 = {
              date: pkt.DAY3_DATE,
              rMinor: pkt.DAY3_R_MINOR_PROB,
              rMajor: pkt.DAY3_R_MAJOR_PROB,
              sProb: pkt.DAY3_S_PROB,
              gScale: pkt.DAY3_G_SCALE,
              gText: pkt.DAY3_G_TEXT,
            }
            if (pkt.RECEIVED_TIMESECONDS) {
              this.lastRefreshed = new Date(pkt.RECEIVED_TIMESECONDS * 1000)
            }
          })
          .catch(() => {}),
        this.api
          .get_tlm_packet(this.target, 'ALERTS_RESPONSE', 'CONVERTED')
          .then((data) => {
            if (!data) return
            const pkt = Object.fromEntries(data)
            this.alert = {
              productId: pkt.PRODUCT_ID,
              dateTime: pkt.ISSUE_DATETIME,
              message: pkt.MESSAGE,
            }
          })
          .catch(() => {}),
      ])
    },
    formatUserTime(dateStr) {
      if (!dateStr) return ''
      const d = new Date(dateStr.replace(' ', 'T') + 'Z')
      if (isNaN(d.getTime())) return dateStr
      return this.formatDateTimeHMS(d, this.screenTimeZone)
    },
    async refresh() {
      this.refreshing = true
      try {
        await Promise.all([
          this.api.cmd(this.target, 'GET_SCALES', {}),
          this.api.cmd(this.target, 'GET_ALERTS', {}),
        ])
        await new Promise((resolve) => setTimeout(resolve, 1000))
        await this.update()
      } finally {
        this.refreshing = false
      }
    },
  },
}
</script>

<style scoped>
.spaceweather-container {
  width: 800px;
  min-width: 800px;
  max-width: 800px;
}
.header-divider {
  border-bottom: 2px solid rgba(255, 255, 255, 0.12);
}
</style>
