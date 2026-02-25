<script setup>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue';
import { useScroll } from '@vueuse/core';
import { getScrollRange, selectedColour, isMobile } from '@src/composables/utils.js';
import { useUIControls } from '@src/composables/Thuringia/useUIControls.js';
import { useMapControls } from '@src/composables/Thuringia/useMapControls.js';
import { computeStats } from '@composables/Thuringia/useDataProcessing';

import ArrowChart from '@src/components/Thuringia/ArrowChart.vue';
import HeaderRange from '@src/components/Thuringia/HeaderRange.vue';
import TextRange from '@src/components/Thuringia/TextRange.vue';
import LeafletMap from '@src/components/Thuringia/LeafletMap.vue';
import MapSVG from '@src/components/Thuringia/MapSVG.vue';
import SpeechBubble from '@src/components/Thuringia/SpeechBubble.vue';
import SideMenu from '@src/components/SideMenu.vue';

const props = defineProps({
  data: { type: Object, default: null },
  mode: { type: String, default: 'view' },
});

const stats = ref(null);
const statsPercentages = ref(null);
const rawData = ref([]);
const currentRange = ref(0);
const arrowVisible = ref(false);
const showMapScrollytelling = ref(false);
const showMapScrollytelling2 = ref(false);
const showMapButton = ref(false);
const showMapOverlay = ref(false);
const initMidElement = ref(null);
const headerRangeRef = ref(null);
const textRangeRef = ref(null);
const arrowChartRef = ref(null);
const scrollContainer = ref(null);

const { visibleLayers, handleMapReady, handleMarkerClick, handleLayerToggle } = useMapControls();

const { showMainUI, hideMainUI, initializeUI, showMapImgUI, mapUI } = useUIControls();

const { y: scrollY, isScrolling } = useScroll(scrollContainer, {
  throttle: 16,
  idle: 200,
});

watch(scrollY, (newScrollY) => {
  if (!initMidElement.value) return;

  const windowHeight = window.innerHeight;
  const initMidRect = initMidElement.value.getBoundingClientRect();
  const initMidOutOfView = initMidRect.bottom <= 0;

  if (initMidOutOfView) {
    const initMidHeight = initMidElement.value.offsetHeight + initMidElement.value.offsetTop;
    const scrollAfterInitMid = Math.max(0, newScrollY - initMidHeight);
    const newRange = getScrollRange(scrollAfterInitMid, windowHeight);

    if (newRange === 3) {
      arrowVisible.value = false;
      showMapScrollytelling.value = true;
      showMapScrollytelling2.value = false;
      showMapButton.value = false;
      showMapImgUI();
      mapUI();
    } else if (newRange === 4) {
      arrowVisible.value = false;
      showMapScrollytelling.value = false;
      showMapScrollytelling2.value = true;
      showMapButton.value = false;
      mapUI();
    } else if (newRange === 5) {
      arrowVisible.value = false;
      showMapScrollytelling.value = false;
      showMapScrollytelling2.value = false;
      showMapButton.value = true;
      showMapImgUI();
      mapUI();
    } else {
      arrowVisible.value = true;
      showMapScrollytelling.value = false;
      showMapScrollytelling2.value = false;
      showMapButton.value = false;
      currentRange.value = newRange;
      showMainUI(newRange, headerRangeRef, textRangeRef, arrowChartRef);

      // Progressive ground scaling for mobile based on arrow stages
      if (isMobile()) {
        const groundElement = document.querySelector('.main');
        const headerRangeElement = document.querySelector('.headerRange');
        if (groundElement) {
          let groundHeight;
          if (newRange === 0) {
            groundHeight = 70; // Stage 0
          } else if (newRange === 1) {
            groundHeight = 75; // Stage 1
          } else if (newRange === 2) {
            groundHeight = 80; // Final stage
          }
          groundElement.style.height = `${groundHeight}vh`;

          // Move HeaderRange up with ground expansion
          if (headerRangeElement) {
            const headerBottomPosition = groundHeight;
            headerRangeElement.style.bottom = `${headerBottomPosition}vh`;
          }
        }
      }
    }
  } else {
    arrowVisible.value = false;
    showMapScrollytelling.value = false;
    showMapScrollytelling2.value = false;
    showMapButton.value = false;
    currentRange.value = 0;
    hideMainUI(headerRangeRef, textRangeRef, arrowChartRef);

    // Reset ground height for mobile
    if (isMobile()) {
      const groundElement = document.querySelector('.main');
      const headerRangeElement = document.querySelector('.headerRange');
      if (groundElement) {
        groundElement.style.height = '15vh';
      }
      // Reset HeaderRange position
      if (headerRangeElement) {
        headerRangeElement.style.bottom = '20vh';
      }
    }
  }
}, {
  immediate: true // Run immediately onmount
});

