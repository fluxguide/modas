<script setup>
import { computed, ref } from 'vue'
import EditableTextField from '@src/components/EditableTextField.vue'
import { Streamlit } from 'streamlit-component-lib'

const props = defineProps({
    years: {
        type: Array,
        default: () => ['year1', 'year2', 'year3', 'year4']
    },
    yearLabels: {
        type: Array,
        default: () => ['Year 1', 'Year 2', 'Year 3', 'Year 4']
    },
    showMarkers: {
        type: Boolean,
        default: true
    },
    startPoint: {
        type: Number,
        default: 10 // Percentage from left where the timeline starts
    },
    markersGap: {
        type: Number,
        default: 25 // Additional percentage to add to the left position of the last year marker
    },
    activeMode: {
        type: String,
        default: 'view'
    }
});

const emit = defineEmits(['update:yearLabels']);

const updateYearLabel = (index, value) => {
    const next = [...props.yearLabels];
    next[index] = value;
    emit('update:yearLabels', next);
};
</script>

<template>
    <div class="timeline">
        <div class="arrow-line">
            <div v-if="showMarkers" class="year-markers">
                <div v-for="(year, index) in years" :key="index" class="year-marker" :style="{
                    left: (props.startPoint + (index * props.markersGap)) + '%'
                }">
                    <div class="year-dot"></div>
                    <div class="year-label">
                        <EditableTextField :model-value="yearLabels[index]"
                            @update:model-value="val => updateYearLabel(index, val)" :active-mode="activeMode" :rows="1"
                            :width="'10vw'" :font-size="'24px'" :line-height="1" :padding="'0'" :text-align="'center'"
                            :font-weight="'bold'" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.timeline {
    position: relative;
    width: 100%;
    height: 100%;
    z-index: 3;
}

.arrow-line {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 10px;
    background-color: black;
}

.year-markers {
    position: absolute;
    width: 100%;
    height: 100%;
}

.year-marker {
    position: absolute;
    display: flex;
    flex-direction: column;
    align-items: center;
    z-index: 4;
}

.year-dot {
    width: 30px;
    height: 30px;
    background: black;
    border-radius: 50%;
    position: relative;
    top: -10px;
}

.year-label {
    font-size: 1.5rem;
    font-weight: 600;
    color: black;
}

@media (max-width: 768px) {
    .arrow-line {
        top: 0;
        width: 8px;
        height: 80%;
        left: 18%;
    }

    .year-marker {
        flex-direction: row;
        gap: 10px;
        transform: translateX(-80%);
    }

    .year-dot {
        width: 20px;
        height: 20px;
        top: 0;
    }

    .year-label {
        transform: rotate(-90deg);
        font-size: 18px;
    }
}
</style>
