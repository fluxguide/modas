<script setup>
import avvLogo from '@img/VRR/Partners/avv.svg';
import zwsLogo from '@img/VRR/Partners/zws.svg';
import vrsLogo from '@img/VRR/Partners/vrs.svg';
import mobilLogo from '@img/VRR/Partners/mobil.svg';
import ruhrBahnLogo from '@img/VRR/Partners/ruhrBahn.svg';
import zrlLogo from '@img/VRR/Partners/zrl.svg';
import rvmLogo from '@img/VRR/Partners/rvm.svg';

const partners = [
    { src: avvLogo, name: 'AVV' },
    { src: zwsLogo, name: 'ZWS' },
    { src: vrsLogo, name: 'VRS' },
    { src: mobilLogo, name: 'Mobil' },
    { src: ruhrBahnLogo, name: 'RuhrBahn' },
    { src: zrlLogo, name: 'ZRL' },
    { src: rvmLogo, name: 'RVM' }
];
</script>

<template>
    <div class="partners">
        <p>Projektpartner:</p>
        <div class="partner-logos">
            <img v-for="(partner, index) in partners" :key="index" :src="partner.src"
                :alt="partner.alt || partner.name || ''" />
        </div>
    </div>
</template>

<style scoped>
.partners {
    position: absolute;
    background-color: white;
    z-index: 5;
    width: fit-content;
    padding: 5px 20px;
    bottom: 0;
    right: 5%;
}

.partners p {
    font-size: 1.1rem;
    font-weight: 600;
}

.partner-logos {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    align-items: center;
    gap: 10px;
}

@media (max-width: 768px) {
    .partners {
        width: 90%;
        left: 50%;
        transform: translateX(-50%);
        right: auto;
        padding: 10px;
    }

    .partners p {
        font-size: 14px;
        margin: 0 0 10px 0;
    }

    .partner-logos img {
        height: 25px;
    }
}
</style>