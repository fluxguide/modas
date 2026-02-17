<script setup>
import { useTextStats } from '@composables/Thuringia/useTextStats.js';
import { computed } from 'vue';
import { scaleRange, isMobile } from '@src/composables/utils.js';

const props = defineProps({
  stats: Object,
  statsPercentages: Object,
  currentRange: Number
});

const {
  headerData,
  showHeaderRange
} = useTextStats(computed(() => props.stats), computed(() => props.statsPercentages), computed(() => props.currentRange));

defineExpose({
  showHeaderRange
});
</script>

<template>
  <div class="headerRange">
    <div v-for="(header, index) in headerData" :key="index" :id="`headerRange${index}`" class="header-item"
      :style="`width: ${isMobile() ? 52 : 85 * scaleRange(props.currentRange)}%`">
      <h2>Im Umkreis von {{ header.distance }} haben <br /><span>{{ header.stops }}%</span> der Rathäuser
        <span>mindestens
          eine Haltestelle</span>, <br /><span>{{ header.noStops }}%</span> haben <span>keine Haltestelle</span>.
      </h2>
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
}

.headerRange h2 {
  line-height: 1.6;
  font-weight: 400;
  text-align: left;
  padding: 10px 0px;
}

.headerRange h2 span {
  font-weight: 700;
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
