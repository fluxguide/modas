<script setup>
import { ref, toRef } from 'vue';
import IntroScreen from '@components/Story4/IntroScreen.vue';
import SideMenu from '@src/components/SideMenu.vue';
import { useColumnLabels } from '@composables/useColumnLabels.js';

const props = defineProps({
    data: { type: Array, default: () => [] },
    mode: { type: String, default: 'view' },
    columnLabelMap: { type: Object, default: () => ({}) },
    categoryColours: { type: Object, default: () => [] },
});

const activeMode = ref('view');
const isPresenting = ref(false);
const background = ref({ type: 'texture', tint: 'rgba(255, 255, 255, 0)', opacity: 0, image: null });

const { col } = useColumnLabels(toRef(props, "columnLabelMap"));

const handleModeChange = (newMode) => {
    if (newMode === "presenter") {
        activeMode.value = "view";
        const storyContainer = document.querySelector('.story4-app');
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
</script>

<template>
    <div class="story4-app">
        <SideMenu v-if="!isPresenting" :active-mode="activeMode" :background="background" :allow-image-upload="true"
            @mode-change="handleModeChange" @update:background="val => background = val" />
        <button v-if="isPresenting" class="exit-presenter" @click="exitPresenter">Präsentationsansicht beenden</button>
        <IntroScreen :data="props.data" :background="background" :active-mode="activeMode" />
    </div>
</template>

<style scoped>
.story4-app {
    width: 100%;
    height: 100%;
}

.story4-app:fullscreen {
    background: var(--bg-img) top / cover no-repeat;
}

.story4-app:fullscreen::backdrop {
    background: var(--bg-img) top / cover no-repeat;
}

.exit-presenter {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 1001;
    padding: 10px 20px;
    font-size: 16px;
    background-color: #010080;
    color: #fff !important;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 1px 1px 4px 0 rgba(0, 0, 0, 0.40);
    font-style: normal;
    font-weight: 500;
    line-height: normal;
}
</style>