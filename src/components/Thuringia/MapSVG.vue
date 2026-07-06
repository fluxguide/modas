<script setup>
import * as d3 from 'd3'
import { ref, onMounted, onUnmounted, watch, nextTick, computed } from 'vue'
import { Streamlit } from 'streamlit-component-lib';
import regionConfig from '@src/data/regions.json'

const props = defineProps({
    csvData: {
        type: Array,
        default: () => []
    },
    colorFill: {
        type: String,
        default: '#006F45'
    },
    colorStroke: {
        type: String,
        default: '#e3dbc3'
    },
    activeMode: {
        type: String,
        default: 'view'
    },
    selectedRegion: {
        type: String,
        default: 'Thüringen',
    },
})

const emit = defineEmits(['update:modelValue'])

const openMapEditor = () => {
    Streamlit.setComponentValue({ action: "open_map_editor" });
};

const regionBounds = Object.fromEntries(
    Object.entries(regionConfig).map(([region, cfg]) => [region, cfg.bounds]),
)

const mapAssets = import.meta.glob(
    '../../../static/img/Thuringia/maps/*.{png,svg}',
    { eager: true, import: 'default' },
)
const mapUrlByFile = {}
for (const [path, url] of Object.entries(mapAssets)) {
    mapUrlByFile[path.split('/').pop().normalize('NFC')] = url
}
const regionMaps = Object.fromEntries(
    Object.entries(regionConfig).map(
        ([region, cfg]) => [region, mapUrlByFile[cfg.map.normalize('NFC')]],
    ),
)
const ThuringenMap = regionMaps['Thüringen']

const width = 1360
const height = 1065

const CALIBRATED_REGIONS = new Set(['Thüringen'])
const isCalibratedRegion = (region) =>
    CALIBRATED_REGIONS.has(region) || !regionBounds[region]

const MAP_PADDING = 0.0

// Refs for DOM elements
const mapSvg = ref(null)
const mapSvgRaw = computed(() => {
    return regionMaps[props.selectedRegion] || ThuringenMap
})
const mapGroup = ref(null)
const dataGroup = ref(null)

// Reactive state
const projection = ref(null)

const setupProjection = () => {
    if (isCalibratedRegion(props.selectedRegion)) {
        projection.value = d3.geoMercator()
            .center([10.87, 51.33])
            .scale(24800)
        return
    }

    const [west, south, east, north] = regionBounds[props.selectedRegion]
    const padX = width * MAP_PADDING
    const padY = height * MAP_PADDING

    projection.value = d3.geoMercator().fitExtent(
        [[padX, padY], [width - padX, height - padY]],
        {
            type: 'MultiPoint',
            coordinates: [[west, south], [east, north]],
        },
    )
}

const loadSVGContent = async () => {
    const mapUrl = mapSvgRaw.value

    console.log('Loading map content from:', mapUrl)

    if (!mapUrl || !mapGroup.value) {
        console.warn('No map content or mapGroup not ready')
        return
    }

    const group = d3.select(mapGroup.value)

    const isCalibrated = isCalibratedRegion(props.selectedRegion)
    const padX = width * MAP_PADDING
    const padY = height * MAP_PADDING
    const fit = isCalibrated
        ? { x: 0, y: 0, w: width, h: height }
        : { x: padX, y: padY, w: width - 2 * padX, h: height - 2 * padY }

    try {
        if (mapUrl.includes('.svg')) {
            const response = await fetch(mapUrl)
            if (!response.ok) {
                throw new Error(`Failed to load SVG: ${response.status}`)
            }
            const svgContent = await response.text()
            group.html(svgContent)

            if (!isCalibrated) {
                const inner = group.select('svg')
                if (!inner.empty()) {
                    if (!inner.attr('viewBox')) {
                        const w = parseFloat(inner.attr('width')) || width
                        const h = parseFloat(inner.attr('height')) || height
                        inner.attr('viewBox', `0 0 ${w} ${h}`)
                    }
                    inner
                        .attr('x', fit.x)
                        .attr('y', fit.y)
                        .attr('width', fit.w)
                        .attr('height', fit.h)
                        .attr('preserveAspectRatio', 'xMidYMid meet')
                }
            }
        } else {
            // Raster maps (e.g. PNG): fit + center into the same box.
            group
                .html('')
                .append('image')
                .attr('href', mapUrl)
                .attr('x', fit.x)
                .attr('y', fit.y)
                .attr('width', fit.w)
                .attr('height', fit.h)
                .attr('preserveAspectRatio', 'xMidYMid meet')
        }

        console.log('Map content loaded successfully')

    } catch (error) {
        console.error('Error loading map:', error)
    }
}

