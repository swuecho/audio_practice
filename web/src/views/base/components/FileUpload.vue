<template>
    <n-space vertical>
        <n-input v-model:value="fileName" placeholder="Enter file name (optional)" />
        <n-upload action="#" :custom-request="customRequest" accept="audio/*" :max="1" @finish="handleFinish">
            <n-button>Upload Audio File</n-button>
        </n-upload>
    </n-space>
</template>

<script setup>
import { ref } from 'vue';
import api from '../services/api';

const emit = defineEmits(['file-uploaded']);
const fileName = ref('');

const customRequest = async ({ file, onFinish, onError }) => {
    const uploadName = fileName.value || file.name;
    await api.uploadAudio(file.file, uploadName)
        .then(() => {
            onFinish();
            emit('file-uploaded');
        })
        .catch((error) => {
            console.error('Upload failed:', error);
            onError();
        });
};

const handleFinish = () => {
        console.log('File uploaded successfully');
};
</script>