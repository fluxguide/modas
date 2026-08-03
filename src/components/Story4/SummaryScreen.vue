<script setup>
import { computed, reactive, ref, watch } from 'vue';

import { summaryInsights as defaultSummaryInsights } from '@data/summaryInsights.js';
import EditableTextField from '@components/EditableTextField.vue';

const props = defineProps({
    activeMode: { type: String, default: 'view' },
});

const emit = defineEmits(['restart'])

const summaryInsights = ref(defaultSummaryInsights.map((insight) => ({ ...insight })));

const enabledMap = reactive(
    Object.fromEntries(defaultSummaryInsights.map((insight) => [insight.id, true])),
);

const visibleInsights = computed(() =>
    props.activeMode === 'edit'
        ? summaryInsights.value
        : summaryInsights.value.filter((insight) => enabledMap[insight.id] !== false),
);

const currentIndex = ref(0);

const currentInsight = computed(() => visibleInsights.value[currentIndex.value] ?? null);

const displayIndex = computed(() => String(currentIndex.value + 1).padStart(2, '0'));

const isFirst = computed(() => currentIndex.value === 0)
const isLast = computed(() => currentIndex.value >= visibleInsights.value.length - 1);

watch(visibleInsights, (list) => {
    if (currentIndex.value > list.length - 1) {
        currentIndex.value = Math.max(0, list.length - 1);
    }
});

function previousInsight() {
    return currentIndex.value -= 1;
}

function nextInsight() {
    if (!isLast.value) {
        currentIndex.value += 1;
    }
}

function toggleCurrentInsight(checked) {
    if (!currentInsight.value) return;
    enabledMap[currentInsight.value.id] = checked;
}

const texts = ref({
    summaryTitle: 'Summary',
    slide0Total: '8,250€',
    slide0Card1Number: '3,375€',
    slide0Card1Desc: 'Baukosten von 270 €/m²',
    slide0Card2Number: '4,875€',
    slide0Card2Desc: 'Laufende Summe – 195€ pro Stellplatz/Jahr',
    slide2TreeTitle: '16 Straßenbäume',
    slide2TreeDesc: 'ca. 500 € pro Baum, inkl. Pflanzung',
    slide2BikeTitle: '9 Fahrradständer',
    slide2BikeDesc: 'mit Platz für jeweils 5 Fahrräder, zu ca. 850 € pro Fahrradträger',
    slide2BenchTitle: '82 Parkbänke',
    slide2BenchDesc: 'ca. 100€ pro Werkbank für die jährliche Wartung',
    slide3Label1: 'Baukosten',
    slide3Label2: 'Jährlicher Lauf',
    slide3Label3: 'Gesamtwert über 25 Jahre',
});

const segments = ref([
    { label: 'Personnel', value: 170, color: '#6D01E0' },
    { label: 'Maintenance', value: 25, color: '#00EAFF' },
]);

const total = computed(() => segments.value.reduce((sum, s) => sum + s.value, 0));

