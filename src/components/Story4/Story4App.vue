<script setup>
import IntroScreen from '@components/Story4/IntroScreen.vue';

const props = defineProps({
    data: { type: Array, default: () => [] },
    mode: { type: String, default: 'view' },
    columnLabelMap: { type: Object, default: () => ({}) },
    categoryColours: { type: Object, default: () => [] },
});
</script>

<template>
    <div class="story4-app">
        <IntroScreen :data="props.data" />
    </div>
</template>

<style scoped>
.story4-app {
    width: 100%;
    height: 100%;
}
</style>