const scrollHeight = computed(() => {
  if (!scrollContainer.value) return 0;
  return scrollContainer.value.scrollHeight - scrollContainer.value.clientHeight;
});

onMounted(async () => {
  if (!props.data) return; // no data yet, nothing to render

  const rawData_parsed = props.data.map(d => ({
    id: +d.id,
    townHall: d.townhall_name || '',
    city: d.townhall_city || '',
    street: d.townhall_street || '',
    latitude: +d.townhall_latitude || 0,
    longitude: +d.townhall_longitude || 0,
    stops100m: +d.stops_within_100m || 0,
    stops200m: +d.stops_within_200m || 0,
    stops300m: +d.stops_within_300m || 0,
  }));

  const { stats: loadedStats, statsPercentages: loadedStatsPercentages } = computeStats(rawData_parsed);
  rawData.value = rawData_parsed;
  stats.value = loadedStats;
  statsPercentages.value = loadedStatsPercentages;

  initializeUI();
});
</script>

<template>
  <div class="thuringia-app" ref="scrollContainer">
    <SideMenu />
    <div class="scroll-wrapper" :style="{ height: `${scrollHeight}px` }">
      <div class="init-mid" ref="initMidElement">
        <img src="@img/Thuringia/Emblem.png" alt="Emblem" id="emblemImage" />
        <!-- before -->
        <!-- <h1>
          Thüringen hat <span>353 Rathäuser</span> und
          <span>662 Haltestellen innerhalb von 300 Metern</span> rund um Rathäuser.
        </h1> -->
        <h1>
          STADT hat <span>ANZAHL Rathäuser</span> und <span>ANZAHL Haltestellen innerhalb von 300 Metern</span> rund um
          Rathäuser.
        </h1>
        <h1><span>Und was bedeutet das für Inge?</span></h1>
      </div>
    </div>
    <div class="main" :style="{ '--selectedColour': selectedColour }">
      <div class="above-ground">
        <div class="cityHall">
          <img src="@img/Thuringia/Clouds.png" alt="Clouds" id="cloudsImage" />
          <img src="@img/Thuringia/Rathaus.png" alt="Rathaus" id="cityHallImage" />
        </div>
        <div class="arrow" :class="{ visible: arrowVisible }" v-if="arrowVisible">
          <ArrowChart ref="arrowChartRef" :stats="stats" :currentRange="currentRange" v-if="stats" />
          <HeaderRange ref="headerRangeRef" :stats="stats" :stats-percentages="statsPercentages"
            :currentRange="currentRange" v-if="stats" />
        </div>
        <div class="character">
          <img src="@img/Thuringia/Bus_Stop.png" alt="Bus Stop" id="busStopImage" />
          <img src="@img/Thuringia/Bus.png" alt="Bus" id="busImage" />
          <SpeechBubble :arrow-range="currentRange" v-if="arrowVisible" />
          <img src="@img/Thuringia/Inge.png" alt="Inge" id="ingeImage" />
        </div>
        <div v-if="showMapScrollytelling" class="map-scrollytelling">
          <div class="map-intro">
            <h2>Ein genauerer Blick auf die Karte zeigt, in welchen Teilen des Landes Rathäuser gut erreichbar sind
              und wo der öffentliche Nahverkehr eher Lücken aufweist.</h2>
          </div>
          <div class="svg-map-container">
            <MapSVG :csv-data="stats?.stops_within_300m" />
          </div>
        </div>
        <div v-if="showMapScrollytelling2" class="map-scrollytelling-2">
          <div class="map-intro">
            <h2>Wirklich abgehängt ist kaum ein Rathaus. <span>Nur 7 Prozent</span> liegen weiter als 300 Meter von der
              nächsten
              Haltestelle entfernt. Das heißt aber auch: Für einige bleibt der Weg zur Bushaltestelle ein kleiner
              Spaziergang.</h2>
          </div>
          <div class="svg-map-container">
            <MapSVG :csv-data="stats?.townhallsWithoutStopsWithin300m" :color-fill="'#E14A2C'" />
          </div>
        </div>
        <div v-if="showMapButton" class="pre-map-view">
          <div class="map-intro">
            <h1>Erkunden Sie selbst, wie gut Thüringens Rathäuser erreichbar sind.</h1>
            <br>
            <h2>Nutzen Sie die Filter und klicken Sie auf die Marker für Details.</h2>
          </div>
          <button class="open-map-btn" @click="showMapOverlay = true">Erkunden Sie die
            Karte</button>
        </div>
      </div>
      <div class="ground-content">
        <TextRange ref="textRangeRef" :stats="stats" :currentRange="currentRange" v-if="stats && arrowVisible" />
        <div class="sources" v-if="showMapButton">
          <p>Sources:</p>
        </div>
      </div>
      <div v-if="showMapOverlay" class="map-overlay">
        <LeafletMap :data="rawData" :stats="stats" :visible-layers="visibleLayers" @map-ready="handleMapReady"
          @marker-click="handleMarkerClick" @layer-toggle="handleLayerToggle" @close="showMapOverlay = false" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.thuringia-app {
  height: 100vh;
  overflow-y: auto;
}

