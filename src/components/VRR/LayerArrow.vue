<script setup>
import { computed } from 'vue';
import { isMobile } from '@src/composables/utils.js';

const props = defineProps({
    startYear: {
        type: Number,
        default: 2022
    },
    endYear: {
        type: Number,
        default: 2024
    },
    dataPoints: {
        type: Array,
        default: () => []
        // Expected format: [{ year: 2022, month: 10, label: 'Event', description: 'Description' }]
    },
    lineLabel: {
        type: String,
        default: 'Timeline'
    },
    layerColor: {
        type: String,
        default: 'black'
    },
    startPoint: {
        type: Number,
        default: 15 // Percentage from left where the timeline starts
    },
    dotLineLength: {
        type: Number,
        default: 80
    }
});

// Calculate data point positions
const dataPointPositions = computed(() => {
    return props.dataPoints.map((point, index) => {
        const totalYears = props.endYear - props.startYear;
        const yearProgress = (point.year - props.startYear) / totalYears;

        // If month is specified, add fractional position within the year
        const monthOffset = point.month ? (point.month - 1) / 12 / totalYears : 0;
        const totalProgress = yearProgress + monthOffset;

        const dotPosition = props.startPoint + (totalProgress * 50);
        const dotHeight = props.startPoint + (totalProgress * 50);

        return {
            ...point,
            x: dotPosition,
            y: dotHeight,
            id: `datapoint-${index}`
        };
    });
});

// Calculate the dynamic start position based on the first data point
const dynamicStartPositionHorizontal = computed(() => {
    if (dataPointPositions.value.length === 0) {
        return props.startPoint; // fallback to prop if no data points
    }
    return dataPointPositions.value[0].x;
});

const dynamicStartPositionVertical = computed(() => {
    if (dataPointPositions.value.length === 0) {
        return props.startPoint; // fallback to prop if no data points
    }
    return dataPointPositions.value[0].y;
});

// Calculate the dynamic width from first to last data point
const dynamicWidth = computed(() => {
    if (dataPointPositions.value.length <= 1) {
        return 50; // fallback width
    }
    const firstPoint = dataPointPositions.value[0].x;
    const lastPoint = dataPointPositions.value[dataPointPositions.value.length - 1].x;
    return lastPoint - firstPoint;
});

const dynamicHeight = computed(() => {
    if (dataPointPositions.value.length <= 1) {
        return 50; // fallback height
    }
    const firstPoint = dataPointPositions.value[0].y;
    const lastPoint = dataPointPositions.value[dataPointPositions.value.length - 1].y;
    return lastPoint - firstPoint;
});
</script>

<template>
    <div class="layer-arrow"
        :style="isMobile() ? { left: '20vw' } : { marginTop: props.dotLineLength + 'px' }">
        <!-- Main horizontal line -->
        <div class="layer-line" :style="isMobile() ? {
            backgroundColor: layerColor,
            top: dynamicStartPositionVertical + 'vh',
            left: props.dotLineLength + 'px',
            height: dynamicHeight + 'vh'
        } : {
            backgroundColor: layerColor,
            left: dynamicStartPositionHorizontal + '%',
            width: dynamicWidth + '%'
        }">
            <h1>{{ props.lineLabel }}</h1>
        </div>

        <!-- Year markers with vertical dotted lines -->
        <div v-for="dataPoint in dataPointPositions" :key="dataPoint.id" class="year-connector"
            :style="isMobile() ? { top: dataPoint.y + 'vh' } : { left: dataPoint.x + 'vw' }">
            <div class="vertical-dotted-line" :style="isMobile() ? {
                borderColor: layerColor,
                width: props.dotLineLength + 'px'
            } : {
                borderColor: layerColor,
                height: props.dotLineLength + 'px'
            }"></div>
        </div>

        <!-- Data points -->
        <div v-for="dataPoint in dataPointPositions" :key="dataPoint.id" class="data-point" :style="isMobile() ? {
            top: dataPoint.y - 1 + 'vh'
        } : { left: dataPoint.x + 'vw' }">
            <!-- Only show data point elements if there's a label -->
            <template v-if="dataPoint.label">
                <!-- Vertical connector line -->
                <div class="data-connector" :style="{ borderColor: layerColor }"></div>

                <!-- Data point marker -->
                <div class="data-marker" :style="{
                    backgroundColor: layerColor,
                    boxShadow: `0 0 0 1px ${layerColor}`
                }"></div>

                <!-- Data point content -->
                <div class="data-content">
                    <div class="data-label" :style="{ color: layerColor }">{{ dataPoint.label }}</div>
                </div>
            </template>
        </div>
    </div>
</template>

<style scoped>
.layer-arrow {
    position: relative;
    width: 100%;
    height: fit-content;
    z-index: 2;
}

.layer-line {
    position: absolute;
    height: 5px;
    text-align: center;
}

.layer-line h1 {
    margin: 10px 0;
    font-size: 16px;
    color: black;
    font-weight: 500;
}

.year-connector {
    position: absolute;
    bottom: 0;
    transform: translateX(-50%);
}

.vertical-dotted-line {
    width: 0;
    border-left: 2.5px dotted;
    opacity: 0.8;
}

.data-point {
    position: absolute;
    transform: translateX(-50%);
    display: flex;
    flex-direction: column;
    align-items: center;
}

.data-connector {
    width: 0;
    height: 15px;
    border-left: 1px solid;
}

.data-marker {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    border: 2px solid white;
    margin-bottom: 8px;
    z-index: 3;
}

.data-content {
    text-align: center;
}

.data-label {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 2px;
    line-height: 1.2;
}

@media (max-width: 768px) {
    .layer-arrow {
        position: absolute;
        top: 0;
        height: 100%;
        width: auto;
        z-index: 10;
    }

    .layer-line {
        position: absolute;
        width: 5px;
        text-align: start;
    }

    .layer-line h1 {
        margin: 0 0 0 -25vw;
        font-size: 14px;
        height: fit-content;
    }

    .vertical-dotted-line {
        height: 0;
        border-top: 2.5px dotted;
        border-left: none;
    }

    .year-connector {
        transform: none;
    }

    .data-point {
        flex-direction: row;
        transform: translateX(-100%);
        justify-content: space-between;
    }

    .data-connector {
        height: 0;
        width: 15px;
        border-top: 1px solid;
        border-left: none;
        order: 2;
    }

    .data-marker {
        margin-bottom: 0;
        order: 1;
    }

    .data-content {
        text-wrap: wrap;
        width: 60%;
    }

    .data-label {
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 2px;
        line-height: 1.2;
        transform: rotate(-90deg);
    }
}
</style>