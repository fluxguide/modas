<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useScroll, useElementBounding } from '@vueuse/core'
import ArrowBubbleChart from './ArrowBubbleChart.vue'
import Timeline from './Timeline.vue'
import { isMobile } from '@src/composables/utils.js'

const props = defineProps({
    // How many additional year panels to create
    additionalPanels: {
        type: Number,
        default: 1
    },
    // How many years to shift for each panel
    yearShift: {
        type: Number,
        default: 1
    },
    // Height of the wrapper (affects scroll distance)
    wrapperHeight: {
        type: String,
        default: '300vh'
    },
    // Show progress indicator
    showProgress: {
        type: Boolean,
        default: true
    },
    // Scroll sensitivity (lower = more sensitive)
    scrollSensitivity: {
        type: Number,
        default: 0.3
    },
    statsData: {
        type: Object,
        default: null
    },
    mehrwertData: {
        type: Array,
        default: () => []
    },
    categoryNames: { type: Object, default: () => ({}) },
})

// Get all other props to pass to ArrowBubbleChart
const chartProps = computed(() => {
    const { additionalPanels, yearShift, wrapperHeight, showProgress, scrollSensitivity, ...rest } = props
    return rest
})

// Refs
const containerRef = ref()
const scrollX = ref(0)

// Use useScroll to track window scroll
const { y: scrollY } = useScroll(window)

// Get bounding info for the container
const { top: containerTop, height: containerHeight } = useElementBounding(containerRef)

// Generate panels (same years for all panels, different content)
const panelCount = computed(() => props.additionalPanels + 1)

// Calculate horizontal scroll progress based on vertical scroll
const scrollProgress = computed(() => {
    if (!containerTop.value || !containerHeight.value) return 0

    // Start scrolling when the container comes into view
    const scrollStart = containerTop.value + window.innerHeight * props.scrollSensitivity
    // End scrolling when we've scrolled through the container
    const scrollEnd = containerTop.value + containerHeight.value - window.innerHeight * (1 - props.scrollSensitivity)

    if (scrollY.value < scrollStart) return 0
    if (scrollY.value > scrollEnd) return 1

    return (scrollY.value - scrollStart) / (scrollEnd - scrollStart)
})

// Watch for scroll progress changes and update horizontal position
watch(scrollProgress, (progress) => {
    // Calculate max scroll distance
    // Each panel is 100vw, so total scroll = (number of panels - 1) * viewport width
    const maxScroll = window.innerWidth * (props.additionalPanels)
    scrollX.value = progress * maxScroll
}, { immediate: true })

// Handle window resize
const handleResize = () => {
    // Recalculate scroll position on resize
    const maxScroll = window.innerWidth * (props.additionalPanels)
    scrollX.value = scrollProgress.value * maxScroll
}

onMounted(() => {
    window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
})

defineExpose({
    scrollProgress,
    currentPanelIndex: computed(() => Math.floor(scrollProgress.value * panelCount.value))
})
</script>

<template>
    <div ref="containerRef" class="horizontal-scroll-wrapper" :style="{ height: wrapperHeight }">
        <!-- Sticky container that holds the horizontally scrolling content -->
        <div class="horizontal-scroll-container">
            <div class="horizontal-content" :style="{ transform: `translateX(-${scrollX}px)` }">

                <div v-for="panelIndex in panelCount" :key="`panel-${panelIndex}`" class="chart-panel">
                    <!-- Pass through all props to ArrowBubbleChart -->
                    <div class="timeline-wrapper" :style="{ width: '100%' }">
                        <div v-if="panelIndex === 1">
                            <ArrowBubbleChart v-if="panelIndex === 1" v-bind="chartProps" :chartType="'mehrwert'"
                                :years="[2022, 2023, 2024, 2025]" :height="isMobile() ? '75vh' : '45vh'"
                                :bubble-position="isMobile() ? [8, 30, 53] : [28, 53, 78]"
                                :timeline-start="isMobile() ? 5 : 25" :percentage-shift="isMobile() ? 30 : 25"
                                :bubble-gap="2" />
                            <div class="mehrwert-bg-img">
                                <img id="theo" src="@img/VRR/Characters/Theo.svg" alt="Theo" />
                                <img id="orange-tram" src="@img/VRR/Transport/TramOrange.svg" alt="Orange Tram" />
                            </div>
                        </div>
                        <div v-if="panelIndex === 2" class="panel-content">
                            <div class="content-above-timeline">
                                <div class="section-wrapper">
                                    <img id="waving-robot" src="@img/VRR/Robot/Waving.svg" alt="Waving Robot">
                                    <div class="coloured-space">
                                        <div class="white-space">
                                            <h1 class="h1-list">
                                                <ul>
                                                    <span>
                                                        Auf Basis der gesammelten Erfahrungen werden vom VRR folgende
                                                        Ziele
                                                        verfolgt:
                                                    </span>
                                                    <li>Aufbau eines vollautomatisierten KI-Chatbots inkl. LLM als
                                                        nächste Entwicklungsstufe</li>
                                                    <li>Vernetzte, KI-gestützte Serviceplattform</li>
                                                </ul>
                                            </h1>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="timeline-at-bottom">
                                <Timeline :years="[2026, 2027, 2028]" :start-point="25" :markers-gap="25" />
                            </div>
                            <div class="bg-theresa">
                                <img id="theresa" src="@img/VRR/Characters/Theresa.svg" alt="Theresa" />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.horizontal-scroll-wrapper {
    position: relative;
    width: 100%;
}

