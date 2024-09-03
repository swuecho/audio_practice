<template>
  <div class="h-screen flex flex-col">
    <header class="m-4 p-4">
      <h1 class="font-bold mb-4">Add Audio</h1>
      <div class="mt-20 ml-20">
        <n-tabs>
          <n-tab-pane name="record" tab="Record Audio">
            <AudioRecorder @recording-uploaded="refreshAudioFiles" />
          </n-tab-pane>
          <n-tab-pane name="upload" tab="Upload File">
            <FileUpload @file-uploaded="refreshAudioFiles" />
          </n-tab-pane>
        </n-tabs>
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
import AudioRecorder from './components/AudioRecorder.vue';
import api from './services/api';

const audioFiles = ref([]);

const fetchAudioFiles = async () => {
  const response = await api.getAudioFiles();
  audioFiles.value = response;
};

const refreshAudioFiles = () => {
  fetchAudioFiles();
};

onMounted(() => {
  fetchAudioFiles();
});
</script>
