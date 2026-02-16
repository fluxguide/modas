<template>
  <div class="color-picker">
    <label>{{ label }}</label>
    <input type="color" :value="color" @input="onColorChange" />
    <span class="color-value">{{ color }}</span>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { Streamlit } from "streamlit-component-lib";

const label = ref("Pick a color");
const color = ref("#010080");

// Listen for render events (this is how Streamlit passes props/args)
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, (event) => {
  const args = event.detail.args;
  if (args.label) label.value = args.label;
  if (args.default) color.value = args.default;
  Streamlit.setFrameHeight();
});

function onColorChange(e) {
  color.value = e.target.value;
  // Send value back to Streamlit (equivalent to this.props in the video)
  Streamlit.setComponentValue(e.target.value);
}

onMounted(() => {
  Streamlit.setComponentReady();
  Streamlit.setFrameHeight();
});
</script>

<style scoped>
.color-picker {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px;
  font-family: "Albert Sans", sans-serif;
}

input[type="color"] {
  width: 48px;
  height: 48px;
  border: none;
  cursor: pointer;
}

.color-value {
  font-family: monospace;
  font-size: 14px;
}
</style>