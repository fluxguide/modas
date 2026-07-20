<script setup>
import { computed, ref } from 'vue';

import { summaryInsights } from '@data/summaryInsights.js';

const emit = defineEmits(['restart'])

const currentIndex = ref(0);

const currentInsight = computed(() => summaryInsights[currentIndex.value]);

const isFirst = computed(() => currentIndex.value === 0)
const isLast = computed(() => currentIndex.value >= summaryInsights.length - 1);

function previousInsight() {
    return currentIndex.value -= 1;
}

function nextInsight() {
    if (!isLast.value) {
        currentIndex.value += 1;
    }
}

const segments = [
    { label: 'Personnel', value: 170, color: '#6D01E0' },
    { label: 'Maintenance', value: 25, color: '#00EAFF' },
];

const total = computed(() => segments.reduce((sum, s) => sum + s.value, 0));

const bars = computed(() => {
    let x = 0;
    return segments.map((s) => {
        const pct = (s.value / total.value) * 100;
        const bar = { ...s, x, pct };
        x += pct;
        return bar;
    });
});

const sliderValue = ref(10);

function getBuildingCost(spacesNum) {
    return spacesNum * 3375;
}

function getAnnualCost(spacesNum) {
    return spacesNum * 195;
}

function get25YearTotal(spacesNum) {
    return getBuildingCost(spacesNum) + getAnnualCost(spacesNum) * 25;
}

</script>

<template>
    <section class="summary-screen">
        <div class="summary-screen__body">
            <div class="summary-screen__counter">
                <h1>Summary</h1>
                <p>{{ currentInsight.id }}<span>/0{{ summaryInsights.length }}</span></p>
            </div>
            <p class="summary-screen__question">{{ currentInsight.description }}</p>
            <div class="summary-screen__details" :class="`summary-screen__details--${currentIndex}`"
                v-if="currentIndex === 0">
                <h2>8,250€</h2>
                <h2><span>&rarr;</span></h2>
                <div class="card">
                    <h4>3,375€</h4>
                    <p>Baukosten von 270 €/m²</p>
                </div>
                <h2><span>&#43;</span></h2>
                <div class="card">
                    <h4>4,875€</h4>
                    <p>Laufende Summe – 195€ pro Stellplatz/Jahr</p>
                </div>
            </div>
            <div class="summary-screen__details" :class="`summary-screen__details--${currentIndex}`"
                v-if="currentIndex === 1">
                <svg viewBox="0 0 100 6" preserveAspectRatio="none" class="bar">
                    <rect v-for="bar in bars" :key="bar.label" :x="bar.x" :width="bar.pct" y="0" height="6"
                        :fill="bar.color"></rect>
                </svg>
                <div class="legend">
                    <div v-for="category in segments" :key="category.label" class="category">
                        <span class="swatch" :style="{ backgroundColor: category.color }"></span>
                        <p>{{ category.label }} - {{ category.value }}€ ({{ Math.round(category.value / total * 100)
                            }}%)
                        </p>
                    </div>
                </div>
            </div>
            <div class="summary-screen__details" :class="`summary-screen__details--${currentIndex}`"
                v-if="currentIndex === 2">
                <div class="count-tree">
                    <img src="@img/Story4/Icons/Oak Tree.svg" alt="">
                    <div>
                        <p><span>16 Straßenbäume</span></p>
                        <p>ca. 500 € pro Baum, inkl. Pflanzung</p>
                    </div>
                </div>
                <div class="count-bike">
                    <img src="@img/Story4/Icons/Bicycle.svg" alt="">
                    <div>
                        <p><span>9 Fahrradständer</span></p>
                        <p>mit Platz für jeweils 5 Fahrräder, zu ca. 850 € pro Fahrradträger</p>
                    </div>
                </div>
                <div class="count-bench">
                    <img src="@img/Story4/Icons/Park With Street Light.svg" alt="">
                    <div>
                        <p><span>82 Parkbänke</span></p>
                        <p>ca. 100€ pro Werkbank für die jährliche Wartung</p>
                    </div>
                </div>
            </div>
            <div class="summary-screen__details" :class="`summary-screen__details--${currentIndex}`"
                v-if="currentIndex === 3">
                <div class="slider-container">
                    <input type="range" class="slider" min="1" max="100" v-model.number="sliderValue">
                    <p class="value-display">{{ sliderValue }} spaces</p>
                </div>
                <div class="count-categories">
                    <div>
                        <p>Baukosten</p>
                        <p><span>{{ getBuildingCost(sliderValue) }}€</span></p>
                    </div>
                    <div>
                        <p>Jährlicher Lauf</p>
                        <p><span>{{ getAnnualCost(sliderValue) }}€</span></p>
                    </div>
                    <div>
                        <p>Gesamtwert über 25 Jahre</p>
                        <p><span>{{ get25YearTotal(sliderValue) }}€</span></p>
                    </div>
                </div>
            </div>
        </div>

        <div class="buttons">
            <button v-if="!isFirst" type="button" class="summary-screen__previous" @click="previousInsight">
                <span>&larr;</span> Zurück</button>
            <button v-if="!isLast" type="button" class="summary-screen__next" @click="nextInsight">
                Nächstes Highlight <span>&rarr;</span>
            </button>
            <button class="summary-screen__explore-again" v-else @click="emit('restart')">Geschichte neu
                entdecken</button>
        </div>
    </section>
