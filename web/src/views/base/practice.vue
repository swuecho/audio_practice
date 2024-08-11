<template>
  <div class="h-screen flex flex-col">
    <main class="flex-grow overflow-hidden">
      <n-card>
        <div>{{ normalChunkName(chunkFile.media) }}</div>
        <AudioPlayerWave :audioSrc="chunkFile.media" />
        <div>
          <n-button v-if="!transcript" type="primary" @click="transcribeAudio">Transcribe</n-button>
        </div>
      </n-card>
      <div v-if="transcript" class="px-30 py-10">
        <h3>Transcript:</h3>
        <div v-html="transcript"></div>
      </div>
      <div v-if="loading">
        <n-spin></n-spin>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import AudioPlayerWave from './components/AudioPlayerWave.vue';
import AudioPlayerClaude from './components/AudioPlayerClaude.vue';
import api from './services/api';
const route = useRoute()
const chunkId = route.params.id
const chunkFile = ref({
  media: ''
});

const transcript = ref('')
const loading = ref(false)

const fetchAudioChunk = async (chunkId) => {
  const response = await api.getAudioChunk(chunkId);
  chunkFile.value = response.data;
  transcript.value = chunkFile.value.transcript;
};

const normalChunkName = (name) => {
  return name?.replace('/media/chunks/', '')
}

onMounted(() => {
  fetchAudioChunk(chunkId)
}
)


const transcribeAudio = async () => {
  try {
    loading.value = true
    const response = await api.audioChunkTranscript(chunkId);
    console.log(response)
    transcript.value = response.data.text;
  } catch (error) {
    console.error('Error during transcription:', error);
  } finally {
    loading.value = false
  }
};
</script>
