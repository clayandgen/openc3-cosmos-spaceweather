<template>
  <div>
    <div class="text-subtitle-2 text-medium-emphasis mb-2">3-Day Forecast</div>
    <v-table density="default" class="mb-4">
      <thead>
        <tr>
          <th>Date</th>
          <th class="text-center">
            R (Radio)
            <v-tooltip location="top" max-width="280">
              <template #activator="{ props }">
                <v-icon v-bind="props" size="small" class="ml-1">mdi-information-outline</v-icon>
              </template>
              <div class="text-body-2">
                <div class="font-weight-bold">Minor / Major probability</div>
                <div>Chance of an R1-R2 (minor) or R3+ (major) radio blackout occurring that day.</div>
              </div>
            </v-tooltip>
          </th>
          <th class="text-center">
            S (Radiation)
            <v-tooltip location="top" max-width="280">
              <template #activator="{ props }">
                <v-icon v-bind="props" size="small" class="ml-1">mdi-information-outline</v-icon>
              </template>
              <div class="text-body-2">
                <div class="font-weight-bold">Storm probability</div>
                <div>Chance of an S1+ solar radiation storm occurring that day, posing risk to satellites and astronauts.</div>
              </div>
            </v-tooltip>
          </th>
          <th class="text-center">
            G (Geomagnetic)
            <v-tooltip location="top" max-width="280">
              <template #activator="{ props }">
                <v-icon v-bind="props" size="small" class="ml-1">mdi-information-outline</v-icon>
              </template>
              <div class="text-body-2">
                <div class="font-weight-bold">Predicted storm level</div>
                <div>Expected geomagnetic storm intensity (G0-G5). Affects power grids, GPS, and aurora visibility.</div>
              </div>
            </v-tooltip>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="day in forecast" :key="day.date">
          <td class="text-body-2">{{ day.date }}</td>
          <td class="text-center">
            <v-tooltip v-if="day.gScale !== null" location="top">
              <template #activator="{ props }">
                <v-chip
                  v-bind="props"
                  size="small"
                  label
                  :color="scaleColor(day.rMinor > 25 ? '1' : '0')"
                  class="mr-1"
                >
                  {{ day.rMinor }}% / {{ day.rMajor }}%
                </v-chip>
              </template>
              {{ day.rMinor }}% chance of minor (R1-R2), {{ day.rMajor }}% chance of major (R3+) radio blackout
            </v-tooltip>
            <span v-else class="text-caption text-medium-emphasis">--</span>
          </td>
          <td class="text-center">
            <v-tooltip v-if="day.sProb !== null" location="top">
              <template #activator="{ props }">
                <v-chip
                  v-bind="props"
                  size="small"
                  label
                  :color="scaleColor(day.sProb > 25 ? '1' : '0')"
                >
                  {{ day.sProb }}%
                </v-chip>
              </template>
              {{ day.sProb }}% chance of a solar radiation storm (S1+)
            </v-tooltip>
            <span v-else class="text-caption text-medium-emphasis">--</span>
          </td>
          <td class="text-center">
            <v-tooltip location="top">
              <template #activator="{ props }">
                <v-chip
                  v-bind="props"
                  size="small"
                  label
                  :color="scaleColor(day.gScale)"
                >
                  G{{ day.gScale }} {{ day.gText }}
                </v-chip>
              </template>
              Predicted G{{ day.gScale }} ({{ day.gText || 'none' }}) geomagnetic storm
            </v-tooltip>
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<script>
import { scaleColor } from './scaleColor'

export default {
  props: {
    forecast: { type: Array, required: true },
  },
  methods: {
    scaleColor,
  },
}
</script>
