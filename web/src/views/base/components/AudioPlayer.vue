<template>
        <audio controls :src="audioSrc"></audio>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps({

        chunkMedia: {
                type: String,
                required: true
        }
});

const audioSrc = computed(() => {
        return  props.chunkMedia;
});

</script>