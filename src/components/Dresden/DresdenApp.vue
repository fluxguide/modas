<script setup>
import { computed, onBeforeUnmount, onMounted, onUnmounted, reactive, ref, watch, nextTick } from 'vue'
import { Streamlit } from 'streamlit-component-lib';
import { loadData, getCategoryMetrics, getCategoryName, getDistrictName } from '@composables/Dresden/useDataProcessing.js'
import { useTranslations } from '@composables/Dresden/useTranslations.js'
import {
    sectionOne,
    sectionTwo,
    othersAcceptanceInfo,
    conclusionSummaryInfo,
    conclusionTransportUsage,
    safetyDetailsStory,
    storyScenes,
    orderedStoryScenes,
    conclusionStory,
    endStory
} from '../../../data/storyData.js'
import ConclusionTransportUsage from '@components/Dresden/ConclusionTransportUsage.vue'
import DresdenMap from '@components/Dresden/DresdenMap.vue'
import SpeechBubbleContent from '@components/Dresden/SpeechBubbleContent.vue'
import StoryInfoBox from '@components/Dresden/StoryInfoBox.vue'
import TransportationOptionCard from '@components/Dresden/TransportationOptionCard.vue'
import EditableTextField from '@src/components/EditableTextField.vue';
import SideMenu from '@src/components/SideMenu.vue';

import bikeImage from '@img/Dresden/bike.png'
import busImage from '@img/Dresden/bus.png'
import carImage from '@img/Dresden/car.png'
import endCarImage from '@img/Dresden/end-car.png'
import peopleWalkingImage from '@img/Dresden/people-walking.png'
import riderImage from '@img/Dresden/rider.png'
import tree1Image from '@img/Dresden/tree1.png'
import tree2Image from '@img/Dresden/tree2.png'
import tree3Image from '@img/Dresden/tree3.png'
import tree4Image from '@img/Dresden/tree4.png'
import tree5Image from '@img/Dresden/tree5.png'
import tramImage from '@img/Dresden/tram.png'
import manBikeImage from '@img/Dresden/man-bike.svg'
import manCarImage from '@img/Dresden/man-car.svg'
import manTramImage from '@img/Dresden/man-tram.svg'
import manImage from '@img/Dresden/man.png'
import manWalkImage from '@img/Dresden/man-walk.svg'
import walkImage from '@img/Dresden/walk.png'
import womanBikeImage from '@img/Dresden/woman-bike.svg'
import womanCarImage from '@img/Dresden/woman-car.svg'
import womanTramImage from '@img/Dresden/woman-tram.svg'
import womanImage from '@img/Dresden/woman.png'
import womanWalkImage from '@img/Dresden/woman-walk.svg'
import boyBikeImage from '@img/Dresden/boy-bike.svg'
import boyCarImage from '@img/Dresden/boy-car.svg'
import boyTramImage from '@img/Dresden/boy-tram.svg'
import boyImage from '@img/Dresden/boy.png'
import boyWalkImage from '@img/Dresden/boy-walk.svg'
import arrowIcon from '@img/Dresden/arrow.svg'

const props = defineProps({
    data: { type: Array, default: () => [] },
    mode: { type: String, default: 'view' },
    columnLabelMap: { type: Object, default: () => ({}) },
    categoryColours: { type: Object, default: () => ({}) },
    selectedCity: { type: String, default: 'Dresden' },
});

const scrollingSection = ref(null)
const activeStorySectionId = ref('')
const storySectionVisibility = reactive({})
const storySectionIntersecting = reactive({})
const storySectionSide = reactive({})
const fullyVisibleItems = reactive({})
let sectionScrollLockTimeout = null
let storySectionObserver = null
let fullyVisibleItemObserver = null
const { getTranslation } = useTranslations()

const hasSelectedDistrict = ref(false)
const activeMode = ref('view');
const isPresenting = ref(false);
const editModeActive = ref(true);
const bgTintColor = ref('rgba(255, 255, 255, 0)')
const bgTintOpacity = ref(0.3)

const openEditor = (chartNumber) => {
    Streamlit.setComponentValue({ action: "open_data_editor", chartNumber });
};

const dresdenBackground = computed(() => ({
    type: 'texture',
    tint: bgTintColor.value,
    opacity: bgTintOpacity.value,
}))

const headers = ref({
    section1: getTranslation('intro_title'),
    section2: getTranslation('choose_character_title'),
    section3: getTranslation('choose_city_title'),
    section4: getTranslation('choose_transportation_title'),
})

const texts = ref({
    section1: getTranslation('intro_subtitle_line_1'),
})

const treeImages = {
    tree1: tree1Image,
    tree2: tree2Image,
    tree3: tree3Image,
    tree4: tree4Image,
    tree5: tree5Image,
}

const conclusionImages = {
    tram: tramImage,
    car: carImage,
    bike: bikeImage,
    'end-car': endCarImage,
    'people-walking': peopleWalkingImage,
    rider: riderImage,
}

const storyCharacterTransportationImages = {
    man: {
        bike: manBikeImage,
        car: manCarImage,
        bus: manTramImage,
        walk: manWalkImage,
    },
    woman: {
        bike: womanBikeImage,
        car: womanCarImage,
        bus: womanTramImage,
        walk: womanWalkImage,
    },
    boy: {
        bike: boyBikeImage,
        car: boyCarImage,
        bus: boyTramImage,
        walk: boyWalkImage,
    },
}

const scrollingSetupOptions = {
    characters: [
        {
            id: 'man',
            labelKey: 'character_man',
            image: manImage,
        },
        {
            id: 'woman',
            labelKey: 'character_woman',
            image: womanImage,
        },
        {
            id: 'boy',
            labelKey: 'character_boy',
            image: boyImage,
        },
    ],
    cityParts: Array.from({ length: 17 }, (_, index) => {
        const number = index + 1

        return {
            id: `district-${number}`,
            label: String(number),
            number,
        }
    }),
    transportation: [
        {
            id: 'bike',
            labelKey: 'transportation_bike',
            image: bikeImage,
        },
        {
            id: 'car',
            labelKey: 'transportation_car',
            image: carImage,
        },
        {
            id: 'bus',
            labelKey: 'transportation_bus',
            image: busImage,
        },
        {
            id: 'walk',
            labelKey: 'transportation_walk',
            image: walkImage,
        },
    ],
}

const transportationCards = computed(() => {
    const characterId = selectedScrollingSetup.characterId
    const perCharacter = storyCharacterTransportationImages[characterId] ?? {}

    return [
        { id: 'bike', labelKey: 'transportation_bike', image: perCharacter.bike ?? bikeImage },
        { id: 'car', labelKey: 'transportation_car', image: perCharacter.car ?? carImage },
        { id: 'bus', labelKey: 'transportation_bus', image: perCharacter.bus ?? busImage },
        { id: 'walk', labelKey: 'transportation_walk', image: perCharacter.walk ?? walkImage },
    ]
})

