import { computed, ref, unref } from 'vue';

export function useHotspotFocus(sceneRef, spots, options = {}) {
    const zoom = options.zoom ?? 2.2;
    const panelRatio = options.panelRatio ?? 0.4;

    const activeKey = ref(null);
    const sceneTransform = ref('none');

    const activeSpot = computed(() => {
        return unref(spots).find((spot) => spot.key === activeKey.value) ?? null;
    });

    const sceneStyle = computed(() => ({
        transform: sceneTransform.value,
    }));

    function focusSpot(spot, element) {
        const scene = sceneRef.value;

        if (!scene || !element) {
            return;
        }

        if (activeKey.value === spot.key) {
            resetFocus();
            return;
        }

        const sceneWidth = scene.offsetWidth;
        const sceneHeight = scene.offsetHeight;

        const hotspotCenterX = element.offsetLeft + element.offsetWidth / 2;
        const hotspotCenterY = element.offsetTop + element.offsetHeight / 2;

        const visibleSceneWidth = sceneWidth * (1 - panelRatio);

        const targetX = visibleSceneWidth / 2;
        const targetY = sceneHeight / 2;

        const minTranslateX = -(zoom - 1) * sceneWidth;
        const minTranslateY = -(zoom - 1) * sceneHeight;

        const translateX = clamp(
            targetX - zoom * hotspotCenterX,
            minTranslateX,
            0,
        );

        const translateY = clamp(
            targetY - zoom * hotspotCenterY,
            minTranslateY,
            0,
        );

        sceneTransform.value = `
      translate3d(${translateX}px, ${translateY}px, 0)
      scale(${zoom})
    `;

        activeKey.value = spot.key;
    }

    function focusSpotByKey(key) {
        const scene = sceneRef.value;
        const spot = unref(spots).find((candidate) => candidate.key === key);

        if (!scene || !spot) {
            return;
        }

        const element = scene.querySelector(`[data-spot-key="${key}"]`);

        if (!element) {
            return;
        }

        focusSpot(spot, element);
    }

    function resetFocus() {
        activeKey.value = null;
        sceneTransform.value = 'none';
    }

    return {
        activeKey,
        activeSpot,
        sceneStyle,
        focusSpot,
        focusSpotByKey,
        resetFocus,
    };
}

function clamp(value, min, max) {
    return Math.min(max, Math.max(min, value));
}