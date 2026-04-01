<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
    textContent: String,
    activeMode: String,
    rows: { type: Number, default: 7 },
    width: { type: String, default: '60%' },
    fontSize: { type: String, default: '36px' },
    lineHeight: { type: Number, default: '1.3' },
    topPadding: { type: String, default: '5vh' },
    bottomPadding: { type: String, default: '5vh' },
    textAlign: { type: String, default: 'left' },
    fontWeight: { type: String, default: 'normal' }
});

const emit = defineEmits(['update:textContent']);
const textAreaRef = ref(null);

// Reset scroll to top when leaving edit mode
watch(() => props.activeMode, (newMode) => {
    if (newMode !== 'edit' && textAreaRef.value) {
        const el = textAreaRef.value.$el.querySelector('textarea');
        if (el) el.scrollTop = 0;
    }
});
</script>

<template>
    <v-textarea ref="textAreaRef" :text-content="textContent"
        @update:text-content="val => emit('update:textContent', val)" :readonly="activeMode !== 'edit'" variant="plain"
        hide-details no-resize :rows="rows" class="editable-text-comp"
        :style="{ '--custom-font-size': fontSize, '--custom-width': width, '--rows': rows, '--custom-line-height': lineHeight, '--top-padding': topPadding, '--bottom-padding': bottomPadding, '--custom-text-align': textAlign, '--custom-font-weight': fontWeight }"></v-textarea>
</template>

<style scoped>
.editable-text-comp {
    width: var(--custom-width);
    pointer-events: auto;
}

.editable-text-comp :deep(.v-field) {
    transition: all 0.3s ease;
    border-radius: 12px;
    border: 1px solid transparent;
    padding: 0;
    display: flex;
    align-items: center;
    min-height: calc(var(--rows, 15) * 1.3 * var(--custom-font-size)) !important;
}

.editable-text-comp :deep(textarea) {
    font-size: var(--custom-font-size) !important;
    font-weight: var(--custom-font-weight) !important;
    line-height: var(--custom-line-height) !important;
    width: 100%;
    text-align: var(--custom-text-align);
    height: auto !important;
}

.editable-text-comp:not(.v-input--readonly) :deep(.v-field) {
    background-color: rgba(255, 255, 255, 0.15) !important;
    border: 1px dashed #808080;
}

.editable-text-comp:not(.v-input--readonly) :deep(textarea) {
    overflow-y: auto !important;
    cursor: text !important;
}

.editable-text-comp :deep(.v-input__control) {
    height: fit-content;
    padding-top: var(--top-padding);
    padding-bottom: var(--bottom-padding);
}
</style>
