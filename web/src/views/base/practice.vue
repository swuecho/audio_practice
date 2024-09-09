<template>
  <div class="h-screen flex flex-col">
    <main class="flex-grow overflow-hidden">
      <n-card>
        <div class="flex justify-between">
          <div>{{ normalChunkName(chunkFile.media) }}</div>
          <div class="flex gap-4">
            <n-button v-if="totalChunks > 1 && !isFirstChunk" @click="navigateChunk('prev')">Prev</n-button>
            <n-button v-if="totalChunks > 1 && !isLastChunk" @click="navigateChunk('next')">Next</n-button>
          </div>
        </div>
        <div>
          <audio controls :src="audioSrc"></audio>
        </div>

        <div>
          <n-button v-if="!transcript" type="primary" @click="transcribeAudio">Transcribe</n-button>
        </div>
      </n-card>
      <div class="container h-full">
        <div class="content-section">
          <div v-if="loading">
            <n-spin></n-spin>
          </div>

          <div v-if="transcript" class="transcript-content">
            <h3>Transcript:</h3>
            <div v-html="transcript"></div>
          </div>
        </div>

        <div class="editor-section h-full overflow-y-auto">
          <h3>Note:</h3>
          <tiptap-editor :audio-chunk-id="chunkId" />
        </div>
      </div>


    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
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
  //audioSrc.value = chunkFile.value.media
  console.log(audioSrc.value)
  transcript.value = chunkFile.value.transcript;
};

const normalChunkName = (name) => {
  return name?.replace('/media/chunks/', '')
}

const router = useRouter();

const navigateChunk = (direction) => {
  const currentId = parseInt(chunkId);
  const newId = direction === 'next' ? currentId + 1 : currentId - 1;
  const newIndex = direction === 'next' ? parseInt(route.query.index) + 1 : parseInt(route.query.index) - 1;
  router.push({ name: 'AUDIO_PRACTICE', params: { id: newId.toString() }, query: { index: newIndex, total: totalChunks.value } });
};

onMounted(() => {
  fetchAudioChunk(chunkId)
}
)

const totalChunks = computed(() => {
  return route.query.total
})

const isFirstChunk = computed(() => {
  const chunkIndex = parseInt(route.query.index)
  console.log(chunkIndex)
  return chunkIndex === 0
})

const isLastChunk = computed(() => {
  const chunkIndex = parseInt(route.query.index)
  const chunkTotal = parseInt(route.query.total)
  return chunkIndex === chunkTotal - 1
})

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

.editor-section,
.content-section {
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
