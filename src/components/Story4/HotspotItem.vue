<script setup>
import { computed, ref } from 'vue';

const props = defineProps({
    spot: {
        type: Object,
        required: true,
    },
    active: {
        type: Boolean,
        default: false,
    },
    dimmed: {
        type: Boolean,
        default: false,
    },
});

const emit = defineEmits(['select']);

const rootRef = ref(null);

const rootStyle = computed(() => ({
    ...props.spot.position,
    '--spot-color': props.spot.color,
    '--label-margin': props.spot.labelMargin ?? '0 0 10px',
}));

const imageStyle = computed(() => ({
    width: props.spot.imageStyle?.width,
    scale: props.spot.imageStyle?.scale,
    rotate: props.spot.imageStyle?.rotate,
}));

function selectSpot() {
    if (!rootRef.value) {
        return;
    }

    emit('select', props.spot, rootRef.value);
}
</script>

<template>
    <button ref="rootRef" type="button" class="hotspot" :class="{
        'hotspot--active': active,
        'hotspot--dimmed': dimmed,
    }" :style="rootStyle" :data-spot-key="spot.key" :aria-pressed="active" :aria-label="`${spot.label} anzeigen`" @click="selectSpot">
        <span class="hotspot__label">
            {{ spot.label }}
        </span>

        <img v-if="spot.image" class="hotspot__image" :src="spot.image" :alt="spot.label" :style="imageStyle">
    </button>
</template>

<style scoped lang="less">
.hotspot {
    position: absolute;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    margin: 0;
    padding: 0;

    color: inherit;
    font: inherit;
    background: transparent;
    border: 0;
    cursor: pointer;

    transition: opacity 0.4s ease;
}

.hotspot--dimmed {
    opacity: 0.35;
    pointer-events: none;
}

.hotspot--active {
    z-index: 2;
}

.hotspot__label {
    position: relative;
    z-index: 3;

    margin: var(--label-margin);
    padding: 8px 16px;

    color: #fff !important;
    font-size: 27px;
    font-weight: 500;
    line-height: 1;
    white-space: nowrap;

    background: rgba(0, 0, 0, 0.9);
    border: 2px solid var(--spot-color);
    border-radius: 8px;

    &::before {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;

        transform: translateX(-50%);

        border-top: 16px solid var(--spot-color);
        border-right: 16px solid transparent;
        border-left: 16px solid transparent;
    }
}

.hotspot__image {
    display: block;
    height: auto;

    filter:
        drop-shadow(0 0 1rem color-mix(in srgb, var(--spot-color) 70%, transparent)) drop-shadow(0 0 3rem color-mix(in srgb, var(--spot-color) 40%, transparent)) drop-shadow(0 0 5rem color-mix(in srgb, var(--spot-color) 10%, transparent));
}
</style>