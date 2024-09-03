<template>
        <n-thing :title="audioFile.title">
                <template #header-extra>
                        <n-button @click="deleteAudioFile" size="small" class="mr-2">
                                <i class="i-fe:trash"></i>
                        </n-button>
                        <n-button @click="toggleCollapse" size="small">
                                <i :class="collapsed ? 'i-fe:chevron-down' : 'i-fe:chevron-up'"></i>
                        </n-button>
                </template>
                <template #description>
                        <div v-show="!collapsed">
                                <div v-for="chunk in audioFile.chunks" :key="chunk.id">
                                        <n-card class="mb-4">
                                                <div class="flex justify-between">
                                                        <div class="flex items-center">
                                                                <h2>
                                                                        <span>{{ formatTime(chunk.start)
                                                                                }} - {{
                                                                                        formatTime(chunk.end) }}
                                                                        </span>
                                                                </h2>
                                                        </div>
                                                        <div class="flex items-center">
                                                                <router-link :to="`/base/practice/${chunk.id}`"
                                                                        class="practice-link">
                                                                        <h2> <i class="i-fe:arrow-up-right"></i>
                                                                        </h2>
                                                                </router-link>
                                                        </div>


                                                </div>
                                                <div>
                                                        <AudioPlayer :chunk-media="chunk.media" />
                                                </div>
                                                <div v-html="chunk.note"></div>
                                        </n-card>

                                </div>
                        </div>
                </template>
        </n-thing>
</template>



<script setup lang="ts">
import { ref } from 'vue'
import AudioPlayer from './AudioPlayer.vue';
import api from '../services/api';

const emit = defineEmits(['file-deleted']);


interface AudioFile {
        id: number
        title: string
        chunks: any
}

const props = defineProps<{
        audioFile: AudioFile
}>()

const collapsed = ref(true)

const toggleCollapse = () => {
        collapsed.value = !collapsed.value
}


const formatTime = (seconds) => {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = Math.floor(seconds % 60);
        return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
};

const deleteAudioFile = () => {
        console.log('Delete audio file:', props.audioFile.id);
        api.deleteAudioFile(props.audioFile.id)
        console.log('file deleted')
        emit('file-deleted');
};
</script>