p {
  text-align: center;
  font-size: 18px;
}

.main {
  height: 30vh;
  background-color: #E8DFC5;
  position: sticky;
  bottom: 0;
  left: 0;
  width: 100%;
  padding: 0px;
  overflow: visible;
  z-index: 3;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  transition: height 0.8s ease-in-out;
}

.above-ground {
  position: absolute;
  bottom: 100%;
  left: 0;
  width: 100%;
  height: 70vh;
  z-index: 4;
  opacity: 1;
  transition: opacity 0.2s ease-out;
}

.cityHall,
.arrow,
.character {
  position: absolute;
  bottom: 0;
}

.cityHall {
  left: 0;
  width: 25%;
  height: 70vh;
  margin: 0px 15px;
  z-index: 2;
}

.cityHall img {
  width: 100%;
  left: 0;
}

.cityHall img,
.character img {
  position: absolute;
  bottom: 0;
}

#cloudsImage {
  bottom: 40%;
}

.character {
  right: 0;
  width: 25%;
  height: 70vh;
  z-index: 2;
}

.arrow {
  left: calc(25% + 30px);
  width: 50%;
  height: 70vh;
  opacity: 0;
  transition: opacity 0.8s ease-in-out;
  z-index: 2;
}

.ground-content {
  width: 100%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

#emblemImage {
  width: calc(50% / 4);
}

.init-mid {
  width: 50%;
  margin-left: calc(25% + 50% / 5);
  margin-right: calc(100% - (25% + 50% / 5));
  margin-top: 5vh;
}

.init-mid h1 {
  width: 60%;
  text-align: left;
  font-size: 36px;
  font-weight: 400;
}

.init-mid h1 span {
  font-weight: 700;
}

#ingeImage {
  width: calc(30% * 1.2);
  right: 30%;
}

#ingeImage.scrolled {
  width: 30%;
}

#busStopImage {
  width: calc(25% * 1.2);
  left: 0;
}

#busStopImage.scrolled {
  width: 25%;
}

#busImage {
  width: 80%;
  right: 0;
}

#busImage,
#busStopImage {
  opacity: 0;
  transition: opacity 0.5s ease-in-out;
}

#ingeImage,
#busStopImage {
  transition: width 0.8s ease-in-out;
}

.scroll-wrapper {
  min-height: 700vh;
}

.pre-map-view,
.map-scrollytelling,
.map-scrollytelling-2 {
  position: absolute;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  bottom: 0;
  margin: 0 2%;
}

.pre-map-view {
  align-items: start;
  flex-direction: column;
  margin-left: 5%;
  z-index: 3;
}

.svg-map-container {
  position: relative;
  width: auto;
  height: 80%;
  margin-left: 5%;
}

.pre-map-view .map-intro {
  width: 60%;
}

.map-intro {
  width: 45%;
  height: 100%;
  position: relative;
  margin: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.5s ease-in-out;
}

.map-intro h1 {
  text-align: left;
  font-size: 36px;
  font-weight: 600;
  line-height: 2;
}

.map-intro h2 {
  text-align: left;
  font-size: 24px;
  font-weight: 400;
  line-height: 1.5;
}

.map-scrollytelling .map-intro h2,
.map-scrollytelling-2 .map-intro h2 {
  text-align: left;
  font-size: 26px;
  font-weight: 400;
  line-height: 2;
}

.map-scrollytelling-2 .map-intro h2 span {
  font-weight: 700;
}

#mapImage {
  width: 40%;
}

.open-map-btn {
  display: block;
  width: 30%;
  padding: 16px 32px;
  font-size: 1.2rem;
  background: #2b2d42;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  box-shadow: 0 0 4px rgba(0, 0, 0, 0.3);
  margin-bottom: 5%;
}

