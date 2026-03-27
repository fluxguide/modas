<script setup>
defineProps({
    phaseTitle: {
        type: String,
        required: true
    },
    phaseDescription: {
        type: String,
        required: true
    },
    characterImage: {
        type: String,
        required: true
    },
    characterAlt: {
        type: String,
        required: true
    },
    phaseClass: {
        type: String,
        default: 'phase1'
    }
});
</script>

<template>
    <div class="phase-card" :class="phaseClass">
        <div class="phase-text">
            <h1 class="phase-heading">{{ phaseTitle }}</h1>
            <h1><span>{{ phaseDescription }}</span></h1>
        </div>
        <img :src="characterImage" :alt="characterAlt">
    </div>
</template>

<style scoped>
.phase-card {
    height: 100%;
    width: 23%;
    position: absolute;
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: rgba(255, 255, 255, 0.6);
    border-radius: 15px;
    overflow: hidden;
    box-sizing: border-box;
}

.phase1 {
    left: 28%;
}

.phase2 {
    right: 24%;
}

.phase-card h1 {
    padding: 0rem 1rem;
    margin: 15px 0 0 0;
    word-wrap: break-word;
    overflow-wrap: break-word;
    hyphens: auto;
    text-align: left;
    width: fit-content;
    box-sizing: border-box;
}

.phase-card h1 span {
    font-weight: 400;
}

.phase-text {
    width: 100%;
}

.phase-heading {
    color: #760B5A;
    background-color: white;
    width: fit-content;
    border-radius: 0 10px 10px 0;
}

.phase-card img {
    position: absolute;
    bottom: 10%;
    width: 90%;
    max-height: 50%;
}

@media (max-width: 768px) {
    .phase-card {
        width: 70%;
        height: fit-content;
        margin: 0;
        align-items: start;
        flex-direction: row;
        padding: 10px 10px 10px 0;
    }

    .phase1 {
        top: 23vh;
    }

    .phase2 {
        top: 43vh;
    }

    .phase1,
    .phase2 {
        left: auto;
        right: 5%;
    }

    .phase-card h1 {
        font-size: 16px;
    }

    .phase-card h1 span {
        font-size: 14px;
    }

    .phase-text {
        width: 50%;
    }

    .phase-card img {
        position: relative;
        bottom: auto;
        width: 50%;
        height: 15vh;
        max-height: none;
        margin: 0;
    }
}
</style>