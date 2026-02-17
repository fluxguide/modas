<script setup>
import { useTextStats } from '@composables/Thuringia/useTextStats.js';
import { computed } from 'vue';
import { colors } from '@src/composables/Thuringia/useArrowChart.js';

const props = defineProps({
  stats: Object,
  currentRange: Number
});

const { showTextRange, hideAllTextRanges } = useTextStats(
  computed(() => props.stats),
  computed(() => props.currentRange)
);

const rangeDescriptions = [
  { id: 0, description: 'innerhalb von 100 Metern' },
  { id: 1, description: 'zwischen 101 und 200 Metern Distanz' },
  { id: 2, description: 'zwischen 201 und 300 Metern Distanz' }
];

const stopTypes = [
  { id: 'noStops', text: 'gar keine Haltestelle', color: colors[0] },
  { id: 'oneStop', text: 'eine Haltestelle', color: colors[1] },
  { id: 'twoStops', text: 'zwei Haltestellen', color: colors[2] },
  { id: 'moreThanTwoStops', text: 'mehr als zwei Haltestellen', color: colors[3] }
];

// Expose functions to parent component
defineExpose({
  showTextRange,
  hideAllTextRanges
});
</script>

<template>
  <div class="text-ranges">
    <div v-for="range in rangeDescriptions" class="textRange" :id="`textRange${range.id}`"
      :style="range.id !== 0 ? 'display: none;' : ''">
      <p v-for="stopType in stopTypes" :key="stopType.id">
        Rathäuser haben <span :style="{ backgroundColor: stopType.color }">{{ stopType.text }}</span> {{
          range.description }}.
      </p>
    </div>
  </div>
</template>

<style scoped>
.text-ranges {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.textRange {
  transition: opacity 0.8s ease-in-out, visibility 0.8s ease-in-out;
  opacity: 0;
  padding: 10px 0;
  text-align: left;
}

.textRange.visible {
  opacity: 1;
  visibility: visible;
}

.textRange p {
  text-align: left;
  font-size: 18px;
}

.textRange p span {
  padding: 2px 6px;
  border-radius: 4px;
  color: white;
  font-weight: 500;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

@media (max-width: 768px) {
  .text-ranges {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: flex-start;
  }

  .textRange {
    padding: 0;
  }

  .textRange p {
    font-size: 12px;
    margin: 15% 5% 10% 8%;
    line-height: 2;
  }
}

@media (min-width: 2560px) {
  .textRange p {
    font-size: 21px;
  }
}

@media (min-width: 3440px) {
  .textRange p {
    font-size: 30px;
  }
}
</style>
