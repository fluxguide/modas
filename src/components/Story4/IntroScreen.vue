<script setup>
import { ref } from 'vue';
import MainScreen from '@components/Story4/MainScreen.vue';
import SummaryScreen from '@components/Story4/SummaryScreen.vue';

const props = defineProps({
    data: { type: Array, default: () => [] },
    background: { type: Object, default: () => ({}) },
});

const introDismissed = ref(false);
const showSummary = ref(false);

function hideElements() {
    introDismissed.value = true;
}

function openSummary() {
    showSummary.value = true;
}

function closeSummary() {
    showSummary.value = false;
}

</script>

<template>
    <div v-if="!introDismissed" class="intro">
        <p>
            Was kostet ein Pkw-Stellplatz wirklich?
            <br />
            <br />
            Das Zukunftsnetz Mobilität hat 2022 gemeinsam mit kommunalen Verbänden in NRW Ansätze zur Berechnung der
            Stellplatzkosten vorgestellt.
        </p>
        <button id="start-button" @click="hideElements()">Explore more <span>&rarr;</span></button>
    </div>
    <img v-if="!introDismissed" src="@img/Story4/ParkingSign.svg" alt="Parking Sign" />
    <MainScreen v-if="!showSummary" :visibility="introDismissed" :data="props.data" :background="props.background"
        @summary="openSummary" />
    <SummaryScreen v-else @restart="closeSummary" />
</template>

<style scoped>
button,
input,
select,
textarea {
    font-family: inherit;
}

p {
    margin: 0;
}

.intro {
    width: 100%;
    height: 100%;
    box-sizing: border-box;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: start;
    padding: 5vh 5vw;
    backdrop-filter: blur(10px)
}

.intro p {
    width: 50%;
    position: relative;
    padding: 48px;
    background: #FFF;
    font-size: 32px;
    font-weight: 400;
    line-height: 40px;
    border-radius: 16px;
    border: 3px solid #1D2F6F;
    gap: 10px;
}

.intro button {
    width: fit-content;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #1D2F6F;
    color: #FFF !important;
    font-size: 32px;
    font-weight: 500;
    line-height: 40px;
    padding: 28px 48px;
    border-radius: 24px;
    border: none;
    box-shadow: 1px 1px 6px 0 rgba(255, 255, 255, 0.60);
    gap: 72px;
    margin-top: auto;
    margin-bottom: 0;
    cursor: pointer;
}

.intro button span {
    font-family: none;
    font-size: 56px;
}

img {
    width: auto;
    height: 40%;
    position: absolute;
    display: block;
    bottom: 0;
    right: 5vw;
}
</style>