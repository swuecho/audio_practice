<template>
        <AVWaveform :src="audioSrc" :playtime-with-ms="false"></AVWaveform>
</template>

<script setup>
import { AVWaveform } from 'vue-audio-visual'

const props = defineProps({
        audioSrc: {
                type: String,
                required: true
        }
});


</script>