<script setup>
import EditableTextField from '@src/components/EditableTextField.vue';
import { ref, watch } from 'vue';

const props = defineProps({
    showLogo: { type: Boolean, default: false },
    activeMode: { type: String, default: 'view' },
    modelValue: { type: String, default: '' },
});

const emit = defineEmits(['update:modelValue']);
</script>

<template>
    <div class="heading" :class="{ 'heading-first': showLogo }">
        <h1>
            <EditableTextField :model-value="modelValue" @update:model-value="emit('update:modelValue', $event)"
                :active-mode="activeMode" :font-size="'24px'" :line-height="1" :top-padding="'0vh'" :bottom-padding="'2vh'" :font-weight="'bold'" :rows="1" :width="'95%'" />
        </h1>
        <img v-if="showLogo" id="logo" src="@img/VRR/Logo.svg" alt="VRR Logo" />
    </div>
</template>

<style scoped>
.heading-first #logo {
    width: 3%;
    margin-right: 2%;
}

.heading-first #logo,
.heading-first h1 {
    z-index: 2;
}

.heading-first {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
}

.heading-first,
.heading {
    width: 100%;
    height: fit-content;
    display: flex;
    position: sticky;
    top: 0;
    align-items: center;
    color: white;
    margin: 5% 0 5% 0;
    z-index: 12;
}

.heading-first h1,
.heading h1 {
    width: 60%;
    background-color: #760B5A;
    padding: 0.5rem 0 0.5rem 2rem;
    border-radius: 0 10px 10px 0;
}
</style>