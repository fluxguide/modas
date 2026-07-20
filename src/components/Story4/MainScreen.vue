<script setup>
import { ref, watch } from 'vue';

import HotspotDetail from '@components/Story4/HotspotDetail.vue';
import HotspotItem from '@components/Story4/HotspotItem.vue';

import { hotspots } from '@data/hotspots.js';
import { useHotspotFocus } from '@composables/Story4/useHotspotFocus.js';

const props = defineProps({
    visibility: {
        type: Boolean,
        default: false,
    },
});

defineEmits(["summary"]);

const sceneRef = ref(null);

const {
    activeKey,
    activeSpot,
    sceneStyle,
    focusSpot,
    focusSpotByKey,
    resetFocus,
} = useHotspotFocus(sceneRef, hotspots, {
    zoom: 2,
    panelRatio: 0.4,
});

function handleSpotSelect(spot, element) {
    focusSpot(spot, element);
}

watch(
    () => props.visibility,
    (visible) => {
        if (!visible) {
            resetFocus();
        }
    },
);
</script>

<template>
    <main v-if="visibility" class="hotspot-scene">
        <div ref="sceneRef" class="hotspot-scene__canvas" :style="sceneStyle">
            <HotspotItem v-for="spot in hotspots" :key="spot.key" :spot="spot" :active="activeKey === spot.key"
                :dimmed="Boolean(activeKey && activeKey !== spot.key)" @select="handleSpotSelect" />
        </div>

        <HotspotDetail :spot="activeSpot" :spots="hotspots" @close="resetFocus" @navigate="focusSpotByKey"
            @summary="$emit('summary')" />
    </main>
</template>

<style scoped lang="less">
.hotspot-scene {
    position: relative;
    width: 100vw;
    height: 100vh;
    margin: 0;
    padding: 0;
    overflow: hidden;
}

.hotspot-scene__canvas {
    position: absolute;
    inset: 0;

    width: 100%;
    height: 100%;

    background: var(--bg-img) top / cover no-repeat;

    transform-origin: 0 0;
    transition: transform 0.6s cubic-bezier(0.25, 1, 0.5, 1);
    will-change: transform;
}

@media (prefers-reduced-motion: reduce) {

    .hotspot-scene__canvas,
    :deep(.detail-panel),
    :deep(.hotspot) {
        transition: none;
    }
}
</style>