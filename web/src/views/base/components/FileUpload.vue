<template>
        <n-upload action="#" :custom-request="customRequest" accept="audio/*" :max="1" @finish="handleFinish">
                <n-button>Upload Audio File</n-button>
        </n-upload>
</template>

<script setup>
import api from '../services/api';

const emit = defineEmits(['file-uploaded']);

const customRequest = ({ file, onFinish, onError }) => {
        api.uploadAudio(file.file)
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