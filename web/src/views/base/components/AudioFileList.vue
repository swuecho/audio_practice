<template>
        <div class="m-8">
                <h2>Uploaded Audio Files</h2>
                <n-list>
                        <n-list-item v-for="file in audioFiles" :key="file.id">
                              <AudioFileAndChunks :audio-file="file">  </AudioFileAndChunks>
                        </n-list-item>
                </n-list>
        </div>
</template>

<script setup>
import AudioFileAndChunks from './AudioFileAndChunks.vue';

const props = defineProps({
        audioFiles: {
                type: Array,
                required: true
        }
});


</script>