<script setup>
import { isMobile } from '@src/composables/utils.js';
defineProps({
    text: String,
    color: String,
    fontSize: String,
    position: Number,
    spacingFactor: {
        type: Number,
        default: 0
    }
});
</script>

<template>
    <div v-if="isMobile()" class="label-item" :style="{
        left: (spacingFactor * 35) + 'vw'
    }">
        <span class="label-text" :style="{
            color: color,
            fontSize: '14px'
        }">{{ text }}</span>
    </div>
    <div v-else class="label-item" :style="{ bottom: position + 'vh' }">
        <span class="label-text" :style="{
            color: color,
            fontSize: fontSize
        }">{{ text }}</span>
    </div>
</template>

<style scoped>
.label-item {
    position: absolute;
    display: flex;
    align-items: center;
    transform: translateY(60%);
}

.label-text {
    font-weight: 600;
    text-align: left;
    width: 100%;
}

@media (max-width: 768px) {
    .label-item {
        transform: none;
        position: absolute;
        width: 100%;
        text-align: center;
    }

    .label-text {
        width: 20%;
    }
}
</style>