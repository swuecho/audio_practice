<template>
        <div>
                <audio ref="player" :src="audioSrc" controls />
                <canvas ref="canvas" />
        </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAVWaveform } from 'vue-audio-visual'

const props = defineProps({
        audioSrc: {
                type: String,
                required: true
        }
});

const player = ref(null)
const canvas = ref(null)

useAVWaveform(player, canvas, { src: props.audioSrc, playtimeWithMs: false })
</script>