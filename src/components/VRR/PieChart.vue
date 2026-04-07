<script setup>
import { ref, watch, onMounted } from 'vue';
import * as d3 from 'd3';
import EditableTextField from '@src/components/EditableTextField.vue';

const props = defineProps({
    data: { type: Array, default: () => [] },
    activeMode: { type: String, default: 'view' }
});

const emit = defineEmits(['pieSliceSelected']);

const arcs = ref([]);
const selectedIndex = ref(0);
const radius = 170;
const expandedRadius = 180;
const colors = ['#52AE32', '#63BEDD'];
const labels = ['Anfragen automatisiert beantwortet', 'an Servicepersonal weitergeleitet'];
const arcGenerator = d3.arc().innerRadius(0).outerRadius(radius);
const expandedArcGenerator = d3.arc().innerRadius(0).outerRadius(expandedRadius);

function changePart(index) {
    selectedIndex.value = index;

    const sliceData = {
        index: index,
        percentage: arcs.value[index]?.data?.Percentage || 0
    };

    emit('pieSliceSelected', sliceData);
}

watch(() => props.data, (newData) => {
    if (!newData || newData.length === 0) return;
    const pie = d3.pie().value(d => +d.Percentage);
    arcs.value = pie(newData);
}, { immediate: true });
</script>

<template>
    <svg viewBox="-200 -200 400 400">
        <g>
            <!-- non-selected slices are getting rendered first -->
            <path v-for="(arc, index) in arcs" :key="`normal-${index}`" v-show="selectedIndex !== index"
                :d="arcGenerator(arc)" :fill="colors[index]" stroke="none" stroke-width="0" filter="grayscale(1)"
                :style="{
                    cursor: 'pointer',
                    transition: 'all 0.3s ease'
                }" @click="changePart(index)" />

            <!-- selected slice is rendered last to appear on top -->
            <path v-for="(arc, index) in arcs" :key="`selected-${index}`" v-show="selectedIndex === index"
                :d="expandedArcGenerator(arc)" :fill="colors[index]" filter="drop-shadow(-5px 8px 0px #FFF)" :style="{
                    cursor: 'pointer',
                    transition: 'all 0.3s ease'
                }" @click="changePart(index)" />

            <!-- Labels -->
            <g v-for="(arc, index) in arcs" :key="`label-${index}`">
                <foreignObject :x="arcGenerator.centroid(arc)[0] - 90" :y="arcGenerator.centroid(arc)[1] - 40"
                    width="150" height="80" style="pointer-events: none;">
                    <div class="label-container">
                        <div class="percentage-text">
                            {{ arc.data.Percentage }}%
                        </div>
                        <div class="description-text">
                            <EditableTextField :model-value="labels[index]" :active-mode="activeMode"
                                @update:model-value="val => labels[index] = val" :rows="2" :width="'100%'"
                                :font-size="'12px'" :line-height="1.3" :padding="'0'" :font-weight="'400'"
                                :border-radius="'8px'" />
                        </div>
                    </div>
                </foreignObject>
            </g>
        </g>
    </svg>
</template>

<style scoped>
svg {
    height: 100%;
}

/* non-selected slices on hover get original color */
path[filter="grayscale(1)"]:hover {
    filter: grayscale(0);
}

/* selected slice always has shadow */
path[filter="url(#expandedDropShadow)"]:hover {
    filter: url(#expandedDropShadow);
}

.label-container {
    background-color: white;
    border-radius: 8px;
    padding-left: 10px;
    width: 100%;
    height: 100%;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: left;
}

.percentage-text {
    font-size: 24px;
    font-weight: 700;
    color: black;
}

.description-text {
    font-size: 12px;
    font-weight: 400;
    color: black;
    line-height: 1.3;
}
</style>