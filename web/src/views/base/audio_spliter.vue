<template>
  <div class="h-screen flex flex-col">
    <header class="m-4 p-4">
      <h1 class="font-bold mb-4">Audio File Splitter</h1>
      <div class="mt-20 ml-20">
      <FileUpload @file-uploaded="refreshAudioFiles" />
</div>
    </header>
    <main class="flex-grow overflow-hidden">
      <div ref="audioListContainer" class="h-full overflow-y-auto p-4">
        <AudioFileList :audio-files="audioFiles" />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import FileUpload from './components/FileUpload.vue';
import AudioFileList from './components/AudioFileList.vue';
import api from './services/api';

const audioFiles = ref([]);

const fetchAudioFiles = async () => {
  const response = await api.getAudioFiles();
  audioFiles.value = response.data;
};

const refreshAudioFiles = () => {
  fetchAudioFiles();
};

onMounted(() => {
  fetchAudioFiles();
});
</script>