// Plot data points as drop markers
const plotDataPoints = () => {
    console.log('Plotting data points. Data length:', props.csvData?.length)

    if (!props.csvData || props.csvData.length === 0) {
        console.log('No data to plot')
        return
    }

    // Clear previous points
    d3.select(dataGroup.value).selectAll('*').remove()

    // Create drop-shaped markers
    const markers = d3.select(dataGroup.value)
        .selectAll('.townhall-point')
        .data(props.csvData)
        .enter()
        .append('g')
        .attr('class', 'townhall-point')
        .attr('transform', d => {
            const coords = projection.value([d.longitude, d.latitude])
            return coords ? `translate(${coords[0]}, ${coords[1]})` : 'translate(0, 0)'
        })

    markers.append('g')
        .attr('class', 'drop-marker')
        .attr('transform', 'scale(0)')
        .html(d => `
      <path d="M0,-15 C-6,-15 -10,-11 -10,-5 C-10,2.5 0,15 0,15 S10,2.5 10,-5 C10,-11 6,-15 0,-15 Z" 
            fill="${props.colorFill}" 
            stroke="${props.colorStroke}" 
            stroke-width="1.5"
            filter="url(#drop-shadow-${d.id})"/>
      <circle cx="0" cy="-5" r="3" fill="${props.colorStroke}"/>
    `)

    // animate appearance
    markers.select('.drop-marker')
        .transition()
        .duration(400)
        .delay((d, i) => i * 3)
        .attr('transform', 'scale(1.2)')
}

// Initialize the map
const initializeMap = async () => {
    try {
        setupProjection()

        await loadSVGContent()

        plotDataPoints()
    } catch (error) {
        console.error('Error initializing map:', error)
    }
}

// Watchers
watch(() => props.csvData, () => {
    console.log('CSV Data changed:', props.csvData?.length)
    if (props.csvData && props.csvData.length > 0) {
        plotDataPoints()
    }
}, { deep: true })

watch(() => props.selectedRegion, async () => {
    if (!mapGroup.value) return

    setupProjection()
    await loadSVGContent()
    await nextTick()
    plotDataPoints()
})

onMounted(() => {
    initializeMap()
})
</script>

<template>
    <div class="map-container" :class="{ 'is-edit': props.activeMode === 'edit' }">
        <button v-if="props.activeMode === 'edit'" class="chart-edit-btn" @click.stop="openMapEditor"
            title="Diagrammdaten bearbeiten" aria-label="Diagrammdaten bearbeiten">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path
                    d="M12.2358 0.139355C12.1466 0.0501261 12.0255 0 11.8993 0C11.7731 0 11.6521 0.0501261 11.5628 0.139355L9.99501 1.70717L13.5238 5.23595L15.0916 3.66909C15.1359 3.62487 15.1711 3.57235 15.1951 3.51453C15.2191 3.4567 15.2314 3.39471 15.2314 3.3321C15.2314 3.2695 15.2191 3.20751 15.1951 3.14968C15.1711 3.09186 15.1359 3.03934 15.0916 2.99512L12.2358 0.139355ZM12.8508 5.90896L9.322 2.38018L3.1345 8.56768H3.33155C3.45778 8.56768 3.57884 8.61783 3.6681 8.70709C3.75736 8.79635 3.80751 8.91741 3.80751 9.04364V9.5196H4.28347C4.4097 9.5196 4.53076 9.56975 4.62002 9.65901C4.70928 9.74827 4.75943 9.86933 4.75943 9.99557V10.4715H5.23539C5.36163 10.4715 5.48269 10.5217 5.57195 10.6109C5.66121 10.7002 5.71135 10.8213 5.71135 10.9475V11.4235H6.18732C6.31355 11.4235 6.43461 11.4736 6.52387 11.5629C6.61313 11.6521 6.66328 11.7732 6.66328 11.8994V12.0965L12.8508 5.90896ZM5.74182 13.0179C5.72179 12.9647 5.71147 12.9082 5.71135 12.8513V12.3754H5.23539C5.10916 12.3754 4.9881 12.3252 4.89884 12.236C4.80958 12.1467 4.75943 12.0256 4.75943 11.8994V11.4235H4.28347C4.15724 11.4235 4.03617 11.3733 3.94691 11.284C3.85765 11.1948 3.80751 11.0737 3.80751 10.9475V10.4715H3.33155C3.20531 10.4715 3.08425 10.4214 2.99499 10.3321C2.90573 10.2429 2.85558 10.1218 2.85558 9.99557V9.5196H2.37962C2.32272 9.51949 2.2663 9.50917 2.21304 9.48914L2.04264 9.65859C1.99728 9.70426 1.96166 9.75867 1.93793 9.81851L0.0340846 14.5781C-0.00053745 14.6646 -0.0090129 14.7594 0.009709 14.8506C0.0284309 14.9419 0.0735268 15.0257 0.139406 15.0916C0.205285 15.1574 0.289051 15.2025 0.380318 15.2212C0.471584 15.24 0.566339 15.2315 0.652835 15.1969L5.41245 13.293C5.47229 13.2693 5.52669 13.2337 5.57237 13.1883L5.74182 13.0179Z"
                    fill="#F3F3F3" />
            </svg>
        </button>
        <svg ref="mapSvg" class="map-svg" :viewBox="`0 0 ${width} ${height}`" preserveAspectRatio="xMidYMid meet">
            <g ref="mapGroup"></g>
            <g ref="dataGroup"></g>
        </svg>
    </div>
</template>

<style scoped>
.map-container {
    position: relative;
    width: 100%;
    height: 100%;
}

.map-container.is-edit {
    border: 1px dashed #808080;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.15);
}

.map-svg {
    /* width: 100%; */
    height: 100%;
}

.chart-edit-btn {
    position: absolute;
    bottom: 10%;
    right: -10px;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: #010080;
    color: #F3F3F3;
    border: none;
    place-items: center;
    cursor: pointer;
    box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.40);
    z-index: 5;
    pointer-events: auto !important;
}


.chart-edit-btn:focus {
    outline: none;
}

.chart-edit-btn svg {
    display: block;
}
</style>