const selectedScrollingSetup = reactive({
    characterId: scrollingSetupOptions.characters[0].id,
    cityPartId: scrollingSetupOptions.cityParts[0].id,
    transportationId: scrollingSetupOptions.transportation[0].id,
})

const activeScrollingSetup = computed(() => ({
    character: scrollingSetupOptions.characters.find(
        ({ id }) => id === selectedScrollingSetup.characterId,
    ),
    cityPart: scrollingSetupOptions.cityParts.find(
        ({ id }) => id === selectedScrollingSetup.cityPartId,
    ),
    transportation: scrollingSetupOptions.transportation.find(
        ({ id }) => id === selectedScrollingSetup.transportationId,
    ),
}))

const activeStoryCharacterTransportationImage = computed(() => {
    const characterImages =
        storyCharacterTransportationImages[selectedScrollingSetup.characterId]

    return characterImages?.[selectedScrollingSetup.transportationId] ?? null
})

const parsedData = computed(() =>
    props.data?.length ? loadData(props.data) : null
)

const activeDistrictNum = computed(() => {
    const match = selectedScrollingSetup.cityPartId.match(/\d+/)
    return match ? Number(match[0]) : null
})

const activeDistrictName = computed(() => {
    if (!hasSelectedDistrict.value) return '';
    if (!parsedData.value || activeDistrictNum.value == null) return '';
    return getDistrictName(parsedData.value, activeDistrictNum.value);
});

function resolveStorySceneMetrics(scene) {
    if (!parsedData.value) return {};

    const scenePosition = orderedStoryScenes.indexOf(scene);
    if (scenePosition === -1) return {};

    const categoryIndex = scenePosition + 1;
    const slots = getCategoryMetrics(
        parsedData.value,
        categoryIndex,
        selectedScrollingSetup.transportationId,
        activeDistrictNum.value,
    );
    const transport = selectedScrollingSetup.transportationId;
    const cats = parsedData.value.categoryOrderByTransport[transport] ?? [];
    const category = cats[categoryIndex];
    const labels = parsedData.value.measurementOrderByCategory[category] ?? [];

    const labelsBySlot = {};
    labels.forEach((label, i) => {
        labelsBySlot[`slot_${i}`] = label;
    });

    return {
        ...slots,
        total: Object.values(slots).reduce((sum, v) => sum + v, 0),
        labels: labelsBySlot,
    };
}

const categoryCount = computed(() => {
    if (!parsedData.value) return 0;
    const transport = selectedScrollingSetup.transportationId;
    const cats = parsedData.value.categoryOrderByTransport[transport] ?? [];
    return Math.max(0, cats.length - 1);
});

const titleOverrides = ref({})

function titleOverrideKey(scene) {
    const pos = orderedStoryScenes.indexOf(scene);
    return `${selectedScrollingSetup.transportationId}:${pos}`;
}

function resolveSceneCategoryName(scene) {
    if (scene?.isStatic) return '';

    const key = titleOverrideKey(scene);
    if (titleOverrides.value[key] != null) return titleOverrides.value[key];   // edited wins

    if (!parsedData.value) return '';
    const scenePosition = orderedStoryScenes.indexOf(scene);
    if (scenePosition === -1) return '';
    return getCategoryName(
        parsedData.value,
        scenePosition + 1,
        selectedScrollingSetup.transportationId,
    );
}

function setSceneTitle(scene, val) {
    titleOverrides.value = {
        ...titleOverrides.value,
        [titleOverrideKey(scene)]: val,
    };
}

const defaultSlotColours = [
    'var(--blue)',
    'var(--mint)',
    'var(--yellow)',
    'var(--orange-soft)',
    'var(--orange-light)',
    'var(--taupe-light)',
]

function slotColour(chartNumber, slotIndex) {
    const slotColours = props.categoryColours?.[chartNumber] ?? []
    return slotColours[slotIndex] || defaultSlotColours[slotIndex]
}

function paletteFor(chartNumber) {
    return [0, 1, 2, 3, 4, 5].map(i => slotColour(chartNumber, i))
}

function buildTowerSegments(metrics, chartNumber) {
    const colorBySlot = {
        slot_0: slotColour(chartNumber, 0),
        slot_1: slotColour(chartNumber, 1),
        slot_2: slotColour(chartNumber, 2),
        slot_3: slotColour(chartNumber, 3),
        slot_4: slotColour(chartNumber, 4),
        slot_5: slotColour(chartNumber, 5),
    }

    return Object.keys(metrics)
        .filter(k => /^slot_\d+$/.test(k))
        .sort((a, b) => Number(a.split('_')[1]) - Number(b.split('_')[1]))
        .slice(0, 6)
        .map(key => ({
            key,
            value: metrics[key] ?? 0,
            height: `${metrics[key] ?? 0}%`,
            color: colorBySlot[key],
            showLabel: (metrics[key] ?? 0) >= 5,
        }))
        .filter(seg => seg.value > 0);
}

const accessibilityHappinessMetrics = computed(() =>
    resolveStorySceneMetrics(sectionOne),
)

const accessibilityRoadMetrics = computed(() =>
    resolveStorySceneMetrics(sectionTwo),
)

const accessibilityHappinessTowerSegments = computed(() =>
    buildTowerSegments(accessibilityHappinessMetrics.value, 1),
)

const accessibilityRoadTowerSegments = computed(() =>
    buildTowerSegments(accessibilityRoadMetrics.value, 2),
)

const safetyDetailsMetrics = computed(() =>
    resolveStorySceneMetrics(safetyDetailsStory),
)

const safetyTreeItems = computed(() => {
    const items = safetyDetailsStory.treeItems
        .map((item) => ({
            ...item,
            image: treeImages[item.imageKey],
            value: safetyDetailsMetrics.value[item.metricKey] ?? 0,
            color: slotColour(3, Number(item.metricKey.split('_')[1])),
        }))
        .filter((item) => item.value > 0);

    if (!items.length) return [];

    const maxValue = Math.max(...items.map(i => i.value));
    const MIN_HEIGHT = 10;   // % of the trees-wrapper height — smallest tree
    const MAX_HEIGHT = 100;   // largest tree

    return items.map(item => ({
        ...item,
        height: MIN_HEIGHT + item.value,
    }));
});

const othersAcceptanceMetrics = computed(() =>
    resolveStorySceneMetrics(othersAcceptanceInfo),
)

const conclusionSummaryMetrics = computed(() =>
    resolveStorySceneMetrics(conclusionSummaryInfo),
)

const conclusionTransportItems = computed(() =>
    conclusionTransportUsage.map((item) => ({
        ...item,
        image: conclusionImages[item.assetKey ?? item.imageKey],
        alt: getTranslation(item.labelKey),
    })),
)

const activeStoryScene = computed(
    () => storyScenes[activeStorySectionId.value] ?? null,
)

