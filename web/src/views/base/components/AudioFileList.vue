<template>
        <div class="m-8">
                <h2>Uploaded Audio Files</h2>
                <n-list>
                        <n-list-item v-for="file in audioFiles" :key="file.id">
                              <AudioFileAndChunks :audio-file="file"  @file-deleted="onFileDeleted">  </AudioFileAndChunks>
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

const emit = defineEmits(['file-deleted']);

const onFileDeleted = () => {
        console.log('file deleted emited from AudioFileList')
  emit('file-deleted');
};

</script>