<script setup>
import { toRef } from 'vue';
import { useTextStats } from '@composables/Thuringia/useTextStats.js';
import { computed } from 'vue';
import { scaleRange, isMobile } from '@src/composables/utils.js';
import { useColumnLabels } from '@composables/useColumnLabels.js';
import EditableTextField from '@src/components/EditableTextField.vue';

const props = defineProps({
  stats: Object,
  statsPercentages: Object,
  currentRange: Number,
  activeMode: String,
  columnLabelMap: { type: Object, default: () => ({}) },
});

const { col } = useColumnLabels(toRef(props, "columnLabelMap"))

const rangeKeyByRangeIndex = {
  0: "stops_within_100m",
  1: "stops_within_200m",
  2: "stops_within_300m",
};


const {
  headerData,
  showHeaderRange
} = useTextStats(computed(() => props.stats), computed(() => props.statsPercentages), computed(() => props.currentRange));

const getHeaderString = (header) => {
  const key = rangeKeyByRangeIndex[props.currentRange] || "stops_within_300m";
  const colName = col(key, `${header.distance}m`);

  return `Im Umkreis von [${colName}] haben ${header.stops}% der Rathäuser mindestens eine Haltestelle, ${header.noStops}% haben keine Haltestelle.`
}

defineExpose({
  showHeaderRange
});
</script>

<template>
  <div class="headerRange">
    <div v-for="(header, index) in headerData" :key="index" v-show="currentRange === index" class="header-item"
      :style="`width: ${isMobile() ? 52 : 85 * scaleRange(props.currentRange)}%`">
      <EditableTextField :model-value="getHeaderString(header)" :active-mode="activeMode" :rows="3" :width="`100%`"
        :font-size="`24px`" :line-height="1.6" :top-bottom-padding="`0`" />
    </div>
  </div>
</template>

<style scoped>
.headerRange {
  width: 100%;
  height: 100%;
}

.header-item {
  height: fit-content;
  position: absolute;
  top: 30%;
  right: 10%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  transition: width 0.7s ease-in-out;
  padding: 5px 20px 15px 20px;
  pointer-events: none;
}

.header-item.visible {
  pointer-events: auto;
}

@media (max-width: 768px) {
  .header-item {
    width: 100%;
    height: fit-content;
    position: fixed;
    top: 7%;
    right: 2%;
    border-radius: 15px;
  }

  .headerRange h2 {
    font-size: 10px;
    text-align: left;
    padding: 5px 12px;
  }
}

@media (min-width: 2560px) {
  .header-item {
    border-radius: 20px;
  }

  .headerRange h2 {
    font-size: 28px;
  }
}

@media (min-width: 3440px) {
  .header-item {
    border-radius: 25px;
  }

  .headerRange h2 {
    font-size: 36px;
  }
}
</style>
