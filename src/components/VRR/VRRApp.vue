<script setup>
import { ref, watch, computed, onMounted, onUnmounted } from 'vue';
import { isMobile } from '@src/composables/utils.js';
import { loadData } from '@composables/VRR/useDataProcessing';

import ArrowBubbleChart from './ArrowBubbleChart.vue';
import Timeline from './Timeline.vue';
import PieChart from './PieChart.vue';
import HorizontalScrollChart from './HorizontalScrollChart.vue';
import SectionHeading from './SectionHeading.vue';
import PhaseCard from './PhaseCard.vue';
import ColouredSection from './ColouredSection.vue';
import BulletList from './BulletList.vue';
import PartnerLogos from './PartnerLogos.vue';
import SideMenu from '@src/components/SideMenu.vue';
import EditableTextField from '@src/components/EditableTextField.vue';

import robotHandsUp from '@img/VRR/Robot/HandsUp.svg';
import paul from '@img/VRR/Characters/Paul.svg';
import robotHandsDown from '@img/VRR/Robot/HandsDown.svg';

const props = defineProps({
    data: { type: Array, default: () => [] },
    mode: { type: String, default: 'view' },
    columnLabelMap: { type: Object, default: () => ({}) },
    categoryColours: { type: Object, default: () => [] },
});

const chartData = ref(null)
const activeMode = ref('view');
const isPresenting = ref(false);

// Data for bullet lists
const testlaufItems = [
    'Laufzeit: <span>Oktober</span> 2022 <span>bis September</span> 2024',
    'Ziel: <span>Test eines</span> digitalen, automatisierten Kundenkanals; <span>Erkenntnisgewinnung hinsichtlich</span> Kundenakzeptanz <span>und</span> Möglichkeiten <span>der</span> Substitution klassischer Dialogkanäle',
    'Technologie: KI-gestützter Chatbot',
    'Zielgruppe: Fahrgäste <span>mit Serviceanfragen</span>'
];

const phase1Items = [
    'Start: <span>Go-Live am 04.10. (Webseite vrr.de)</span>',
    'Reaktive Anzeige des Chatbuttons',
    'Nutzerbewertung: <span>Abfrage der Zufriedenheit der Nutzer / subjektive Auskunftsqualität in Form einer Sternebewertung</span>'
];

const chatbotItems = [
    '<span>Aufbau Q&A Chatbot:</span> Modellierung <span>sog.</span> „Flows" <span>(Abläufe) für</span> verschiedene Themenbereiche<span>, in Zukunft KI-gestützt.</span>',
    'Antwortgenerierung: <span>Ausspielung von bis zu fünf verschiedenen Wissensartikeln, auch als Verlinkung</span>',
    'Identifizierung <span>von</span> geeigneten Themen <span>für das (priorisierte) Beauskunften durch Chatbot</span>'
];

const selectedPieSlice = ref(null);

const handlePieSliceSelected = (sliceData) => {
    selectedPieSlice.value = sliceData;
};

const characterImage = computed(() => {
    if (!selectedPieSlice.value) return robotHandsUp; // image before pressing on category
    if (selectedPieSlice.value.index === 0) return robotHandsUp;
    if (selectedPieSlice.value.index === 1) return paul;
});

const characterMessage = computed(() => {
    if (!selectedPieSlice.value) return 'Ich konnte rund 70% aller Anfragen selbst lösen!';

    // Change message based on selected slice
    if (selectedPieSlice.value.index === 0) {
        return `Ich konnte rund ${selectedPieSlice.value.percentage}% aller Anfragen selbst lösen!`;
    }
    if (selectedPieSlice.value.index === 1) {
        return `In ${selectedPieSlice.value.percentage}% haben wir vom Servicepersonal geholfen!`;
    }
});