const bars = computed(() => {
    let x = 0;
    return segments.value.map((s) => {
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
        <div v-if="currentInsight" class="summary-screen__body">
            <label v-if="props.activeMode === 'edit'" class="summary-screen__toggle">
                <input type="checkbox" :checked="enabledMap[currentInsight.id] !== false"
                    @change="e => toggleCurrentInsight(e.target.checked)" />
                In Zusammenfassung anzeigen
            </label>
            <div class="summary-screen__counter">
                <EditableTextField :model-value="texts.summaryTitle"
                    @update:model-value="val => texts.summaryTitle = val" :active-mode="props.activeMode" :rows="1"
                    :width="'fit-content'" :font-size="'88px'" :line-height="'88px'" :font-weight="'700'" />
                <p>{{ displayIndex }}<span>/0{{ visibleInsights.length }}</span></p>
            </div>
            <EditableTextField class="summary-screen__question" :model-value="currentInsight.description"
                @update:model-value="val => currentInsight.description = val" :active-mode="props.activeMode" :rows="2"
                :width="'100%'" :font-size="'28px'" :line-height="'40px'" :font-weight="'300'" />

            <div class="summary-screen__details summary-screen__details--0" v-if="currentInsight.id === '01'">
                <EditableTextField :model-value="texts.slide0Total" @update:model-value="val => texts.slide0Total = val"
                    :active-mode="props.activeMode" :rows="1" :width="'16vw'" :font-size="'72px'"
                    :font-weight="'700'" />
                <h2><span>&rarr;</span></h2>
                <div class="card">
                    <EditableTextField :model-value="texts.slide0Card1Number"
                        @update:model-value="val => texts.slide0Card1Number = val" :active-mode="props.activeMode"
                        :rows="1" :width="'16vw'" :font-size="'40px'" :line-height="'40px'" :font-weight="'700'" />
                    <EditableTextField :model-value="texts.slide0Card1Desc"
                        @update:model-value="val => texts.slide0Card1Desc = val" :active-mode="props.activeMode"
                        :rows="2" :width="'16vw'" :font-size="'22px'" :line-height="'40px'" />
                </div>
                <h2><span>&#43;</span></h2>
                <div class="card">
                    <EditableTextField :model-value="texts.slide0Card2Number"
                        @update:model-value="val => texts.slide0Card2Number = val" :active-mode="props.activeMode"
                        :rows="1" :width="'16vw'" :font-size="'40px'" :line-height="'40px'" :font-weight="'700'" />
                    <EditableTextField :model-value="texts.slide0Card2Desc"
                        @update:model-value="val => texts.slide0Card2Desc = val" :active-mode="props.activeMode"
                        :rows="2" :width="'16vw'" :font-size="'22px'" :line-height="'40px'" />
                </div>
            </div>
            <div class="summary-screen__details summary-screen__details--1" v-if="currentInsight.id === '02'">
                <svg viewBox="0 0 100 6" preserveAspectRatio="none" class="bar">
                    <rect v-for="(bar, i) in bars" :key="i" :x="bar.x" :width="bar.pct" y="0" height="6"
                        :fill="bar.color"></rect>
                </svg>
                <div class="legend">
                    <div v-for="(category, i) in segments" :key="i" class="category">
                        <span class="swatch" :style="{ backgroundColor: category.color }"></span>
                        <EditableTextField :model-value="category.label"
                            @update:model-value="val => segments[i].label = val" :active-mode="props.activeMode"
                            :rows="1" :width="'fit-content'" :font-size="'20px'" :line-height="'40px'"
                            :font-weight="'300'" />
                        <p v-if="props.activeMode !== 'edit'">
                            &nbsp;- {{ category.value }}€ ({{ Math.round(category.value / total * 100) }}%)
                        </p>
                        <p v-else class="category__value-edit">
                            &nbsp;-
                            <input type="number" min="0" class="category__value-input" :value="category.value"
                                @input="e => segments[i].value = Number(e.target.value) || 0" />
                            € ({{ Math.round(category.value / total * 100) }}%)
                        </p>
                    </div>
                </div>
            </div>
            <div class="summary-screen__details summary-screen__details--2" v-if="currentInsight.id === '03'">
                <div class="count-tree">
                    <img src="@img/Story4/Icons/Oak Tree.svg" alt="">
                    <div>
                        <EditableTextField :model-value="texts.slide2TreeTitle"
                            @update:model-value="val => texts.slide2TreeTitle = val" :active-mode="props.activeMode"
                            :rows="1" :width="'100%'" :font-size="'24px'" :line-height="'40px'" />
                        <EditableTextField :model-value="texts.slide2TreeDesc"
                            @update:model-value="val => texts.slide2TreeDesc = val" :active-mode="props.activeMode"
                            :rows="2" :width="'100%'" :font-size="'18px'" :line-height="'40px'" :font-weight="'300'" />
                    </div>
                </div>
                <div class="count-bike">
                    <img src="@img/Story4/Icons/Bicycle.svg" alt="">
                    <div>
                        <EditableTextField :model-value="texts.slide2BikeTitle"
                            @update:model-value="val => texts.slide2BikeTitle = val" :active-mode="props.activeMode"
                            :rows="1" :width="'100%'" :font-size="'24px'" :line-height="'40px'" />
                        <EditableTextField :model-value="texts.slide2BikeDesc"
                            @update:model-value="val => texts.slide2BikeDesc = val" :active-mode="props.activeMode"
                            :rows="2" :width="'100%'" :font-size="'18px'" :line-height="'40px'" :font-weight="'300'" />
                    </div>
                </div>
                <div class="count-bench">
                    <img src="@img/Story4/Icons/Park With Street Light.svg" alt="">
                    <div>
                        <EditableTextField :model-value="texts.slide2BenchTitle"
                            @update:model-value="val => texts.slide2BenchTitle = val" :active-mode="props.activeMode"
                            :rows="1" :width="'100%'" :font-size="'24px'" :line-height="'40px'" />
                        <EditableTextField :model-value="texts.slide2BenchDesc"
                            @update:model-value="val => texts.slide2BenchDesc = val" :active-mode="props.activeMode"
                            :rows="2" :width="'100%'" :font-size="'18px'" :line-height="'40px'" :font-weight="'300'" />
                    </div>
                </div>
            </div>
            <div class="summary-screen__details summary-screen__details--3" v-if="currentInsight.id === '04'">
                <div class="slider-container">
                    <input type="range" class="slider" min="1" max="100" v-model.number="sliderValue">
                    <p class="value-display">{{ sliderValue }} spaces</p>
                </div>
                <div class="count-categories">
                    <div>
                        <EditableTextField :model-value="texts.slide3Label1"
                            @update:model-value="val => texts.slide3Label1 = val" :active-mode="props.activeMode"
                            :rows="1" :width="'100%'" :font-size="'18px'" :line-height="'40px'" />
                        <p><span>{{ getBuildingCost(sliderValue) }}€</span></p>
                    </div>
                    <div>
                        <EditableTextField :model-value="texts.slide3Label2"
                            @update:model-value="val => texts.slide3Label2 = val" :active-mode="props.activeMode"
                            :rows="1" :width="'100%'" :font-size="'18px'" :line-height="'40px'" />
                        <p><span>{{ getAnnualCost(sliderValue) }}€</span></p>
                    </div>
                    <div>
                        <EditableTextField :model-value="texts.slide3Label3"
                            @update:model-value="val => texts.slide3Label3 = val" :active-mode="props.activeMode"
                            :rows="1" :width="'100%'" :font-size="'18px'" :line-height="'40px'" />
                        <p><span>{{ get25YearTotal(sliderValue) }}€</span></p>
                    </div>
                </div>
            </div>
        </div>
        <div v-else class="summary-screen__empty">
            <p>Keine Zusammenfassungsseiten ausgewählt.</p>
        </div>

        <div class="buttons">
            <button v-if="currentInsight && !isFirst" type="button" class="summary-screen__previous"
                @click="previousInsight">
                <span>&larr;</span> Zurück</button>
            <button v-if="currentInsight && !isLast" type="button" class="summary-screen__next" @click="nextInsight">
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

.summary-screen :deep(.editable-text-comp textarea),
.summary-screen :deep(.editable-text-comp .v-field__input) {
    color: #fff !important;
    caret-color: #fff;
}

.summary-screen__empty {
    width: 100%;
    height: 80%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
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

.summary-screen__toggle {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 0 0 0 auto;
    font-size: 16px;
    font-weight: 400;
    cursor: pointer;
}

.summary-screen__question {
    width: 100%;
    margin: 0 0 4vh;
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

        .category__value-edit {
            display: flex;
            align-items: center;
            gap: 4px;
        }

        .category__value-input {
            width: 4.5em;
            padding: 2px 6px;
            color: #fff;
            font: inherit;
            background: rgba(255, 255, 255, 0.08);
            border: 1px dashed #808080;
            border-radius: 6px;
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