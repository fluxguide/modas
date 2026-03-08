<template>
  <div class="story-container" ref="container">
    <ThuringiaStory v-if="storyData" :data="storyData" :mode="mode" />
    <div v-else class="loading">Loading story...</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { Streamlit } from "streamlit-component-lib";
import ThuringiaStory from "@src/components/Thuringia/ThuringiaApp.vue";

const storyData = ref(null);
const mode = ref("view");
const template = ref(null);

Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, (event) => {
  const args = event.detail.args;
  if (args.data) storyData.value = args.data;
  if (args.mode) mode.value = args.mode;
  if (args.template) template.value = args.template;
  // Set iframe to full viewport height
  Streamlit.setFrameHeight(window.screen.height - 250);
});

onMounted(() => {
  Streamlit.setComponentReady();
  Streamlit.setFrameHeight(window.screen.height - 250);
});
</script>

<style>
.story-container {
  width: 100%;
  height: 100vh;
  overflow-y: auto;
}
</style>