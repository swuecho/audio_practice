<template>
        <n-thing :title="audioFile.title">
                <template #header-extra>
                        <n-button @click="showEditDialog" size="small" class="mr-2">
                                <i class="i-fe:edit-2"></i>
                        </n-button>
                        <n-button @click="confirmDelete" size="small" class="mr-2">
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
  <EditAudioFileDialog
    v-model:show="showDialog"
    title="Edit Audio File Title"
    :initial-title="audioFile.title"
    @save="updateAudioFileTitle"
  />
</template>



<script setup lang="ts">
import { ref, h } from 'vue'
import { useDialog, useMessage } from 'naive-ui'
import AudioPlayer from './AudioPlayer.vue';
import EditAudioFileDialog from './EditAudioFileDialog.vue';
import api from '../services/api';

const emit = defineEmits(['file-deleted', 'file-updated']);

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

const dialog = useDialog()
const message = useMessage()
const showDialog = ref(false)

const showEditDialog = () => {
        showDialog.value = true
}

const updateAudioFileTitle = async (newTitle: string) => {
        try {
                await api.updateAudioFileTitle(props.audioFile.id, newTitle)
                emit('file-updated', { id: props.audioFile.id, title: newTitle })
                message.success('Title updated successfully')
        } catch (error) {
                console.error('Error updating audio file title:', error)
                message.error('Failed to update title')
        }
}

const confirmDelete = () => {
        dialog.warning({
                title: 'Confirm Deletion',
                content: `Are you sure you want to delete "${props.audioFile.title}"?`,
                positiveText: 'Delete',
                negativeText: 'Cancel',
                onPositiveClick: () => {
                        deleteAudioFile()
                }
        })
}

const deleteAudioFile = async () => {
        console.log('Delete audio file:', props.audioFile.id);
        await api.deleteAudioFile(props.audioFile.id)
        console.log('file deleted')
        emit('file-deleted');
};
</script>
