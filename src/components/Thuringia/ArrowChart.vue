<script setup>
import { ref, onMounted, watch } from 'vue';
import { useArrowChart } from '@src/composables/Thuringia/useArrowChart.js';
import { isMobile, scaleRange } from '@src/composables/utils.js';

const props = defineProps({
    stats: {
        type: Object,
        required: true
    },
    currentRange: {
        type: Number,
        default: 0
    }
});

const svgRef = ref(null);
const chartContainer = ref(null);

const { drawArrow } = useArrowChart();

onMounted(async () => {
    if (svgRef.value) {
        drawArrow(svgRef.value, props.stats, props.currentRange);
    }
});

watch(() => props.currentRange, async () => {
    if (svgRef.value) {
        drawArrow(svgRef.value, props.stats, props.currentRange);
    }
});

watch(() => props.stats, async () => {
    if (svgRef.value) {
        drawArrow(svgRef.value, props.stats, props.currentRange);
    }
});
</script>

<template>
    <div ref="chartContainer" class="arrow-chart"
        :style="`transform: ${isMobile() ? `scaleY(${scaleRange(props.currentRange)}) rotate(90deg)` : `scaleX(${scaleRange(props.currentRange)})`}; transform-origin: ${isMobile() ? 'top right' : 'right center'};`">
        <svg ref="svgRef"></svg>
    </div>
</template>

<style scoped>
.arrow-chart {
    height: 100%;
    width: 100%;
    position: relative;
    transition: transform 0.8s ease-in-out;
}

.arrow-chart svg {
    width: 100%;
    height: 15%;
    position: absolute;
    bottom: 0;
}

@media (max-width: 768px) {
    .arrow-chart {
        top: 70%;
        left: 30%;
    }
}
</style>
