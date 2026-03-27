<script setup>
import { ref, computed } from 'vue';
import Timeline from './Timeline.vue';
import LayerArrow from './LayerArrow.vue';
import BubbleLabel from './BubbleLabel.vue';
import { isMobile } from '@src/composables/utils.js';

const props = defineProps({
    chartType: {
        type: String,
        default: 'stats',
        validator: (value) => ['stats', 'mehrwert'].includes(value)
    },
    years: {
        type: Array,
        default: () => [2022, 2023, 2024, 2025]
    },
    height: {
        type: String,
        default: '60vh'
    },
    bubblePosition: {
        type: Array,
        default: () => [15, 39, 65]
    },
    timelineStart: {
        type: Number,
        default: 10
    },
    percentageShift: {
        type: Number,
        default: 25
    },
    bubbleGap: {
        type: Number,
        default: 1
    },
    statsData: {
        type: Object,
        default: null
    },
    mehrwertData: {
        type: Array,
        default: () => []
    }
});

const statsData = computed(() => {
    console.log('statsData prop:', props.statsData);
    return props.statsData;
});

const mehrwertData = computed(() => {
    console.log('mehrwertData prop:', props.mehrwertData);
    return props.mehrwertData;
});

const bubbleConfig = {
    telefon: {
        label: 'Telefon',
        color: '#001C0C',
        fontSize: isMobile() ? '9vw' : '4.5vw',
        borderRadius: isMobile() ? 25 : 40
    },
    bke: {
        label: 'Brief, Kontaktformular, E-Mail',
        color: '#004F22',
        fontSize: isMobile() ? '3.5vw' : '1.5vw',
        borderRadius: isMobile() ? 12 : 16
    },
    sm: {
        label: 'Social Media',
        color: '#43A86B',
        fontSize: isMobile() ? '3vw' : '1.25vw',
        borderRadius: isMobile() ? 8 : 12
    },
    'Klassische Kanäle': {
        label: 'Klassische Kanäle',
        color: 'rgba(0, 28, 12, 0.9)',
        fontSize: isMobile() ? '9vw' : '4.5vw',
        borderRadius: isMobile() ? 25 : 40
    }
};

const chartData = computed(() => {
    return generateChart(props.chartType);
});

const getBubbleLabel = (type) => bubbleConfig[type]?.label || type;
const getBubbleColor = (type) => bubbleConfig[type]?.color;
const getNumberFontSize = (type) => bubbleConfig[type]?.fontSize;
const getBorderRadius = (color) => {
    const config = Object.values(bubbleConfig).find(c => c.color === color);
    return config?.borderRadius;
};

const getBubbleSize = (value) => {
    const minSize = 2;
    const maxSize = 25;
    const minValue = 0;
    let maxValue = 310000;

    if (value === 0) return 0;
    if (value < minValue) value = minValue;

    // Scale by area for proportional representation
    // Area = π * r² = π * (diameter/2)²
    // So diameter = 2 * sqrt(area/π)

    // First, scale the value to get proportional area
    const minArea = Math.PI * Math.pow(minSize / 2, 2);
    const maxArea = Math.PI * Math.pow(maxSize / 2, 2);

    const scaledArea = minArea + ((value - minValue) / (maxValue - minValue)) * (maxArea - minArea);

    // Convert area back to diameter
    const diameter = 2 * Math.sqrt(scaledArea / Math.PI);

    return Math.max(minSize, Math.min(maxSize, Math.round(diameter * 10) / 10));
};

const labelPositions = computed(() => {
    const bubbles = chartData.value;
    const types = props.chartType === 'mehrwert'
        ? ['Klassische Kanäle']
        : ['sm', 'bke', 'telefon'];

    return types.reduce((positions, type) => {
        const config = bubbleConfig[type];
        const bubble = bubbles.find(b => b.label === config?.label);

        if (bubble) {
            positions[type] = bubble.position.y + (bubble.height / 2);
        }

        return positions;
    }, {});
});

const generateChart = (chartType) => {
    // Chart configuration based on type
    const chartConfigs = {
        stats: {
            data: statsData.value,
            dataItems: statsData.value ? [
                { key: 'telefon', data: statsData.value.telefonRecords },
                { key: 'bke', data: statsData.value.bkeRecords },
                { key: 'sm', data: statsData.value.smRecords },
            ] : [],
            years: props.years,
            getValue: (dataItem, year) => dataItem.data[`total${year}`],
            getLabel: (dataItem) => getBubbleLabel(dataItem.key),
            getColor: (dataItem) => getBubbleColor(dataItem.key),
            getFontSize: (dataItem) => getNumberFontSize(dataItem.key)
        },
        mehrwert: {
            data: mehrwertData.value,
            dataItems: ['Klassische Kanäle', 'Chat'],
            years: props.years,
            getValue: (category, year) => {
                const dataPoint = mehrwertData.value?.find(d => d.year === year && d.category === category);
                return dataPoint ? dataPoint.value : 0;
            },
            getLabel: (category) => getBubbleLabel(category),
            getColor: (category) => getBubbleColor(category),
            getFontSize: (category) => getNumberFontSize(category)
        }
    };

    const config = chartConfigs[chartType];
    if (!config || !config.data) return [];

    const bubbles = [];
    let bubbleId = 1;

    const columnHeights = [0, 0, 0];
    const baselineY = 2;

    // Generate bubbles for each data item and year
    config.dataItems.forEach((dataItem) => {
        config.years.forEach((year, yearIndex) => {
            const value = config.getValue(dataItem, year, yearIndex);

            // Skip creating bubble if value is 0
            if (value === 0) return;

            const bubbleHeight = getBubbleSize(value);

            bubbles.push({
                id: bubbleId++,
                number: value,
                label: config.getLabel(dataItem),
                value: value,
                height: bubbleHeight,
                position: {
                    x: props.bubblePosition[yearIndex],
                    y: columnHeights[yearIndex] + baselineY
                },
                color: config.getColor(dataItem),
                fontSize: config.getFontSize(dataItem)
            });

            // Update cumulative height for the column
            columnHeights[yearIndex] += bubbleHeight * props.bubbleGap + 0.5;
        });
    });
    return bubbles;
};
</script>

