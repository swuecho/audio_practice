<template>
  <div class="h-screen flex flex-col">
    <main class="flex-grow overflow-hidden">
      <n-card>
        <div>{{ normalChunkName(chunkFile.media) }}</div>
        <AudioPlayer :audioSrc="audioSrc" />
        <div>
          <n-button v-if="!transcript" type="primary" @click="transcribeAudio">Transcribe</n-button>
        </div>
      </n-card>
      <div class="container">
        <div class="content-section">
          <div v-if="loading">
            <n-spin></n-spin>
          </div>

          <div v-if="transcript" class="transcript-content">
            <h3>Transcript:</h3>
            <div v-html="transcript"></div>
          </div>
        </div>

        <div class="editor-section">
          <h3>Note:</h3>
          <tiptap-editor :audio-chunk-id="chunkId" />
        </div>
      </div>


    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import AudioPlayer from '@/components/AudioPlayer.vue';
import TiptapEditor from './components/TiptapEditor.vue'
import api from './services/api';
const route = useRoute()
const chunkId = route.params.id
const chunkFile = ref({
  media: ''
});
const audioSrc = ref('')
const transcript = ref('')
const loading = ref(false)

const fetchAudioChunk = async (chunkId) => {
  const response = await api.getAudioChunk(chunkId);
  chunkFile.value = response;
  audioSrc.value = `${window.location.origin}${chunkFile.value.media}`
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
    transcript.value = response.text;
  } catch (error) {
    console.error('Error during transcription:', error);
  } finally {
    loading.value = false
  }
};
</script>

<style lang="scss">
.container {
  display: flex;
  gap: 20px;
  height: calc(100vh - 250px);
}

.editor-section, .content-section {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.transcript-content {
  flex-grow: 1;
  overflow-y: auto;
  padding: 0 30px 10px;
}

</style>