const handleModeChange = (newMode) => {
    if (newMode === "presenter") {
        activeMode.value = "view";
        const storyContainer = document.querySelector('.vrr-app');
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

watch(() => props.data, (newData) => {
    if (!newData || newData.length === 0) return;
    chartData.value = loadData(newData);
}, { immediate: true });

onMounted(async () => {
    document.addEventListener("fullscreenchange", () => {
        if (!document.fullscreenElement) {
            isPresenting.value = false;
        }
    })
});

onUnmounted(() => {
    document.removeEventListener("fullscreenchange", () => { });
});
</script>

<template>
    <div class="vrr-app">
        <SideMenu v-if="!isPresenting" :active-mode="activeMode" :default-gradient="{
            angle: 180,
            stops: [{ color: '#ffffff', position: 0 }, { color: '#e1ffd6', position: 50 }, { color: '#d6f5ff', position: 100 }]
        }" @mode-change="handleModeChange" />
        <button v-if="isPresenting" class="exit-presenter" @click="exitPresenter">Präsentationsansicht beenden</button>
        <header>
            <img src="@img/VRR/Logo.svg" alt="VRR Logo" />
            <div>
                <h1><span>Service-Chat</span></h1>
                <h1>Digitale Transformation im Kundenservice</h1>
            </div>
        </header>
        <main>
            <!-- Part 1 -->
            <div class="chat-img">
                <img id="openai-chat" src="@img/VRR/OpenAI-Chat.svg" alt="OpenAI Chat" />
                <img id="vrr-chat" src="@img/VRR/VRR-Chat.svg" alt="VRR Chat" />
            </div>

            <div class="tp-img"> <!-- tp -> transport & people -->
                <img id="red-tram" src="@img/VRR/Transport/TramRed.svg" alt="Red Tram" />
                <img id="people" src="@img/VRR/Characters/People.svg" alt="People" />
                <img id="red-bus" src="@img/VRR/Transport/BusRed.svg" alt="Red Bus" />
            </div>
            <!-- ----------------------------------------------------- -->

            <!-- Part 2 -->
            <SectionHeading :show-logo="true">
                Anfragen <span>über die</span> verschiedenen Kanäle
            </SectionHeading>

            <div class="chart-overlay">
                <ArrowBubbleChart :stats-data="chartData?.stats" :mehrwert-data="chartData?.mehrwertData"
                    chart-type="stats" :height="'55vh'" :bubble-position="[28, 51, 75]" :timeline-start="25"
                    :percentage-shift="23" :bubble-gap="1" :category-names="chartData?.categoryNames" />
            </div>

            <div class="bg-img">
                <img id="orange-tram" src="@img/VRR/Transport/TramOrange.svg" alt="Orange Tram" />
                <img id="ava" src="@img/VRR/Characters/Ava.svg" alt="Ava" />
            </div>
            <!-- ----------------------------------------------------- -->

            <!-- Part 3 -->
            <SectionHeading>
                <span>Steigende Erwartungen an</span> digitale Erreichbarkeit
            </SectionHeading>

            <ColouredSection>
                <template #background>
                    <div class="characters">
                        <img id="theo" src="@img/VRR/Characters/Theo.svg" alt="Theo" />
                        <img id="ava" src="@img/VRR/Characters/Ava.svg" alt="Ava" />
                    </div>
                    <div class="tram-bus">
                        <img id="orange-tram-second" src="@img/VRR/Transport/TramOrange.svg" alt="Orange Tram" />
                        <img id="green-bus" src="@img/VRR/Transport/BusGreen.svg" alt="Green Bus" />
                    </div>
                    <img id="theresa" src="@img/VRR/Characters/Theresa.svg" alt="Theresa">
                </template>

                <img id="paul" src="@img/VRR/Characters/Paul.svg" alt="Paul">
                <h1>" <span>Wie können wir Fahrgastanfragen</span> schnell, effizient <span>und</span> rund um
                    die Uhr
                    <span>bearbeiten?</span>
                </h1>
            </ColouredSection>
            <!-- ----------------------------------------------------- -->

            <!-- Part 4 -->
            <SectionHeading>
                <span> Oktober 2022 bis September 2024 –</span> Testlauf Service-Chat
            </SectionHeading>

            <ColouredSection>
                <template #background>
                    <div class="testlauf-bg-img">
                        <div class="bus-crosswalk">
                            <img id="green-bus" src="@img/VRR/Transport/BusGreen.svg" alt="Green Bus" />
                            <img id="crosswalk" src="@img/VRR/Characters/Crosswalk.svg" alt="People on a crosswalk">
                        </div>
                        <img id="orange-tram" src="@img/VRR/Transport/TramOrange.svg" alt="Orange Tram">
                    </div>
                </template>

                <BulletList :items="testlaufItems" />

                <template #extra>
                    <PartnerLogos />
                </template>
            </ColouredSection>
            <!-- ----------------------------------------------------- -->

            <!-- Part 5 -->
            <SectionHeading>
                Phasenverlauf <span>des Versuchs</span>
            </SectionHeading>

            <div class="section-wrapper">
                <div class="characters-tram">
                    <img id="theo" src="@img/VRR/Characters/Theo.svg" alt="Theo" />
                    <img id="orange-tram" src="@img/VRR/Transport/TramOrange.svg" alt="Orange Tram" />
                    <img id="ava" src="@img/VRR/Characters/Ava.svg" alt="Ava" />
                </div>
                <img id="theresa-phases" src="@img/VRR/Characters/Theresa.svg" alt="Theresa">

                <div class="phase-cards">
                    <PhaseCard phase-title="Phase 1" phase-description="Personenbedienter Chat" :character-image="paul"
                        character-alt="Paul" phase-class="phase1" />
                    <PhaseCard phase-title="Phase 2" phase-description="Q&A-Chatbot, KI unterstützt"
                        :character-image="robotHandsDown" character-alt="Robot Hands Down" phase-class="phase2" />
                    <Timeline />
                </div>
            </div>
            <!-- ----------------------------------------------------- -->

            <!-- Part 6 -->
            <SectionHeading>
                Service-Chat – Phase 1: <span>Personenbedienter Chat</span>
            </SectionHeading>

            <ColouredSection>
                <BulletList :items="phase1Items" />

                <template #extra>
                    <img id="paul-big" src="@img/VRR/Characters/Paul.svg" alt="Paul">
                </template>
            </ColouredSection>
            <!-- ----------------------------------------------------- -->

            <!-- Part 7 -->
            <SectionHeading>
                Service-Chat – Phase 2: <span>Q&A-Chatbot</span>
            </SectionHeading>
            <div class="whole-robot-section">
                <img id="robot-cheering" src="@img/VRR/Robot/HandsUpCheering.svg" alt="Robot with hands up cheering">
                <div class="robot-chatbot-section">
                    <div class="message">
                        <h1>Hallo Mensch!</h1>
                        <h1><span>Ich bin ein</span> Chatbot.</h1>
                        <h1><span>Du kannst mich alles fragen!</span></h1>
                    </div>
                    <div class="section-wrapper">
                        <ColouredSection wrapper-class="robot-chatbot-wrapper" coloured-class="robot-coloured"
                            white-space-class="robot-white">
                            <BulletList :title="'Q&A Chatbot'" :items="chatbotItems" />
                        </ColouredSection>
                    </div>
                </div>
            </div>
            <!-- ----------------------------------------------------- -->

            <!-- Part 8 -->
            <SectionHeading>
                <span>Versuch</span> Service-Chat – Zwischenergebnis
            </SectionHeading>
            <div class="character-chart">
                <img id="character-change" :src="characterImage" alt="Character">
                <PieChart :data="chartData?.pieData" @pie-slice-selected="handlePieSliceSelected" />
                <div class="message-character">
                    <h1>{{ characterMessage }}</h1>
                </div>
            </div>
            <!-- ----------------------------------------------------- -->

            <!-- Part 9 -->
            <SectionHeading>
                <span>Ergebnis</span> Service-Chat – Erfolgsroboter
            </SectionHeading>
            <div class="robot-form">
                <div class="stars-robot">
                    <img id="stars" src="@img/VRR/Stars.svg" alt="Stars">
                    <img id="robot-hands-up-cheering" src="@img/VRR/Robot/HandsUpCheering.svg"
                        alt="Cheering robot with hands up">
                </div>
                <ColouredSection wrapper-class="robot-form-wrapper" coloured-class="robot-form-coloured"
                    white-space-class="robot-form-white">
                    <div class="intro">
                        <h1>Bewertung:</h1>
                        <h1><span>Durchschnittlich</span> 4 von 5 Sternen</h1>
                    </div>
                    <div class="form">
                        <h1>Gesprächsbewertung</h1>
                        <h1><span>Vielen Dank für das Gespräch. Konnten wir Ihnen behilflich sein?</span></h1>
                        <img src="@img/VRR/StarsForm.svg" alt="Stars for rating">
                        <div class="submit-button">
                            <h1>BEWERTUNG SENDEN</h1>
                        </div>
                    </div>
                    <div class="tooltip">
                        <p>Nutzerbewertung erfolgte über eine Abfrage der <span>Zufriedenheit</span> der
                            Nutzer*innen / <span>subjektive Auskunftsqualität</span> in Form einer
                            <span>Sternebewertung</span>
                        </p>
                    </div>
                </ColouredSection>
            </div>
            <!-- ----------------------------------------------------- -->

            <!-- Part 10 -->
            <SectionHeading>
                Mehrwert ohne Verdrängung
            </SectionHeading>
            <HorizontalScrollChart :stats-data="chartData?.stats" :mehrwert-data="chartData?.mehrwertData"
                :year-shift="1" :wrapper-height="isMobile() ? '100vh' : '300vh'" :scroll-sensitivity="0.2"
                :category-names="chartData?.categoryNames" />
            <!-- ----------------------------------------------------- -->
        </main>
    </div>
</template>

<style scoped>
.vrr-app {
    height: 100vh;
    width: 100%;
    overflow-x: hidden;
}

header {
    width: 100%;
    height: 15vh;
    display: flex;
    flex-direction: row;
    align-items: center;
    margin: 2% 0 2% 5%;
    color: #760B5A;
    line-height: 1;
    gap: 2rem;
}

header img {
    width: 6%;
}

h1 span {
    font-weight: 400;
}

main {
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
}

.chat-img {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 2%;
    height: 45vh;
}

#openai-chat {
    width: 60%;
}