</template>

<style scoped lang="less">
.summary-screen {
    width: 100vw;
    height: 100vh;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: flex-start;
    padding: 6vh 7vw 12vh;

    color: #fff;
    background: rgba(0, 0, 0, 0.92);
}

.summary-screen__body {
    width: 100%;
    height: 80%;
    position: relative;
    display: flex;
    flex-direction: column;
}

.summary-screen__counter {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    margin: 4vh 0 12vh;
    font-size: 20px;
    font-weight: 700;

    h1,
    p {
        font-weight: 700;
        line-height: 88px;
    }

    h1 {
        font-size: 88px;
    }

    p {
        font-size: 48px;
    }

    span {
        font-weight: 400;
    }
}

.summary-screen__question {
    width: 100%;
    margin: 0 0 4vh;
    font-size: 28px;
    font-weight: 300;
    line-height: 40px;
}

.summary-screen__details {
    width: 100%;
    height: fit-content;
    position: relative;
    display: flex;
}

.summary-screen__details--0 {
    flex-direction: row;
    justify-content: start;
    align-items: center;
    gap: 4vw;

    h2 {
        font-size: 72px;
        font-weight: 700;
        line-height: 40px;
    }

    .card {
        width: fit-content;
        height: auto;
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: start;
        align-items: start;
        padding: 16px;
        margin: 0;
        gap: 8px;

        border-radius: 8px;
        border: 2px solid #FFF;
        background: rgba(255, 255, 255, 0.08);

        h4,
        p {
            margin: 0;
            padding: 0;
            line-height: 40px;
        }

        h4 {
            font-size: 40px;
            font-weight: 700;
        }

        p {
            font-size: 22px;
            font-weight: 400;
        }
    }
}

.summary-screen__details--1 {
    flex-direction: column;

    .bar {
        border-radius: 16px;
        overflow: hidden;
    }

    .legend {
        width: 100%;
        height: auto;
        position: inherit;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        margin-top: 16px;

        p {
            font-size: 20px;
            font-weight: 300;
            line-height: 40px;
        }

        .category {
            display: flex;
            flex-direction: row;
            align-items: center;
        }

        .swatch {
            width: 2vw;
            height: 2vw;
            flex-shrink: 0;
            border-radius: 6px;
            margin: 0 8px 0 0;
        }
    }
}

.summary-screen__details--2 {
    flex-direction: row;
    justify-content: space-between;
    align-items: start;
    margin-top: 3vh;
    gap: 6vw;

    .count-tree,
    .count-bike,
    .count-bench {
        width: calc(100% / 3);
        position: relative;
        display: flex;
        flex-direction: row;
        gap: 2vw;
        align-items: start;

        img {
            width: auto;
            height: 100%;
        }

        &>div>p {
            font-size: 18px;
            font-weight: 300;
            line-height: 40px;
            margin: 0 0 8px 0;

            span {
                font-size: 24px;
                font-weight: 400;
            }
        }
    }
}

.summary-screen__details--3 {
    flex-direction: column;

    .slider-container {
        width: 100%;
        height: fit-content;
        position: relative;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;

        .slider {
            width: 80%;
            height: 8px;
            margin: 0;
            cursor: pointer;

            -webkit-appearance: none;
            appearance: none;
            background: #FFF;

            &::-webkit-slider-thumb {
                -webkit-appearance: none;
                appearance: none;
                width: 2vw;
                height: 2vw;
                border: none;
                border-radius: 50%;
                background: #FFF;
                cursor: pointer;
            }

            &::-moz-range-thumb {
                width: 2vw;
                height: 2vw;
                border: none;
                border-radius: 50%;
                background: #FFF;
                cursor: pointer;
            }
        }

        p {
            color: #FFF;
            font-size: 32px;
            font-weight: 400;
            line-height: 40px;
            margin: 0;
        }
    }

    .count-categories {
        width: 80%;
        height: auto;
        position: relative;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: start;

        &>div {
            width: calc(80% / 3);
            display: flex;
            flex-direction: column;

            p {
                font-size: 18px;
                font-weight: 400;
                line-height: 40px;
                margin: 0;

                span {
                    font-size: 28px;
                    font-weight: 700;
                }
            }
        }
    }
}

.buttons {
    position: inherit;
    display: flex;
    flex-direction: row;
    align-items: center;
    margin-right: 0;
    margin-left: auto;
    gap: 32px;
}

.summary-screen__previous,
.summary-screen__next,
.summary-screen__explore-again {
    padding: 8px 32px;
    display: flex;
    flex-direction: row;
    align-items: center;
    border: none;
    border-radius: 24px;
    font-size: 24px;
    font-weight: 600;
    line-height: 40px;
    font-family: inherit;
    cursor: pointer;

    span {
        font-size: 32px;
    }
}

.summary-screen__previous {
    border: 2px solid #FFF;
    background: rgba(255, 255, 255, 0.08);
    color: #FFF;

    span {
        margin-right: 16px;
    }
}

.summary-screen__next,
.summary-screen__explore-again {
    color: #000 !important;
    background: #fff;
    box-shadow: 1px 1px 5px 0 rgba(255, 255, 255, 0.6);

    span {
        margin-left: 16px;
    }
}
</style>