const activeStorySceneMetrics = computed(() =>
    resolveStorySceneMetrics(activeStoryScene.value),
)

const activeStoryChartNumber = computed(() => {
    if (activeStoryScene.value === sectionOne) return 1
    if (activeStoryScene.value === sectionTwo) return 2
    return null
})

const activeStorySceneColours = computed(() => paletteFor(activeStoryChartNumber.value))

const activeStorySceneTitleParams = computed(() => ({
    transportGroup: getTranslation(
        `transport_group_${selectedScrollingSetup.transportationId}`,
    ),
    transportMode: getTranslation(
        `transport_mode_${selectedScrollingSetup.transportationId}`,
    ),
    transportContext: getTranslation(
        `transport_context_${selectedScrollingSetup.transportationId}`,
    ),
    transportWithArticle: getTranslation(
        `transport_with_article_${selectedScrollingSetup.transportationId}`,
    ),
}))

const activeStoryCharacterTransportationAlt = computed(() => {
    const characterLabel = activeScrollingSetup.value.character?.labelKey
        ? getTranslation(activeScrollingSetup.value.character.labelKey)
        : ''
    const transportationLabel = activeScrollingSetup.value.transportation?.labelKey
        ? getTranslation(activeScrollingSetup.value.transportation.labelKey)
        : ''

    return getTranslation('story_character_transport_alt', {
        character: characterLabel,
        transportation: transportationLabel,
    })
})

const visibleStorySectionIds = computed(() =>
    Object.entries(storySectionIntersecting)
        .filter(([, isIntersecting]) => isIntersecting)
        .map(([sectionId]) => sectionId),
)

const hasVisibleStorySection = computed(
    () => visibleStorySectionIds.value.length > 0,
)

const activeStoryVisibilityBucket = computed(
    () => storySectionVisibility[activeStorySectionId.value] ?? 0,
)

const hasActiveStorySection = computed(
    () => activeStoryVisibilityBucket.value >= 50 && Boolean(activeStorySectionId.value),
)

const activeStorySectionSide = computed(
    () => storySectionSide[activeStorySectionId.value] ?? 'center',
)

function normalizeWheelDelta(event) {
    let delta = event.deltaY || event.deltaX

    if (delta === 0) {
        return 0
    }

    if (event.deltaMode === 1) {
        delta *= 16
    } else if (event.deltaMode === 2) {
        delta *= window.innerWidth
    }

    return delta
}

function handleSectionWheel(event) {
    const element = scrollingSection.value

    if (!element || element.scrollWidth <= element.clientWidth) {
        return
    }

    const delta = normalizeWheelDelta(event)

    if (delta === 0) {
        return
    }

    event.preventDefault()

    if (sectionScrollLockTimeout) {
        return
    }

    element.scrollBy({
        left: Math.sign(delta) * element.clientWidth,
        behavior: 'smooth',
    })

    sectionScrollLockTimeout = window.setTimeout(() => {
        sectionScrollLockTimeout = null
    }, 450)
}

function getStorySectionVisibilityBucket(ratio) {
    const percentage = Math.floor(ratio * 100)

    if (percentage < 20) {
        return 0
    }

    return Math.min(100, Math.floor(percentage / 10) * 10)
}

function getStorySectionViewportSide(entry) {
    if (!entry.rootBounds) {
        return 'center'
    }

    const sectionWidth = entry.boundingClientRect.width
    const viewportWidth = entry.rootBounds.width

    if (sectionWidth <= viewportWidth * 1.05) {
        return 'center'
    }

    const viewportCenter =
        entry.rootBounds.left + entry.rootBounds.width / 2
    const relativeCenter =
        (viewportCenter - entry.boundingClientRect.left) / sectionWidth

    if (relativeCenter <= 0.34) {
        return 'left'
    }

    if (relativeCenter >= 0.66) {
        return 'right'
    }

    return 'center'
}

function getStorySectionClasses(sectionId) {
    const visibilityBucket = storySectionVisibility[sectionId] ?? 0
    const isActiveSection =
        activeStorySectionId.value === sectionId && visibilityBucket >= 50
    const sectionSide = storySectionSide[sectionId] ?? 'center'

    return {
        'story-section--active': isActiveSection,
        [`active-${visibilityBucket}`]: visibilityBucket >= 20,
        [`active-side-${sectionSide}`]: isActiveSection,
    }
}

function getCharacterStateClasses() {
    const activeSection = activeStorySectionId.value
    const visibilityBucket = activeStoryVisibilityBucket.value
    const transportationId = selectedScrollingSetup.transportationId

    return {
        [`character-wrapper--${activeSection}`]:
            hasActiveStorySection.value && Boolean(activeSection),
        [`character-wrapper--transportation-${transportationId}`]:
            hasActiveStorySection.value && Boolean(transportationId),
        [`active-${visibilityBucket}`]:
            hasActiveStorySection.value && visibilityBucket >= 20,
        [`active-side-${activeStorySectionSide.value}`]:
            hasActiveStorySection.value,
    }
}

function getScrollingSectionStateClasses() {
    const activeSection = activeStorySectionId.value
    const visibilityBucket = activeStoryVisibilityBucket.value

    return {
        [`scrollying-section--active-${activeSection}`]:
            hasActiveStorySection.value && Boolean(activeSection),
        [`active-${visibilityBucket}`]:
            hasActiveStorySection.value && visibilityBucket >= 20,
        [`active-side-${activeStorySectionSide.value}`]:
            hasActiveStorySection.value,
    }
}

function getFullyVisibleItemClasses(itemId) {
    return {
        'is-fully-in-view': Boolean(fullyVisibleItems[itemId]),
    }
}


function scrollToCharacterSection() {
    const container = scrollingSection.value
    const targetSection = container?.querySelector('.choose-character-section')

    if (!container || !targetSection) {
        return
    }

    const previousScrollBehavior = container.style.scrollBehavior

    container.style.scrollBehavior = 'auto'
    container.scrollLeft = targetSection.offsetLeft

    requestAnimationFrame(() => {
        container.style.scrollBehavior = previousScrollBehavior
    })
}

const SCROLL_STORAGE_KEY = 'dresden-story-scroll-left'
const SELECTION_STORAGE_KEY = 'dresden-story-selection'

// On a Streamlit rerun this component remounts. The 'scroll' listener is attached
// immediately, so the initial layout (scrollLeft === 0) would otherwise overwrite
// the saved position before we get a chance to restore it. Gate writes until the
// restore pass has finished.
let hasRestoredScroll = false

function persistScrollPosition() {
    const container = scrollingSection.value

    if (!container || !hasRestoredScroll) {
        return
    }

    try {
        sessionStorage.setItem(SCROLL_STORAGE_KEY, String(container.scrollLeft))
    } catch (error) {
        // sessionStorage may be unavailable (e.g. blocked third-party storage)
    }
}

