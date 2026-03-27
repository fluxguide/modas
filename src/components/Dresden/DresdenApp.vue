<script setup>
import { useScroll, useElementBounding } from '@vueuse/core'
import { computed, ref, watch, onMounted, onUnmounted } from 'vue';
import MapSVG from './MapSVG.vue';

const selectedCharacterIndex = ref(null)

const selectCharacter = (index) => {
    selectedCharacterIndex.value = index
    console.log(`Character ${index + 1} selected`)
}

const panels = ref(4)
const wrapperSize = computed(() => `${100 + (panels.value - 1) * 100}vh`)

const wrapperRef = ref(null)
const scrollX = ref(0)

const { y: scrollY } = useScroll(window)
const { top: wrapperTop, height: wrapperHeight } = useElementBounding(wrapperRef)

const scrollProgress = computed(() => {
    if (!wrapperHeight.value) return 0
    const start = wrapperTop.value
    const end = wrapperTop.value + wrapperHeight.value - window.innerHeight

    if (scrollY.value <= start) return 0
    if (scrollY.value >= end) return 1
    return (scrollY.value - start) / (end - start)
})

const updateScrollX = () => {
    scrollX.value = scrollProgress.value * (panels.value - 1) * window.innerWidth
}

watch(scrollProgress, updateScrollX)

const onScroll = () => {
    updateScrollX()
}

onMounted(() => {
    window.addEventListener('scroll', onScroll)
})
onUnmounted(() => {
    window.removeEventListener('scroll', onScroll)
})


</script>

<template>
    <div ref="wrapperRef" class="story-wrapper dresden-app" :style="{ height: wrapperSize }">
        <div class="story-sticky">
            <div class="story-row" :style="{ transform: `translateX(-${scrollX}px)` }">
                <!-- Initial screen -->
                <section class="panel">
                    <div class="screen-placeholder">
                        <div class="centered-screen1">
                            <h1><span>DRESDEN IN BEWEGUNG</span></h1>
                            <h1>SCROLLE WEITER UND ENTDECKE, WIE SICH DRESDEN BEWEGT</h1>
                        </div>
                    </div>
                </section>

                <!-- Character Selection -->
                <section class="panel">
                    <div class="screen-placeholder">
                        <h1><span>Wähle einen Charakter</span></h1>
                        <div class="characters">
                            <img v-for="src, index in [
                                '/src/components/modas/img/Dresden/Characters/Character1.png',
                                '/src/components/modas/img/Dresden/Characters/Character2.png',
                                '/src/components/modas/img/Dresden/Characters/Character3.png'
                            ]" :key="src" :src="src" alt="Character Image" @click="selectCharacter(index)"
                                :class="{ 'selected': selectedCharacterIndex === index }" />
                        </div>
                    </div>
                </section>

                <!-- District Selection -->
                <section class="panel">
                    <div class="screen-placeholder">
                        <h1><span>Wähle einen Stadtteil</span></h1>
                        <MapSVG />
                    </div>
                </section>

                <!-- Transport Selection -->
                <section class="panel">
                    <div class="screen-placeholder">
                        <h1><span>Wähle einE Fortbewegungsart aus</span></h1>
                    </div>
                </section>
            </div>
            <div class="fixed-bottom">
                <h2>SCROLLEN ZUM LOSFAHREN <span>&#8594</span></h2>
            </div>
            <div class="fixed-bottom-road"></div>
        </div>
    </div>
</template>

<style scoped>
.story-wrapper {
    position: relative;
    width: 100%;
}

.story-sticky {
    position: sticky;
    top: 0;
    height: 100vh;
    width: 100%;
    overflow: hidden;
}

.story-row {
    display: flex;
    height: 100%;
}

.panel {
    width: 100vw;
    height: 95vh;
    flex-shrink: 0;
}

.dresden-app {
    height: 100vh;
    width: 100vw;
}

.screen-placeholder {
    width: 100vw;
    height: 100%;
}

.screen-placeholder,
.centered-screen1 {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.centered-screen1 {
    width: 70vw;
    gap: 20px;
}

h1 {
    color: #000;
    text-align: center;
    font-family: Bedstead;
    font-size: 60px;
    font-weight: 400;
    line-height: 1.2;
    letter-spacing: 3.6px;
    text-transform: uppercase;
}

h1 span {
    color: #FDD7AD;
    -webkit-text-stroke-width: 4.5px;
    -webkit-text-stroke-color: #DD4B1A;
    font-size: 70px;
    font-weight: 700;
    letter-spacing: 11.2px;
    text-transform: uppercase;
}

h2 {
    color: rgb(239, 239, 239);
    font-size: 30px;
    font-weight: 500;
    letter-spacing: 4.8px;
    text-transform: uppercase;
}

h2 span {
    font-family: Arial, Helvetica, sans-serif;
    font-weight: 600;
    font-size: 40px;
}

.characters {
    display: flex;
    height: 80%;
    justify-content: center;
    align-items: center;
    gap: 7vw;
}

.characters img {
    height: 90%;
    cursor: pointer;
    transition: filter 0.2s ease, transform 0.3s ease;
}

.characters img:hover {
    transform: scale(1.1);
}

.characters img.selected {
    filter: drop-shadow(0 0 10px rgba(4, 231, 31, 1));
    transform: scale(1.03);
}

.fixed-bottom,
.fixed-bottom-road {
    position: absolute;
    width: 100vw;
    height: 5vh;
    bottom: 0;
    right: 0;
}

.fixed-bottom {
    display: flex;
    justify-content: end;
    align-items: center;
    text-align: end;
    z-index: 1;
    padding-right: 20px;
}

.fixed-bottom-road {
    background-image: url("/src/components/modas/img/Dresden/Road.svg");
}
</style>