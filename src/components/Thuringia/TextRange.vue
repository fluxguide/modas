<script setup>
import { useTextStats } from '@composables/Thuringia/useTextStats.js';
import { computed } from 'vue';
import { defaultCategoryColours } from '@src/composables/utils.js';
import EditableTextField from '@src/components/EditableTextField.vue';

const props = defineProps({
  stats: Object,
  currentRange: Number,
  activeMode: String,
});

const { showTextRange, hideAllTextRanges } = useTextStats(
  computed(() => props.stats),
  computed(() => props.currentRange)
);

const rangeLabelByIndex = ['0-100 Meter', '101-200 Meter', '201-300 Meter'];

const getTextString = (stopType) => {
  const rangeLabel = rangeLabelByIndex[props.currentRange] ?? rangeLabelByIndex[rangeLabelByIndex.length - 1];

  return `Rathäuser haben ${stopType.text} im Umkreis von ${rangeLabel}.`;
}

const stopTypes = [
  { id: 'noStops', text: 'gar keine Haltestelle', color: defaultCategoryColours[0], countKey: 'townhallsWithNoStops' },
  { id: 'oneStop', text: 'eine Haltestelle', color: defaultCategoryColours[1], countKey: 'townhallsWithOneStop' },
  { id: 'twoStops', text: 'zwei Haltestellen', color: defaultCategoryColours[2], countKey: 'townhallsWithTwoStops' },
  { id: 'moreThanTwoStops', text: 'mehr als zwei Haltestellen', color: defaultCategoryColours[3], countKey: 'townhallsWithMoreThanTwoStops' }
];

const statsRangeKeyByIndex = ['range0_100', 'range101_200', 'range201_300'];

const getStopValue = (stopType) => {
  const rangeKey = statsRangeKeyByIndex[props.currentRange] ?? statsRangeKeyByIndex[statsRangeKeyByIndex.length - 1];
  return props.stats?.[rangeKey]?.[stopType.countKey] ?? 0;
}

// Expose functions to parent component
defineExpose({
  showTextRange,
  hideAllTextRanges
});
</script>

<template>
  <div class="text-ranges">
    <div :id="`textRange${currentRange}`" class="textRange">
      <div v-for="stopType in stopTypes" :key="stopType.id" class="text-range-row">
        <span class="text-range-row__value" :style="{ backgroundColor: stopType.color }">
          {{ getStopValue(stopType) }}
        </span>
        <EditableTextField :model-value="getTextString(stopType)" :active-mode="activeMode" :rows="1"
          :width="activeMode === 'edit' ? '70vw' : `${getTextString(stopType).length + 2}ch`" font-size="18px"
          :line-height="1.3" :padding="`0px`" :text-align="activeMode === 'edit' ? 'center' : 'left'" />
      </div>
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

.text-range-row {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 12px;
  margin: 8px 0;
}

span {
  padding: 18px 0;
}

.text-range-row__value {
  flex-shrink: 0;
  min-width: 64px;
  max-width: 128px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  color: #fff;
  text-shadow: rgb(0, 0, 0) 0.8px 0.8px 1px;
  font-size: 18px;
  font-weight: 700;
}
</style>