function restoreScrollPosition() {
    const container = scrollingSection.value

    if (!container) {
        hasRestoredScroll = true
        return
    }

    let saved = null

    try {
        saved = sessionStorage.getItem(SCROLL_STORAGE_KEY)
    } catch (error) {
        hasRestoredScroll = true
        return
    }

    const left = saved === null ? NaN : Number(saved)

    if (Number.isNaN(left) || left <= 0) {
        hasRestoredScroll = true
        return
    }

    // A data edit triggers a multi-stage re-render (chart redraw + the categoryCount
    // watcher re-running observers on nextTick), and a later stage can reset the
    // scroll back to 0 *after* a one-shot restore. So keep re-asserting the position
    // until it has held steady for several consecutive frames, then re-enable
    // persistence. This also covers the sections/images still laying out on mount.
    let attempts = 0
    let stableFrames = 0

    const tryRestore = () => {
        const c = scrollingSection.value

        if (!c) {
            hasRestoredScroll = true
            return
        }

        if (Math.abs(c.scrollLeft - left) > 2) {
            const previousScrollBehavior = c.style.scrollBehavior
            c.style.scrollBehavior = 'auto'
            c.scrollLeft = left
            c.style.scrollBehavior = previousScrollBehavior
            stableFrames = 0
        } else {
            stableFrames += 1
        }

        attempts += 1

        if (stableFrames < 6 && attempts < 150) {
            requestAnimationFrame(tryRestore)
        } else {
            hasRestoredScroll = true
        }
    }

    tryRestore()
}

function persistSelection() {
    try {
        sessionStorage.setItem(
            SELECTION_STORAGE_KEY,
            JSON.stringify({
                characterId: selectedScrollingSetup.characterId,
                cityPartId: selectedScrollingSetup.cityPartId,
                transportationId: selectedScrollingSetup.transportationId,
                hasSelectedDistrict: hasSelectedDistrict.value,
            }),
        )
    } catch (error) {
        // sessionStorage may be unavailable
    }
}

function restoreSelection() {
    let saved = null

    try {
        saved = sessionStorage.getItem(SELECTION_STORAGE_KEY)
    } catch (error) {
        return
    }

    if (!saved) {
        return
    }

    try {
        const state = JSON.parse(saved)

        if (state.characterId) {
            selectedScrollingSetup.characterId = state.characterId
        }
        if (state.cityPartId) {
            selectedScrollingSetup.cityPartId = state.cityPartId
        }
        if (state.transportationId) {
            selectedScrollingSetup.transportationId = state.transportationId
        }
        if (typeof state.hasSelectedDistrict === 'boolean') {
            hasSelectedDistrict.value = state.hasSelectedDistrict
        }
    } catch (error) {
        // ignore malformed snapshots
    }
}

function observeStorySections() {
    if (!scrollingSection.value) {
        return
    }

    const visibleRatios = new Map()

    storySectionObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                const sectionId = entry.target.dataset.storySection

                if (!sectionId) {
                    return
                }

                storySectionIntersecting[sectionId] = entry.isIntersecting
                storySectionVisibility[sectionId] = getStorySectionVisibilityBucket(
                    entry.intersectionRatio,
                )
                storySectionSide[sectionId] = getStorySectionViewportSide(entry)

                if (entry.isIntersecting) {
                    visibleRatios.set(sectionId, entry.intersectionRatio)
                    return
                }

                visibleRatios.delete(sectionId)
            })

            let nextActiveSectionId = activeStorySectionId.value
            let highestRatio = 0

            visibleRatios.forEach((ratio, sectionId) => {
                if (ratio > highestRatio) {
                    highestRatio = ratio
                    nextActiveSectionId = sectionId
                }
            })

            if (highestRatio >= 0.5) {
                activeStorySectionId.value = nextActiveSectionId
                return
            }

            activeStorySectionId.value = ''
        },
        {
            root: scrollingSection.value,
            threshold: [0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
        },
    )

    scrollingSection.value
        .querySelectorAll(':scope > section[data-story-section]')
        .forEach((section) => {
            storySectionVisibility[section.dataset.storySection] = 0
            storySectionIntersecting[section.dataset.storySection] = false
            storySectionSide[section.dataset.storySection] = 'center'
            storySectionObserver?.observe(section)
        })
}

function observeFullyVisibleItems() {
    if (!scrollingSection.value) {
        return
    }

    fullyVisibleItemObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                const itemId = entry.target.dataset.fullVisibilityItem

                if (!itemId) {
                    return
                }

                fullyVisibleItems[itemId] = entry.intersectionRatio >= 0.999
            })
        },
        {
            root: scrollingSection.value,
            threshold: [0, 1],
        },
    )

    scrollingSection.value
        .querySelectorAll('[data-full-visibility-item]')
        .forEach((element) => {
            const itemId = element.dataset.fullVisibilityItem

            if (!itemId) {
                return
            }

            fullyVisibleItems[itemId] = false
            fullyVisibleItemObserver?.observe(element)
        })
}

const handleModeChange = (newMode) => {
    if (newMode === "presenter") {
        activeMode.value = "view";
        const storyContainer = document.querySelector('.dresden-app');
        if (storyContainer?.requestFullscreen) {
            storyContainer.requestFullscreen();
            isPresenting.value = true;
        }
    } else {
        activeMode.value = newMode;
    }
};

const exitPresenter = () => {
    if (document.exitFullscreen) {
        document.exitFullscreen();
    }
    isPresenting.value = false;
    activeMode.value = "view";
};

watch(categoryCount, async () => {
    await nextTick();
    storySectionObserver?.disconnect();
    storySectionObserver = null;
    observeStorySections();
});

watch(() => selectedScrollingSetup.cityPartId, () => {
    hasSelectedDistrict.value = true;
})

// Persist the story selections so they survive the remount caused by a Streamlit
// rerun (e.g. after editing chart data or picking a map city).
watch(
    () => [
        selectedScrollingSetup.characterId,
        selectedScrollingSetup.cityPartId,
        selectedScrollingSetup.transportationId,
        hasSelectedDistrict.value,
    ],
    persistSelection,
)

// A Streamlit rerun does NOT remount this component (the Vue app persists and only
// receives new args via App.vue's RENDER_EVENT). Replacing the data/colours props
// re-renders the story and resets the horizontal scroll to the start, but onMounted
// never fires again to fix it. So re-apply the saved scroll position whenever the
// Streamlit args change. `flush: 'pre'` lets us freeze persistence *before* the DOM
// resets scrollLeft to 0, so that reset can't clobber the saved value.
watch(
    () => [props.data, props.categoryColours, props.selectedCity, props.columnLabelMap],
    () => {
        hasRestoredScroll = false
        nextTick(() => requestAnimationFrame(restoreScrollPosition))
    },
)

