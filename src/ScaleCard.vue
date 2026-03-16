<template>
  <v-card :color="color" variant="tonal" class="text-center pa-3 position-relative h-100">
    <div class="text-h4 font-weight-bold">
      {{ scale.key }}{{ scale.value }}
    </div>
    <div class="text-caption font-weight-medium text-uppercase mt-1">
      {{ scale.text || 'None' }}
    </div>
    <div class="text-caption text-medium-emphasis mt-1">
      {{ scale.label }}
    </div>
    <div v-if="scale.impact" class="text-caption font-italic mt-1">
      {{ scale.impact }}
    </div>
    <v-tooltip location="top" max-width="300">
      <template #activator="{ props }">
        <v-icon
          v-bind="props"
          size="x-small"
          class="position-absolute info-icon"
        >
          mdi-information-outline
        </v-icon>
      </template>
      <div class="text-body-2">
        <div class="font-weight-bold mb-1">{{ scale.label }} ({{ scale.key }}0&ndash;{{ scale.key }}5)</div>
        <div>{{ scale.description }}</div>
        <div class="mt-1 font-weight-medium">Scale:</div>
        <div>0 = None</div>
        <div>1 = Minor</div>
        <div>2 = Moderate</div>
        <div>3 = Strong</div>
        <div>4 = Severe</div>
        <div>5 = Extreme</div>
      </div>
    </v-tooltip>
  </v-card>
</template>

<script>
import { scaleColor } from './scaleColor'

export default {
  props: {
    scale: { type: Object, required: true },
  },
  computed: {
    color() {
      return scaleColor(this.scale.value)
    },
  },
}
</script>

<style scoped>
.info-icon {
  bottom: 8px;
  right: 8px;
}
</style>