<template>
    <div class="arrow-bubble-chart" :style="{ height: props.height }">
        <div class="chart-container">
            <Timeline v-if="isMobile()" :years="props.years" :start-point="props.timelineStart"
                :markers-gap="props.percentageShift" />
            <Timeline v-else :years="props.years" :start-point="props.timelineStart"
                :markers-gap="props.percentageShift" />
            <LayerArrow v-if="props.chartType === 'mehrwert'" :startYear="2022" :endYear="2024" :dataPoints="[
                { year: 2023, month: 10, label: isMobile() ? 'Okt.' : 'Oktober 2023' },
                { year: 2024, month: 9 }
            ]" :start-point="isMobile() ? 0 : props.timelineStart" :dot-line-length="isMobile() ? 250 : 90"
                :line-label="'52 200 betreute Dialoge'" :layer-color="'#0E6631'" />
            <LayerArrow v-if="props.chartType === 'mehrwert'" :startYear="2022" :endYear="2024" :dataPoints="[
                { year: 2022, month: 10, label: isMobile() ? 'Okt.' : 'Oktober 2022' },
                { year: 2024, month: 9, label: isMobile() ? 'Sep.' : 'September 2024' }
            ]" :start-point="isMobile() ? 0 : props.timelineStart" :dot-line-length="isMobile() ? 300 : 180"
                :line-label="'16 327 Chatbot-Dialoge'" :layer-color="'#43A86B'" />

            <div class="category-labels">
                <div v-if="props.chartType === 'mehrwert'">
                    <BubbleLabel :text="'Klassische Kanäle'" :color="getBubbleColor('Klassische Kanäle')"
                        :fontSize="getNumberFontSize('Klassische Kanäle')"
                        :position="labelPositions['Klassische Kanäle']" :spacing-factor="0.8" />
                </div>
                <div v-else class="stats-labels">
                    <div>
                        <BubbleLabel :text="'Social Media'" :color="getBubbleColor('sm')"
                            :fontSize="getNumberFontSize('sm')" :position="labelPositions['sm']"
                            :spacing-factor="2.2" />
                    </div>
                    <div>
                        <BubbleLabel :text="'Brief, Kontaktformular, E-Mail'" :color="getBubbleColor('bke')"
                            :fontSize="getNumberFontSize('bke')" :position="labelPositions['bke']"
                            :spacing-factor="1.2" />
                    </div>
                    <div>
                        <BubbleLabel :text="'Telefon'" :color="getBubbleColor('telefon')"
                            :fontSize="getNumberFontSize('telefon')" :position="labelPositions['telefon']"
                            :spacing-factor="0.6" />
                    </div>
                </div>
            </div>
        </div>

        <div v-if="isMobile()" v-for="bubble in chartData" :key="bubble.id" class="bubble" :style="{
            top: bubble.position.x + 'vh',
            left: bubble.position.y + 22 + 'vw',
            width: getBubbleSize(bubble.value) * props.bubbleGap + 'vw',
            height: bubble.height / 1.5 + 'vh',
            backgroundColor: bubble.color,
            borderRadius: getBorderRadius(bubble.color) + 'px'
        }">
            <div class="bubble-number" :style="{ fontSize: bubble.fontSize }">{{ bubble.number }}</div>
        </div>
        <div v-if="!isMobile()" v-for="bubble in chartData" :key="bubble.id" class="bubble" :style="{
            left: bubble.position.x + '%',
            bottom: bubble.position.y + 'vh',
            width: getBubbleSize(bubble.value / 1.5) + 'vw',
            height: bubble.height + 'vh',
            backgroundColor: bubble.color,
            borderRadius: getBorderRadius(bubble.color) + 'px'
        }">
            <div class="bubble-number" :style="{ fontSize: bubble.fontSize }">{{ bubble.number }}</div>
        </div>
    </div>
</template>

<style scoped>
.arrow-bubble-chart {
    width: 100%;
    position: absolute;
    display: flex;
    align-items: center;
    justify-content: center;
}

.chart-container {
    width: 100%;
    height: 100%;
    position: relative;
}

.bubble {
    position: absolute;
    color: white;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    z-index: 3;
    font-size: 0.9rem;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 0.85px solid rgba(217, 217, 217, 1);
}

.bubble-number {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 0.2rem;
    line-height: 1;
}

.category-labels {
    position: absolute;
    left: 0;
    bottom: 5%;
    display: flex;
    flex-direction: column;
    z-index: 2;
    padding-left: 1rem;
    width: 23%;
}

.stats-labels {
    position: relative;
    width: 100%;
    height: 100%;
}

@media (max-width: 768px) {
    .chart-container {
        margin-top: 15vh;
    }

    .category-labels {
        position: absolute;
        width: 100%;
        top: -10%;
        display: flex;
        flex-direction: row;
        z-index: 2;
        padding-left: 1rem;
    }

    .stats-labels {
        position: relative;
        width: 100%;
        height: 100%;
    }

}
</style>