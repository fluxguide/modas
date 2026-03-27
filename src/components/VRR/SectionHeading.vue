<script setup>
defineProps({
    showLogo: {
        type: Boolean,
        default: false
    }
});
</script>

<template>
    <div class="heading" :class="{ 'heading-first': showLogo }">
        <h1>
            <slot></slot>
        </h1>
        <img v-if="showLogo" id="logo" src="@img/VRR/Logo.svg" alt="VRR Logo" />
    </div>
</template>

<style scoped>
.heading-first #logo {
    width: 3%;
    margin-right: 2%;
}

.heading-first #logo,
.heading-first h1 {
    z-index: 2;
}

.heading-first {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
}

.heading-first,
.heading {
    width: 100%;
    height: fit-content;
    display: flex;
    position: sticky;
    top: 0;
    align-items: center;
    color: white;
    margin: 5% 0 5% 0;
    z-index: 12;
}

.heading-first h1,
.heading h1 {
    width: 60%;
    background-color: #760B5A;
    padding: 0.5rem 0 0.5rem 2rem;
    border-radius: 0 10px 10px 0;
}

@media (max-width: 768px) {

    .heading-first h1,
    .heading h1 {
        width: 70%;
        height: 50px;
        font-size: 18px;
        padding-left: 1rem;
    }

    .heading-first #logo {
        width: 10%;
        margin-right: 5%;
    }
}
</style>