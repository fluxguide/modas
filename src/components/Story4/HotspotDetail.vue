<script setup>
import { computed } from "vue";

const props = defineProps({
    spot: {
        type: Object,
        default: null,
    },
    spots: {
        type: Array,
        default: () => [],
    },
});

const emit = defineEmits(["close", "navigate", "summary"]);

const currentIndex = computed(() =>
    props.spots.findIndex((s) => s.id === props.spot?.id),
);
const previousSpot = computed(() =>
    currentIndex.value > 0 ? props.spots[currentIndex.value - 1] : null,
);
const nextSpot = computed(() =>
    currentIndex.value >= 0 && currentIndex.value < props.spots.length - 1
        ? props.spots[currentIndex.value + 1]
        : null,
);
</script>

<template>
    <aside class="detail-panel" :class="{ 'detail-panel--open': spot }" :aria-hidden="!spot">
        <button type="button" class="detail-panel__close" @click="$emit('close')">
            &#10005;
        </button>

        <div v-if="spot" class="detail-panel__body">
            <p :style="{ color: spot.color }" class="counter-paragraph">
                {{ spot.id }}<span>/05 - </span>{{ spot.label }}
            </p>
            <h2>
                {{ spot.property }}
            </h2>

            <p>
                <span>{{ spot.description }}</span>
            </p>

            <div class="cards">
                <div class="card1" :style="{
                    background: `color-mix(in srgb, ${spot.color} 16%, transparent)`,
                }">
                    <h4>{{ spot.card1.headerNumber }}</h4>
                    <p>
                        <span>{{ spot.card1.description }}</span>
                    </p>
                </div>
                <div class="card2" :style="{
                    background: `color-mix(in srgb, ${spot.color} 16%, transparent)`,
                }">
                    <h4>{{ spot.card2.headerNumber }}</h4>
                    <p>
                        <span>{{ spot.card2.description }}</span>
                    </p>
                </div>
            </div>

            <div class="buttons">
                <button v-if="previousSpot" class="previous-button" :style="{
                    border: `2px solid ${previousSpot.color}`,
                    background: `color-mix(in srgb, ${previousSpot.color} 8%, transparent)`,
                }" @click="emit('navigate', previousSpot.key)">
                    <span>&larr;</span> Previous
                </button>
                <button v-if="nextSpot" class="next-button" @click="emit('navigate', nextSpot.key)">
                    Next Spotlight <span>&rarr;</span>
                </button>
                <button v-else class="summary-button" @click="emit('summary')">See full summary</button>
            </div>
        </div>
    </aside>
</template>

<style scoped lang="less">
.detail-panel {
    position: absolute;
    z-index: 10;
    top: 0;
    right: 0;

    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    width: 40vw;
    height: 100%;
    padding: 6vh 4vw;
    overflow-y: auto;

    color: #fff;
    background: rgba(0, 0, 0, 0.92);
    box-shadow: -8px 0 40px rgba(0, 0, 0, 0.5);

    transform: translateX(100%);
    transition: transform 0.5s cubic-bezier(0.25, 1, 0.5, 1);
}

.detail-panel--open {
    transform: translateX(0);
}

.detail-panel__close {
    width: 50px;
    height: 50px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0 0 4vh auto;
    padding: 8px;

    color: #000 !important;
    font: inherit;
    font-size: 24px;
    font-weight: bold;

    background: #fff;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    opacity: 1;

    fill: #fff;
    filter: drop-shadow(0.5px 0.5px 5px rgba(255, 255, 255, 0.4));
}

.detail-panel__body {
    flex: 1 1 auto;
    display: flex;
    flex-direction: column;
    justify-content: start;
    gap: 24px;

    h2,
    p {
        margin: 0;
        font-weight: 700;
    }

    h2 {
        font-size: 42px;
        line-height: 56px;
    }

    p {
        font-size: 20px;
        line-height: 40px;

        span {
            font-weight: 300;
        }
    }
}

.cards {
    width: 100%;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: start;
    margin-top: 32px;
    gap: 32px;

    .card1,
    .card2 {
        width: fit-content;
        display: flex;
        flex-direction: column;
        padding: 16px;

        border-radius: 8px;

        h4 {
            font-size: 28px;
            font-weight: 700;
            line-height: 40px;
            margin: 0;
        }
    }
}

.buttons {
    width: 100%;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 5px;
    margin-top: auto;

    .previous-button,
    .next-button,
    .summary-button {
        padding: 8px 32px;
        display: flex;
        flex-direction: row;
        border: none;
        border-radius: 24px;
        cursor: pointer;

        font-size: 24px;
        line-height: 40px;
        font-family: inherit;

        span {
            font-size: 32px;
        }
    }

    .previous-button {
        color: #fff;
        font-weight: 500;

        span {
            margin-right: 16px;
        }
    }

    .next-button,
    .summary-button {
        color: #000;
        background: #fff;
        box-shadow: 1px 1px 5px 0 rgba(255, 255, 255, 0.6);
        font-weight: 600;

        span {
            margin-left: 16px;
        }
    }
}
</style>