watch(
    () => props.selectedCity,
    (city) => {
        console.log('DresdenApp received selectedCity:', city)
    },
    { immediate: true }
)

onMounted(() => {
    // Restore the user's prior selections first so the data-driven sections render
    // the right content before we restore the horizontal scroll position.
    restoreSelection()

    document.addEventListener("fullscreenchange", () => {
        if (!document.fullscreenElement) {
            isPresenting.value = false;
        }
    })

    scrollingSection.value?.addEventListener('wheel', handleSectionWheel, {
        passive: false,
    })

    scrollingSection.value?.addEventListener('scroll', persistScrollPosition, {
        passive: true,
    })

    observeStorySections()
    observeFullyVisibleItems()

    // In release mode (deployed) a Streamlit rerun remounts this component, which
    // resets the horizontal scroll to the start. Restore the last position so the
    // user stays where they were (e.g. after picking a city). No-op on first load.
    nextTick(() => requestAnimationFrame(restoreScrollPosition))
})

onBeforeUnmount(() => {
    if (sectionScrollLockTimeout) {
        window.clearTimeout(sectionScrollLockTimeout)
        sectionScrollLockTimeout = null
    }

    scrollingSection.value?.removeEventListener('wheel', handleSectionWheel)
    scrollingSection.value?.removeEventListener('scroll', persistScrollPosition)
    storySectionObserver?.disconnect()
    storySectionObserver = null
    fullyVisibleItemObserver?.disconnect()
    fullyVisibleItemObserver = null
})

onUnmounted(() => {
    document.removeEventListener("fullscreenchange", () => { });
});
</script>

