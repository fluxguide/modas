<template>
    <div class="section-wrapper" :class="wrapperClass">
        <slot name="background"></slot>
        <div class="coloured-space" :class="colouredClass">
            <div class="white-space" :class="whiteSpaceClass">
                <slot></slot>
            </div>
        </div>
        <slot name="extra"></slot>
    </div>
</template>

<script setup>
defineProps({
    wrapperClass: {
        type: String,
        default: ''
    },
    colouredClass: {
        type: String,
        default: ''
    },
    whiteSpaceClass: {
        type: String,
        default: ''
    }
});
</script>

<style scoped>
.section-wrapper {
    position: relative;
    width: 100%;
}

.coloured-space {
    width: 55%;
    height: fit-content;
    display: flex;
    align-items: center;
    justify-content: center;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    padding: 30px 20px;
    background-image: linear-gradient(rgba(255, 255, 255, 0.75), rgba(115, 245, 70, 0.75), rgba(114, 219, 255, 0.75));
    border-radius: 20px;
    pointer-events: none;
    z-index: 3;
}

.white-space {
    width: 95%;
    height: 90%;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    gap: 7%;
    background-color: white;
    border-radius: 20px;
    padding: 40px;
}

.robot-form-wrapper {
    width: 60%;
}

.robot-form-coloured {
    width: 80%;
    height: fit-content;
    transform: none;
    top: 5%;
    left: 5%;
}

.robot-form-white {
    flex-direction: column;
    background-color: rgba(255, 255, 255, 0.75);
    align-items: center;
    justify-content: center;
    gap: 2.5rem;
    pointer-events: auto;
}

.robot-chatbot-wrapper {
    margin-top: 10%;
}

.robot-coloured {
    width: 100%;
    height: fit-content;
}

.robot-white {
    padding: 0 10px;
}

@media (max-width: 768px) {
    .coloured-space {
        margin-top: -5vh;
        width: 80%;
        padding: 20px 10px;
    }

    .white-space {
        flex-direction: column;
        height: fit-content;
        gap: 1rem;
        padding: 15px 20px;
    }

    .robot-form-wrapper {
        width: 80vw !important;
        align-self: center;
    }

    .robot-form-coloured {
        width: 100%;
        top: -25%;
        left: 0;
        transform: none;
    }

    .robot-chatbot-wrapper {
        margin-top: 20%;
    }

    .robot-coloured {
        width: 80vw;
        height: auto;
        left: 10%;
        z-index: 2;
    }

    .robot-white {
        padding: 10px;
    }
}
</style>