.open-map-btn:hover {
  background: #415a77;
  color: white;
}

.sources {
  width: 100%;
  height: 100%;
  font-size: 18px;
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: start;
  margin-left: 5%;
}

.map-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.main.visible,
#busImage.visible,
#busStopImage.visible,
.arrow.visible {
  opacity: 1;
}

@media (max-width: 768px) {
  .main {
    height: 15vh;
    padding: 10px;
    position: fixed;
    bottom: 0;
  }

  .above-ground {
    position: absolute;
    bottom: 100%;
    left: 0;
    width: 100%;
    z-index: 4;
    opacity: 1;
  }

  .cityHall {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 42%;
    height: 100%;
    margin-left: 5px;
    z-index: 5;
    transition: all 0.8s ease-in-out;
  }

  #cloudsImage {
    bottom: 20%;
  }

  .character {
    width: 45%;
    height: 100%;
    z-index: 5;
  }

  .arrow,
  .arrow.visible {
    position: fixed;
    width: 100%;
    transition: scale 0.8s ease-in-out;
    z-index: 4;
  }

  .ground-content {
    position: absolute;
    right: 0;
    top: 0;
    width: 60%;
    height: 100%;
    padding: 0px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
  }

  .ground-content:has(.open-map-btn) {
    width: 100%;
    align-items: center;
    justify-content: center;
    padding: 0;
  }

  #ingeImage.scrolled,
  #busStopImage.scrolled {
    position: fixed;
    bottom: 10px;
    transition: bottom 0.8s ease-in-out;
  }

  #ingeImage.scrolled {
    width: 17%;
    left: 15%;
  }

  #busStopImage.visible.scrolled {
    width: 13%;
    left: 5%;
  }

  #busStopImage.visible {
    left: 10%;
  }

  #busImage {
    width: 50%;
    position: fixed;
  }

  .init-mid {
    width: 90%;
    margin: 5% auto;
    text-align: center;
  }

  .init-mid h1 {
    width: 100%;
    font-size: 20px;
    text-align: center;
    line-height: 1.4;
  }

  #emblemImage {
    width: 25%;
    margin-bottom: 20px;
  }

  .pre-map-view,
  .map-scrollytelling,
  .map-scrollytelling-2 {
    flex-direction: column;
    margin: 0;
    bottom: 5%;
  }

  .pre-map-view {
    margin: 0;
    align-items: center;
    justify-content: start;
    gap: 15%;
  }

  .svg-map-container {
    position: relative;
    width: 100%;
    height: auto;
    margin: 0;
  }

  .pre-map-view .map-intro {
    width: 100%;
  }

  .map-intro {
    width: 100%;
    height: fit-content;
    position: relative;
    margin: 0;
    display: flex;
    flex-direction: column;
    justify-content: start;
  }

  .map-intro h1 {
    font-size: 24px;
    margin: 10%;
    margin-bottom: 0;
  }

  .map-intro h2 {
    font-size: 18px;
    margin: 10%;
    margin-bottom: 0;
  }

  .map-scrollytelling .map-intro h2,
  .map-scrollytelling-2 .map-intro h2 {
    font-size: 18px;
  }

  .open-map-btn {
    width: 80%;
    padding: 10px 0px;
    font-size: 16px;
    margin: 0 10% 0 10%;
    z-index: 7;
  }
}

@media (min-width: 2560px) {

  .map-scrollytelling,
  .map-scrollytelling-2 {
    margin: 0;
    justify-content: space-evenly;
  }

  .map-scrollytelling .map-intro h2,
  .map-scrollytelling-2 .map-intro h2 {
    font-size: 34px;
  }

  .map-intro h1 {
    font-size: 40px;
  }

  .map-intro h2 {
    font-size: 30px;
  }

  .open-map-btn {
    font-size: 28px;
  }
}

@media (min-width: 3440px) {
  .init-mid h1 {
    font-size: 48px;
  }

  .map-scrollytelling,
  .map-scrollytelling-2 {
    margin: 0;
    justify-content: space-evenly;
  }

  .map-scrollytelling .map-intro h2,
  .map-scrollytelling-2 .map-intro h2 {
    font-size: 42px;
  }

  .map-intro h1 {
    font-size: 48px;
  }

  .map-intro h2 {
    font-size: 38px;
  }

  .open-map-btn {
    font-size: 36px;
    padding: 18px 0;
    border-radius: 15px;
    border-width: 4px;
    box-shadow: 3px 2px 12px rgba(0, 0, 0, 0.3);
  }

  .svg-map-container {
    height: 90%;
  }
}
</style>