<template>
    <div class="dresden-app">
    <SideMenu v-if="!isPresenting" :active-mode="activeMode" :background="dresdenBackground"
        @mode-change="handleModeChange"
        @update:background="val => { bgTintColor = val.tint; bgTintOpacity = val.opacity }" />
    <button v-if="isPresenting" class="exit-presenter" @click="exitPresenter">Präsentationsansicht beenden</button>
    <section ref="scrollingSection" class="scrollying-section" :class="getScrollingSectionStateClasses()"
        :style="{ '--bg-tint': bgTintColor, '--bg-tint-opacity': bgTintOpacity }" :data-active-story-section="hasActiveStorySection ? activeStorySectionId : undefined
            " :data-active-story-visibility="hasActiveStorySection ? activeStoryVisibilityBucket : undefined
                " :data-active-story-side="hasActiveStorySection ? activeStorySectionSide : undefined
                    ">
        <section class="intro-section">
            <div class="intro-section__content">
                <h1>
                    <EditableTextField :model-value="headers.section1"
                        @update:model-value="val => headers.section1 = val" :active-mode="activeMode" :rows="1"
                        :width="`75vw`" :font-size="'7vh'" :line-height="1" :padding="'0vh'" :font-weight="'400'"
                        :text-align="'center'" :text-transform="'uppercase'" :letter-spacing="'0.08em'" />
                </h1>
                <h2>
                    <EditableTextField :model-value="texts.section1" @update:model-value="val => texts.section1 = val"
                        :active-mode="activeMode" :rows="5" :width="`80rem`" :font-size="'2.5vw'" :line-height="1.35"
                        :padding="'0vh'" :font-weight="'400'" :text-align="'center'" :text-transform="'uppercase'"
                        :letter-spacing="'0.06em'" />
                </h2>
                <div class="intro-section__cta">
                    <label>{{ getTranslation('intro_cta') }}</label>
                    <img :src="arrowIcon" alt="" aria-hidden="true" class="intro-section__arrow">
                </div>
            </div>
        </section>

        <section class="choose-character-section">
            <div class="selection-section__content">
                <h1>
                    <EditableTextField :model-value="headers.section2"
                        @update:model-value="val => headers.section2 = val" :active-mode="activeMode" :rows="1"
                        :width="`75vw`" :font-size="'7vh'" :line-height="1" :padding="'0vh'" :font-weight="'400'"
                        :text-align="'center'" :text-transform="'uppercase'" :letter-spacing="'0.08em'" />
                </h1>
                <div class="character-grid" role="list" :aria-label="getTranslation('choose_character_aria_label')">
                    <button v-for="character in scrollingSetupOptions.characters" :key="character.id" type="button"
                        class="character-card" :class="{
                            'character-card--active':
                                selectedScrollingSetup.characterId === character.id,
                        }" @click="selectedScrollingSetup.characterId = character.id">
                        <img :src="character.image" :alt="getTranslation(character.labelKey)"
                            class="character-card__image">
                    </button>
                </div>
            </div>
        </section>
        <section class="choose-city-section">
            <div class="selection-section__content">
                <h1>
                    <EditableTextField :model-value="headers.section3"
                        @update:model-value="val => headers.section3 = val" :active-mode="activeMode" :rows="1"
                        :width="`75vw`" :font-size="'7vh'" :line-height="1" :padding="'0vh'" :font-weight="'400'"
                        :text-align="'center'" :text-transform="'uppercase'" :letter-spacing="'0.08em'" />
                </h1>
                <DresdenMap v-model="selectedScrollingSetup.cityPartId" @update:model-value="hasSelectedDistrict = true"
                    class="city-map" :active-mode="activeMode" :selectedCity="selectedCity" />

                <div class="city-selection-character">
                    <div class="city-selection--speech-bubble">
                        <svg class="bubble-bg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 228 106"
                            preserveAspectRatio="none" fill="none">
                            <path
                                d="M20 2.5H193.217C202.882 2.50003 210.717 10.335 210.717 20V63.7695C210.717 67.2709 211.529 70.6944 213.046 73.8252C215.48 78.85 219.522 87.4086 222.363 94.5273C223.708 97.8965 224.73 100.816 225.212 102.852C216.262 100.072 198.578 93.3114 190.977 90.3701C188.362 89.3585 185.593 88.8369 182.785 88.8369H20C10.335 88.8369 2.5 81.0019 2.5 71.3369V20C2.5 10.335 10.335 2.5 20 2.5Z"
                                fill="white" stroke="#456990" stroke-width="5" />
                        </svg>
                        <label>{{ activeDistrictName || getTranslation('choose_city_prompt') }}</label>
                    </div>
                    <img :src="activeScrollingSetup.character?.image"
                        :alt="getTranslation(activeScrollingSetup.character?.labelKey)">
                </div>
            </div>
        </section>
        <section class="choose-transportation-section">
            <div class="selection-section__content">
                <h1>
                    <EditableTextField :model-value="headers.section4"
                        @update:model-value="val => headers.section4 = val" :active-mode="activeMode" :rows="1"
                        :width="`75vw`" :font-size="'6vh'" :line-height="1" :padding="'0vh'" :font-weight="'400'"
                        :text-align="'center'" :text-transform="'uppercase'" :letter-spacing="'0.08em'" />
                </h1>
                <div class="transportation-grid" role="list"
                    :aria-label="getTranslation('choose_transportation_aria_label')">
                    <TransportationOptionCard v-for="(transportation, index) in transportationCards"
                        :key="transportation.id" :option="transportation" :class="index % 2 == 0 ? 'even' : 'odd'"
                        :selected="selectedScrollingSetup.transportationId === transportation.id
                            " @select="
                                selectedScrollingSetup.transportationId = transportation.id
                                " />
                </div>
            </div>
        </section>



        <!-- Character in Story -->
        <div v-if="hasActiveStorySection && activeStoryScene" class="character-wrapper"
            :class="getCharacterStateClasses()">
            <img v-if="activeStoryCharacterTransportationImage" :src="activeStoryCharacterTransportationImage"
                :alt="activeStoryCharacterTransportationAlt" class="story-character-transportation">
            <article class="speech-bubble">
                <svg class="speech-bubble-bottom" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 213 114" fill="none">
                    <path
                        d="M24.3809 108.27C-53.8085 145.629 85.6407 -11.3606 34.3418 -26.0945C-16.957 -40.8284 240.039 -50.5256 210.651 -26.0945C181.262 -1.66349 102.57 70.9105 24.3809 108.27Z"
                        fill="white" />
                </svg>
                <SpeechBubbleContent
                    :title="resolveSceneCategoryName(activeStoryScene) || getTranslation(activeStoryScene.titleKey, activeStorySceneTitleParams)"
                    @update:title="val => setSceneTitle(activeStoryScene, val)" :lines="activeStoryScene.bubble"
                    :metrics="activeStorySceneMetrics" :active-mode="activeMode" :edit-mode-active="editModeActive"
                    :highlight-colours="activeStorySceneColours" />
            </article>
        </div>



        <!-- Story -->
        <section v-if="categoryCount > 0" class="first-section" :class="getStorySectionClasses('section-one')"
            :data-story-active="activeStorySectionId === 'section-one' &&
                activeStoryVisibilityBucket >= 50
                " data-story-section="section-one">
            <div class="building-image-wrapper" :class="{ 'is-edit': activeMode === 'edit' }">
                <button v-if="activeMode === 'edit'" class="chart-edit-btn" @click.stop="openEditor(1)"
                    title="Diagrammdaten bearbeiten" aria-label="Diagrammdaten bearbeiten">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="none">
                        <path
                            d="M12.2358 0.139355C12.1466 0.0501261 12.0255 0 11.8993 0C11.7731 0 11.6521 0.0501261 11.5628 0.139355L9.99501 1.70717L13.5238 5.23595L15.0916 3.66909C15.1359 3.62487 15.1711 3.57235 15.1951 3.51453C15.2191 3.4567 15.2314 3.39471 15.2314 3.3321C15.2314 3.2695 15.2191 3.20751 15.1951 3.14968C15.1711 3.09186 15.1359 3.03934 15.0916 2.99512L12.2358 0.139355ZM12.8508 5.90896L9.322 2.38018L3.1345 8.56768H3.33155C3.45778 8.56768 3.57884 8.61783 3.6681 8.70709C3.75736 8.79635 3.80751 8.91741 3.80751 9.04364V9.5196H4.28347C4.4097 9.5196 4.53076 9.56975 4.62002 9.65901C4.70928 9.74827 4.75943 9.86933 4.75943 9.99557V10.4715H5.23539C5.36163 10.4715 5.48269 10.5217 5.57195 10.6109C5.66121 10.7002 5.71135 10.8213 5.71135 10.9475V11.4235H6.18732C6.31355 11.4235 6.43461 11.4736 6.52387 11.5629C6.61313 11.6521 6.66328 11.7732 6.66328 11.8994V12.0965L12.8508 5.90896ZM5.74182 13.0179C5.72179 12.9647 5.71147 12.9082 5.71135 12.8513V12.3754H5.23539C5.10916 12.3754 4.9881 12.3252 4.89884 12.236C4.80958 12.1467 4.75943 12.0256 4.75943 11.8994V11.4235H4.28347C4.15724 11.4235 4.03617 11.3733 3.94691 11.284C3.85765 11.1948 3.80751 11.0737 3.80751 10.9475V10.4715H3.33155C3.20531 10.4715 3.08425 10.4214 2.99499 10.3321C2.90573 10.2429 2.85558 10.1218 2.85558 9.99557V9.5196H2.37962C2.32272 9.51949 2.2663 9.50917 2.21304 9.48914L2.04264 9.65859C1.99728 9.70426 1.96166 9.75867 1.93793 9.81851L0.0340846 14.5781C-0.00053745 14.6646 -0.0090129 14.7594 0.009709 14.8506C0.0284309 14.9419 0.0735268 15.0257 0.139406 15.0916C0.205285 15.1574 0.289051 15.2025 0.380318 15.2212C0.471584 15.24 0.566339 15.2315 0.652835 15.1969L5.41245 13.293C5.47229 13.2693 5.52669 13.2337 5.57237 13.1883L5.74182 13.0179Z"
                            fill="#F3F3F3" />
                    </svg>
                </button>
                <img src="@img/Dresden/building.png" alt="" class="building-image" />

                <ul class="building-metrics-list">
                    <li v-for="metric in accessibilityHappinessTowerSegments" :key="metric.key"
                        class="building-metrics-list__item" :style="{
                            height: metric.height,
                            backgroundColor: `color-mix(in srgb, ${metric.color} 80%, transparent)`,
                        }">
                        <span v-if="metric.showLabel">{{ metric.value }}%</span>
                    </li>
                </ul>
            </div>
        </section>

        <section v-if="categoryCount > 1" class="second-section" :class="getStorySectionClasses('section-two')"
            :data-story-active="activeStorySectionId === 'section-two' &&
                activeStoryVisibilityBucket >= 50
                " data-story-section="section-two">
            <div class="building-image-wrapper" :class="{ 'is-edit': activeMode === 'edit' }">
                <button v-if="activeMode === 'edit'" class="chart-edit-btn" @click.stop="openEditor(2)"
                    title="Diagrammdaten bearbeiten" aria-label="Diagrammdaten bearbeiten">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="none">
                        <path
                            d="M12.2358 0.139355C12.1466 0.0501261 12.0255 0 11.8993 0C11.7731 0 11.6521 0.0501261 11.5628 0.139355L9.99501 1.70717L13.5238 5.23595L15.0916 3.66909C15.1359 3.62487 15.1711 3.57235 15.1951 3.51453C15.2191 3.4567 15.2314 3.39471 15.2314 3.3321C15.2314 3.2695 15.2191 3.20751 15.1951 3.14968C15.1711 3.09186 15.1359 3.03934 15.0916 2.99512L12.2358 0.139355ZM12.8508 5.90896L9.322 2.38018L3.1345 8.56768H3.33155C3.45778 8.56768 3.57884 8.61783 3.6681 8.70709C3.75736 8.79635 3.80751 8.91741 3.80751 9.04364V9.5196H4.28347C4.4097 9.5196 4.53076 9.56975 4.62002 9.65901C4.70928 9.74827 4.75943 9.86933 4.75943 9.99557V10.4715H5.23539C5.36163 10.4715 5.48269 10.5217 5.57195 10.6109C5.66121 10.7002 5.71135 10.8213 5.71135 10.9475V11.4235H6.18732C6.31355 11.4235 6.43461 11.4736 6.52387 11.5629C6.61313 11.6521 6.66328 11.7732 6.66328 11.8994V12.0965L12.8508 5.90896ZM5.74182 13.0179C5.72179 12.9647 5.71147 12.9082 5.71135 12.8513V12.3754H5.23539C5.10916 12.3754 4.9881 12.3252 4.89884 12.236C4.80958 12.1467 4.75943 12.0256 4.75943 11.8994V11.4235H4.28347C4.15724 11.4235 4.03617 11.3733 3.94691 11.284C3.85765 11.1948 3.80751 11.0737 3.80751 10.9475V10.4715H3.33155C3.20531 10.4715 3.08425 10.4214 2.99499 10.3321C2.90573 10.2429 2.85558 10.1218 2.85558 9.99557V9.5196H2.37962C2.32272 9.51949 2.2663 9.50917 2.21304 9.48914L2.04264 9.65859C1.99728 9.70426 1.96166 9.75867 1.93793 9.81851L0.0340846 14.5781C-0.00053745 14.6646 -0.0090129 14.7594 0.009709 14.8506C0.0284309 14.9419 0.0735268 15.0257 0.139406 15.0916C0.205285 15.1574 0.289051 15.2025 0.380318 15.2212C0.471584 15.24 0.566339 15.2315 0.652835 15.1969L5.41245 13.293C5.47229 13.2693 5.52669 13.2337 5.57237 13.1883L5.74182 13.0179Z"
                            fill="#F3F3F3" />
                    </svg>
                </button> <img src="@img/Dresden/building.png" alt="" class="building-image" />

                <ul class="building-metrics-list">
                    <li v-for="metric in accessibilityRoadTowerSegments" :key="metric.key"
                        class="building-metrics-list__item" :style="{
                            height: metric.height,
                            backgroundColor: `color-mix(in srgb, ${metric.color} 80%, transparent)`,
                        }">
                        <span v-if="metric.showLabel">{{ metric.value }}%</span>
                    </li>
                </ul>
            </div>
        </section>

        <section v-if="categoryCount > 2" class="safety-section" :class="getStorySectionClasses('safety')"
            :data-story-active="activeStorySectionId === 'safety' &&
                activeStoryVisibilityBucket >= 50
                " data-story-section="safety">
            <div class="trees-wrapper">
                <div :class="{ 'is-edit': activeMode === 'edit' }" class="trees-container">
                    <button v-if="activeMode === 'edit'" class="chart-edit-btn" @click.stop="openEditor(3)"
                        title="Diagrammdaten bearbeiten" aria-label="Diagrammdaten bearbeiten">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="none">
                            <path
                                d="M12.2358 0.139355C12.1466 0.0501261 12.0255 0 11.8993 0C11.7731 0 11.6521 0.0501261 11.5628 0.139355L9.99501 1.70717L13.5238 5.23595L15.0916 3.66909C15.1359 3.62487 15.1711 3.57235 15.1951 3.51453C15.2191 3.4567 15.2314 3.39471 15.2314 3.3321C15.2314 3.2695 15.2191 3.20751 15.1951 3.14968C15.1711 3.09186 15.1359 3.03934 15.0916 2.99512L12.2358 0.139355ZM12.8508 5.90896L9.322 2.38018L3.1345 8.56768H3.33155C3.45778 8.56768 3.57884 8.61783 3.6681 8.70709C3.75736 8.79635 3.80751 8.91741 3.80751 9.04364V9.5196H4.28347C4.4097 9.5196 4.53076 9.56975 4.62002 9.65901C4.70928 9.74827 4.75943 9.86933 4.75943 9.99557V10.4715H5.23539C5.36163 10.4715 5.48269 10.5217 5.57195 10.6109C5.66121 10.7002 5.71135 10.8213 5.71135 10.9475V11.4235H6.18732C6.31355 11.4235 6.43461 11.4736 6.52387 11.5629C6.61313 11.6521 6.66328 11.7732 6.66328 11.8994V12.0965L12.8508 5.90896ZM5.74182 13.0179C5.72179 12.9647 5.71147 12.9082 5.71135 12.8513V12.3754H5.23539C5.10916 12.3754 4.9881 12.3252 4.89884 12.236C4.80958 12.1467 4.75943 12.0256 4.75943 11.8994V11.4235H4.28347C4.15724 11.4235 4.03617 11.3733 3.94691 11.284C3.85765 11.1948 3.80751 11.0737 3.80751 10.9475V10.4715H3.33155C3.20531 10.4715 3.08425 10.4214 2.99499 10.3321C2.90573 10.2429 2.85558 10.1218 2.85558 9.99557V9.5196H2.37962C2.32272 9.51949 2.2663 9.50917 2.21304 9.48914L2.04264 9.65859C1.99728 9.70426 1.96166 9.75867 1.93793 9.81851L0.0340846 14.5781C-0.00053745 14.6646 -0.0090129 14.7594 0.009709 14.8506C0.0284309 14.9419 0.0735268 15.0257 0.139406 15.0916C0.205285 15.1574 0.289051 15.2025 0.380318 15.2212C0.471584 15.24 0.566339 15.2315 0.652835 15.1969L5.41245 13.293C5.47229 13.2693 5.52669 13.2337 5.57237 13.1883L5.74182 13.0179Z"
                                fill="#F3F3F3" />
                        </svg>
                    </button>
                    <div v-for="treeItem in safetyTreeItems" :key="treeItem.id" class="tree-wrapper"
                        :class="`tree-wrapper--${treeItem.id}`" :style="{ '--tree-height': treeItem.height + 'vh' }">
                        <img :src="treeItem.image" alt="" class="tree" />
                        <h3 class="tree-value" :style="{ color: treeItem.color }">{{ treeItem.value }}%</h3>
                    </div>
                </div>

                <div class="trees-info white-info-box">
                    <SpeechBubbleContent :title="resolveSceneCategoryName(safetyDetailsStory)"
                        @update:title="val => setSceneTitle(safetyDetailsStory, val)" :lines="safetyDetailsStory.bubble"
                        :metrics="safetyDetailsMetrics" :highlight-colours="paletteFor(3)" />
                </div>
            </div>
        </section>

        <section v-if="categoryCount > 3" class="others-question-section"
            :class="getStorySectionClasses('others-question')" :data-story-active="activeStorySectionId === 'others-question' &&
                activeStoryVisibilityBucket >= 50
                " data-story-section="others-question">
            <img src="@img/Dresden/cloud.png" alt="" class="cloud-image cloud-1" />
            <img src="@img/Dresden/cloud.png" alt="" class="cloud-image cloud-2" />
            <div class="traffic-light-wrapper">
                <img src="@img/Dresden/traffic-light.png" alt="" class="traffic-light" />
            </div>
            <div class="white-info-box cloud-info-box">
                <SpeechBubbleContent :title="resolveSceneCategoryName(othersAcceptanceInfo)"
                    @update:title="val => setSceneTitle(othersAcceptanceInfo, val)" :lines="othersAcceptanceInfo.bubble"
                    :metrics="othersAcceptanceMetrics" />
            </div>
        </section>

        <section class="conclusion-section" :class="getStorySectionClasses('conclusion')" :data-story-active="activeStorySectionId === 'conclusion' &&
            activeStoryVisibilityBucket >= 50
            " data-story-section="conclusion">
            <div class="white-info-box conclusion-summary-box">
                <StoryInfoBox :blocks="conclusionSummaryInfo.blocks" :metrics="conclusionSummaryMetrics" />
            </div>

            <div class="conclusion-transport-list">
                <ConclusionTransportUsage v-for="item in conclusionTransportItems" :key="item.id"
                    class="conclusion-transport-list__item" :class="[
                        `conclusion-transport-list__item--${item.id}`,
                        getFullyVisibleItemClasses(item.id),
                    ]" :image="item.image" :alt="item.alt" :value="item.value" :data-full-visibility-item="item.id"
                    :data-fully-visible="fullyVisibleItems[item.id] ? 'true' : 'false'" />
            </div>
        </section>

        <section class="end-section" :class="getStorySectionClasses('end')" :data-story-active="activeStorySectionId === 'end' &&
            activeStoryVisibilityBucket >= 50
            " data-story-section="end">
            <div class="end-cta-card">
                <h2>{{ getTranslation('end_cta_question') }}</h2>
                <button type="button" class="end-cta-card__button" @click.prevent.stop="scrollToCharacterSection">
                    <span>{{ getTranslation('end_cta_button') }}</span>
                    <img :src="arrowIcon" alt="" aria-hidden="true" class="end-cta-card__arrow">
                </button>
            </div>
        </section>
    </section>
    </div>