#vrr-chat {
    width: 25%;
}

.tp-img {
    width: 100%;
    position: relative;
    display: flex;
    align-items: end;
    justify-content: center;
    overflow: hidden;
    height: 25vh;
    margin-bottom: 5%;
}

#red-tram {
    height: 100%;
    width: auto;
    position: absolute;
    left: 0;
    bottom: 0;
    transform: translateX(-70%);
}

#people {
    height: 50%;
    position: absolute;
    z-index: 2;
}

#red-bus {
    height: 100%;
    width: auto;
    position: absolute;
    right: 0;
    bottom: 0;
    transform: translateX(60%);
}

#orange-tram {
    position: relative;
    height: 25vh;
    transform: translateX(90%);
    opacity: 0.08;
    z-index: 1;
    margin-top: -15vh;
    margin-bottom: 15px;
}

.tram-bus {
    position: relative;
    width: 100%;
    align-items: center;
    display: flex;
    flex-direction: row;
    gap: 40%;
    margin-top: -35vh;
    height: 25vh;
}

#orange-tram-second,
#green-bus {
    height: 100%;
    z-index: 0;
}

#orange-tram-second {
    opacity: 0.12;
}

#green-bus {
    opacity: 0.2;
}

.chart-overlay {
    position: relative;
    width: 100%;
    z-index: 3;
    pointer-events: none;
    margin-bottom: 5%;
}