.horizontal-scroll-container {
    position: sticky;
    top: 0;
    height: 100vh;
    width: 100%;
    overflow: hidden;
    z-index: 10;
}

.horizontal-content {
    display: flex;
    height: 100%;
    will-change: transform;
    transition: transform 0.1s ease-out;
}

.timeline-wrapper {
    position: relative;
    display: flex;
    flex-direction: column;
    height: 45vh;
    width: 100%;
}

.panel-content {
    position: relative;
    display: flex;
    flex-direction: column;
    height: 45vh;
    width: 100%;
}

.content-above-timeline {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    z-index: 2;
}

.timeline-at-bottom {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: auto;
    z-index: 1;
}

.chart-panel {
    min-width: 100vw;
    width: 100vw;
    height: 100%;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.panel-background {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 1;
}

.default-bg {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    color: #ccc;
}

.mehrwert-bg-img {
    position: relative;
    width: 100%;
    height: 30vh;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    margin-top: -25vh;
}

.mehrwert-bg-img #orange-tram,
.mehrwert-bg-img #theo {
    opacity: 0.08;
    height: 100%;
}

.section-wrapper {
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.coloured-space {
    width: 40%;
    height: fit-content;
    display: flex;
    align-items: center;
    justify-content: center;
    position: absolute;
    top: 0;
    padding: 20px 20px;
    background-image: linear-gradient(rgba(255, 255, 255, 0.75), rgba(115, 245, 70, 0.75), rgba(114, 219, 255, 0.75));
    border-radius: 20px;
    pointer-events: none;
    z-index: 3;
}

.white-space {
    width: 95%;
    height: fit-content;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    background-color: white;
    border-radius: 20px;
    padding: 0px 20px;
}


.white-space .h1-list {
    width: 100%;
}

.white-space .h1-list ul span {
    font-weight: 400;
}

.white-space h1 {
    line-height: 1.8;
    text-wrap: wrap;
    font-size: 25px;
}

#waving-robot {
    position: absolute;
    top: -20%;
    left: 22%;
    height: 80%;
    z-index: 2;
    transform: rotate(-40deg);
}

.bg-theresa {
    position: absolute;
    top: 0;
    right: 5%;
    height: 60%;
    z-index: 2;
}

#theresa {
    transform: rotateY(180deg);
    opacity: 0.1;
    z-index: 1;
}

@media (max-width: 768px) {
    .horizontal-scroll-container {
        position: relative;
        height: auto;
        overflow: visible;
    }

    .horizontal-content {
        display: flex;
        flex-direction: column;
        transform: none !important;
        width: 100%;
    }

    .chart-panel {
        width: 100vw;
        height: 75vh;
        align-items: start;
        margin-top: 0;
    }

    .chart-panel :deep(.arrow-line) {
        height: 100%;
    }

    .timeline-wrapper {
        height: 100%;
    }

    .panel-content {
        height: 100%;
    }

    .coloured-space {
        width: 60%;
        padding: 15px 10px;
        right: 5%;
        top: 20%;
    }

    .white-space h1 {
        font-size: 16px;
    }

    #waving-robot {
        top: 0;
        right: 5%;
        height: 50%;
        transform: rotate(-30deg);
    }

    .bg-theresa {
        position: relative;
        z-index: 1;
    }

    .bg-theresa #theresa {
        position: absolute;
        bottom: 0;
        right: 0;
        height: 60%;
    }

    .mehrwert-bg-img {
        height: 20vh;
        margin-top: 0;
    }

    .timeline-wrapper :deep(.chart-container) {
        margin-top: 0;
    }

    .timeline-wrapper :deep(.category-labels) {
        top: 0;
    }

    .timeline-wrapper :deep(.label-text) {
        width: fit-content;
    }

    .timeline-at-bottom {
        top: 0;
        height: 100%;
    }
}
</style>