</template>


<style>
.scrollying-section {
    position: relative;
    display: flex;
    flex-wrap: nowrap;
    width: 100vw;
    height: 100vh;
    overflow-x: auto;
    overflow-y: hidden;
    overscroll-behavior: contain;
    touch-action: pan-x;
    scroll-snap-type: x mandatory;
    scroll-behavior: smooth;

    background: url('@img/Dresden/bg.jpg') no-repeat;
    background-size: cover;
}

.scrollying-section>* {
    position: relative;
    z-index: 1;
}


.scrollying-section>section {
    flex: 0 0 100vw;
    min-width: 100vw;
    height: 100%;
    scroll-snap-align: start;
    scroll-snap-stop: always;

    display: flex;
    align-items: stretch;
    padding: 5vh 34px;
}

.scrollying-section::before {
    content: '';
    position: fixed;
    inset: 0;
    background-color: var(--bg-tint, transparent);
    opacity: var(--bg-tint-opacity, 0);
    pointer-events: none;
    z-index: 0;
    mix-blend-mode: multiply;
}


.intro-section__content {
    display: flex;
    flex: 1;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    height: 100%;
    text-align: center;
    padding-top: 10vh;
}

/* .intro-section h2 {
    max-width: 64rem;
} */

.intro-section__cta {
    display: inline-flex;
    align-items: center;
    gap: 1rem;
    align-self: flex-end;
}