.characters {
    margin-bottom: 20%;
}

.characters,
.characters-tram,
.bg-img {
    position: relative;
    width: 100%;
    align-items: end;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}

.bg-img {
    width: 100%;
    display: flex;
    flex-direction: column;
    margin-bottom: 10%;
}

.bg-img #orange-tram {
    transform: none;
}

.characters-tram {
    align-items: flex-start;
}

.characters-tram #orange-tram {
    margin: -5% -5% 0 0;
    transform: none;
}

.characters-tram #theo,
.characters-tram #ava {
    opacity: 0.13;
}

#theo,
#ava {
    height: 30vh;
    opacity: 0.4;
}

#orange-tram,
#theo,
#ava,
#theresa,
#theresa-phases {
    z-index: 1;
}

#theresa,
#theresa-phases {
    height: 50vh;
    position: relative;
    margin-top: 5%;
    opacity: 0.4;
}

#theresa-phases {
    opacity: 0.13;
    margin-top: 0;
}

.section-wrapper {
    position: relative;
    width: 100%;
    height: 80vh;
}

.section-wrapper .characters {
    margin-bottom: 0;
}

#paul {
    width: 50%;
}

.testlauf-bg-img {
    position: relative;
    width: 100%;
    display: flex;
    flex-direction: row;
    margin-left: -2%;
}

.bus-crosswalk {
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 50%;
}

#crosswalk {
    width: 40%;
    margin-left: 15%;
    opacity: 0.4;
}

.testlauf-bg-img #orange-tram {
    opacity: 0.23;
    height: 35vh;
    transform: translateY(50%);
    margin: 0 0 0 20%;
}

.phase-cards {
    height: 50vh;
    z-index: 4;
    position: absolute;
    width: 100%;
    top: 0;
    display: flex;
    flex-direction: row;
    align-items: center;
}

#paul-big {
    position: absolute;
    left: -5%;
    bottom: 0;
    z-index: 2;
}

.whole-robot-section {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    width: 100%;
    margin-bottom: 0;
}

#robot-cheering {
    position: sticky;
    top: 10%;
    width: 30%;
    margin-left: 10%;
}