.intro-section__cta label {
    cursor: default;
}

.intro-section__arrow {
    width: 2.75rem;
    height: auto;
}





.selection-section__content {
    display: flex;
    flex: 1;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    height: 100%;
    text-align: center;
}

.character-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    align-items: end;
    gap: 5vw;
    width: 100%;
    max-width: 70vw;
    padding: 5vh 0;
}

.character-card {
    cursor: pointer;
    display: flex;
    align-items: flex-end;
    justify-content: center;
    filter: drop-shadow(0 5px 15px color-mix(in srgb, var(--green), transparent 100%)) drop-shadow(0 0px 1px color-mix(in srgb, var(--blue-dark), transparent 100%));
    transition:
        transform 0.2s ease,
        filter 0.2s ease;
}

.character-card:hover,
.character-card:focus-visible,
.character-card--active {
    transform: translateY(-0.5rem) scale(1.1);
    filter: drop-shadow(0 5px 15px color-mix(in srgb, var(--green), transparent 0%)) drop-shadow(0 0px 1px color-mix(in srgb, var(--blue-dark), transparent 100%));
}

.character-card--active,
.character-card--active:hover {
    filter: drop-shadow(0 5px 15px color-mix(in srgb, var(--green), transparent 0%)) drop-shadow(0 0px 1px color-mix(in srgb, var(--blue-dark), transparent 0%));
}

.character-card__image {
    width: 100%;
    max-width: 25vw;
    max-height: 60vh;
    object-fit: contain;
}



.choose-city-section .selection-section__content {
    position: relative;
    gap: 8vh;
    justify-content: flex-start;
}

.city-map {
    width: 100%;
    max-height: 60vh;
}

.choose-city-section .selection-section__content .city-selection-character {
    position: absolute;
    bottom: 0px;
    right: 34px;
    height: 30vh;
}

.choose-city-section .selection-section__content .city-selection-character img {
    max-height: 100%;
}

.choose-city-section .selection-section__content .city-selection--speech-bubble {
    position: absolute;
    top: 0;
    left: 0;
    transform: translate3d(-100%, -20%, 0);

    display: inline-block;
    padding: 1.2rem 1.6rem 2rem;
}

.choose-city-section .selection-section__content .city-selection--speech-bubble .bubble-bg {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
}

.choose-city-section .selection-section__content .city-selection--speech-bubble label {
    position: relative;
    z-index: 1;
    display: block;
    font-size: 1.2rem;
    text-align: left;
}




.choose-transportation-section {
    display: flex;
    align-items: stretch;
    justify-content: center;
    padding: 2.875rem 5rem 4rem;
}


.transportation-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 2rem 3rem;
    width: 100%;
    max-width: 64rem;
    padding-bottom: 5vh;
}

.exit-presenter {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 1001;
    padding: 10px 20px;
    font-size: 16px;
    background-color: #010080;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 1px 1px 4px 0 rgba(0, 0, 0, 0.40);
    font-family: 'General Sans';
    font-style: normal;
    font-weight: 500;
    line-height: normal;
}

.dresden-app:fullscreen {
    width: 100vw;
    height: 100vh;
    overflow: hidden;
}
</style>