.robot-chatbot-section {
    position: relative;
    width: 60%;
    display: flex;
    flex-direction: column;
    align-items: center;
    z-index: 11;
    margin-top: 25%;
    margin-left: auto;
    margin-right: 5%;
}

.message {
    position: relative;
    width: 50%;
    background-color: white;
    padding: 2rem 3rem;
    border-radius: 0 150px 230px 190px;
    line-height: 1.2;
    text-align: center;
}

.message h1 {
    margin-top: 0;
}

.character-chart {
    height: 70vh;
    width: 100%;
    position: relative;
}

#character-change {
    position: absolute;
    right: 55%;
    bottom: 0;
    height: 70%;
    max-width: 35%;
}

.character-chart>*:nth-child(2) {
    position: absolute;
    right: 10%;
    bottom: 0;
}

.message-character::before {
    content: '';
    position: absolute;
    top: -20px;
    left: 5%;
    border-left: 30px solid transparent;
    border-bottom: 20px solid white;
    transform: skew(70deg);
}

.message-character {
    position: absolute;
    width: 15%;
    left: 37%;
    bottom: 5%;
    background-color: white;
    padding: 0.5rem 1.5rem;
    border-radius: 450px 400px 600px 800px;
    text-align: center;
}

.message-character h1 {
    font-weight: 400;
    font-size: 20px;
    text-wrap: wrap;
}

.robot-form {
    width: 100%;
    height: 60vh;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
}

.stars-robot {
    width: 40%;
    height: 100%;
    position: relative;
    align-items: center;
    display: flex;
    flex-direction: column;
}

#robot-hands-up-cheering {
    height: 100%;
    width: fit-content;
    transform: rotate(-10deg);
}

#stars {
    position: absolute;
    top: 5%;
    width: 60%;
    z-index: 2;
}

.robot-form .white-space h1 {
    width: 100%;
    line-height: 1.3;
}

.intro {
    height: 20%;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.intro h1 {
    text-align: left;
    margin: 0;
}

.form::before {
    content: "\00d7";
    position: absolute;
    top: 0;
    right: 10px;
    font-size: 1.5rem;
    color: #BBBBBB;
}

.form {
    position: relative;
    width: 90%;
    height: 60%;
    background-color: white;
    border-radius: 10px;
    border-color: #BBBBBB;
    border-width: 1.2px;
    border-style: solid;
    padding: 1rem 1.5rem;
    transform: rotate(-5deg);
    align-items: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 1rem;
}

.form h1 {
    margin: 0;
}

.form span {
    color: #666666;
    font-size: 1.8rem;
}

.form img {
    width: 70%;
    margin: 2% 0;
}

.submit-button {
    width: 100%;
    background-color: #A6127E;
    border-radius: 5px;
    text-align: center;
    color: white;
}

.submit-button h1 {
    margin: 0.5rem 0;
    font-size: 1.2rem;
    font-weight: 500;
}

.tooltip::before {
    content: "\2139";
    font-size: 1.5rem;
    color: white;
    background-color: #760B5A;
    border-radius: 50%;
    padding: 1.5px 10px;
    text-align: center;
}

.tooltip {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-left: auto;
    margin-right: 0;
    z-index: 5;
    cursor: pointer;
}

.tooltip p {
    visibility: hidden;
    min-width: 250px;
    background-color: white;
    color: #000;
    text-align: left;
    border-radius: 6px;
    padding: 5px 10px;
    position: absolute;
    z-index: 50;
    bottom: 100%;
    right: 0;
    text-wrap: wrap;
    border: 1.5px solid #BBB;
}

.tooltip p span {
    font-weight: 600;
}

.tooltip:hover p {
    visibility: visible;
}

.exit-presenter {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 1001;
    padding: 10px 20px;
    font-size: 16px;
    background-color: #010080;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 1px 1px 4px 0 rgba(0, 0, 0, 0.40);
    font-style: normal;
    font-weight: 500;
    line-height: normal;
}

.vrr-app:fullscreen::backdrop {
    background-image: linear-gradient(rgba(255, 255, 255, 1), rgba(225, 255, 214, 1), rgba(214, 245, 255, 1)) !important;
}

.vrr-app:fullscreen {
    background: transparent !important;
}

.vrr-app:-webkit-full-screen,
.vrr-app:-moz-full-screen,
.vrr-app:-ms-fullscreen {
    background: transparent !important;
}
</style>