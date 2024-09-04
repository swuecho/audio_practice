<template>
        <div>
                <n-button @click="requestPermission" v-if="!permissionGranted">Allow Microphone Access</n-button>
                <template v-else>
                        <div>
                                
                                <div v-if="!isRecording">
                                        <audio v-if="audioUrl" :src="audioUrl" controls></audio>
                                </div>
                                <n-input v-model:value="customFileName" placeholder="Enter file name (optional)" />
                                <div class="flex gap-4 justify-center mt-8">
                                        <n-button @click="startRecording" :disabled="isRecording || isPaused">Start
                                                Recording</n-button>
                                        <n-button @click="pauseResumeRecording" :disabled="!isRecording && !isPaused">
                                                {{ isPaused ? 'Resume' : 'Pause' }}
                                        </n-button>
                                        <n-button @click="stopRecording" :disabled="!isRecording && !isPaused">Stop
                                                Recording</n-button>
                                        <n-button @click="uploadRecording" :disabled="!audioUrl || isUploading">
                                                {{ isUploading ? 'Uploading...' : 'Upload Recording' }}
                                        </n-button>
                                </div>
                                <div v-if="isUploading" class="uploading-indicator">
                                        <i class="i-fe:loader" /> Uploading...
                                </div>
                                <div v-if="isRecording" class="recording-indicator">
                                        <i class="i-fe:loader" /> Recording... {{ formattedRecordingTime }}
                                </div>
                        </div>

                </template>
                <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
        </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '../services/api';

const isRecording = ref(false);
const audioUrl = ref(null);
const permissionGranted = ref(false);
const errorMessage = ref('');
let mediaRecorder = null;
let audioChunks = [];
const customFileName = ref('');
const isPaused = ref(false);
let mediaStream = null;
const isUploading = ref(false);

const recordingStartTime = ref(null);
const recordingTime = ref(0);

onMounted(() => {
        // Check if permission is already granted
        navigator.permissions.query({ name: 'microphone' }).then((result) => {
                if (result.state === 'granted') {
                        permissionGranted.value = true;
                }
        }).catch(error => {
                console.error('Error querying microphone permission:', error);
        });
});

const emit = defineEmits(['recording-uploaded']);

const checkBrowserSupport = () => {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                throw new Error('Media devices API not supported in this browser.');
        }
};

const checkSecureContext = () => {
        if (!window.isSecureContext) {
                throw new Error('Application must be run in a secure context (HTTPS or localhost).');
        }
};

const requestPermission = async () => {
        try {
                errorMessage.value = '';
                checkBrowserSupport();
                checkSecureContext();

                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                permissionGranted.value = true;
                stream.getTracks().forEach(track => track.stop()); // Stop the stream after getting permission
                console.log('Microphone permission granted');
        } catch (error) {
                console.error('Error requesting microphone permission:', error);
                handleError(error);
        }
};

const startRecording = async () => {
        try {
                errorMessage.value = '';
                mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(mediaStream);
                audioChunks = [];

                mediaRecorder.ondataavailable = (event) => {
                        audioChunks.push(event.data);
                };

                mediaRecorder.onstop = () => {
                        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                        audioUrl.value = URL.createObjectURL(audioBlob);
                };

                mediaRecorder.start();
                isRecording.value = true;
                isPaused.value = false;
                recordingStartTime.value = Date.now();
                updateRecordingTime();
        } catch (error) {
                console.error('Error starting recording:', error);
                handleError(error);
        }
};

const updateRecordingTime = () => {
        if (isRecording.value && !isPaused.value) {
                recordingTime.value = Math.floor((Date.now() - recordingStartTime.value) / 1000);
                setTimeout(updateRecordingTime, 1000);
        }
};

const pauseResumeRecording = () => {
        if (!mediaRecorder) return;

        if (isPaused.value) {
                mediaRecorder.resume();
                isPaused.value = false;
                isRecording.value = true;
                recordingStartTime.value = Date.now() - recordingTime.value * 1000;
                updateRecordingTime();
        } else {
                mediaRecorder.pause();
                isPaused.value = true;
                isRecording.value = false;
        }
};

const stopRecording = () => {
        if (mediaRecorder) {
                mediaRecorder.stop();
                isRecording.value = false;
                isPaused.value = false;
                recordingTime.value = 0;
                if (mediaStream) {
                        mediaStream.getTracks().forEach(track => track.stop());
                }
        }
};

const uploadRecording = async () => {
        if (!audioUrl.value) return;

        try {
                isUploading.value = true;
                const response = await fetch(audioUrl.value);
                const blob = await response.blob();
                const fileName = customFileName.value
                        ? `${customFileName.value}.wav`
                        : `recording-${Date.now()}.wav`;
                await api.uploadAudio(blob, fileName);
                emit('recording-uploaded');
                customFileName.value = ''; // Reset the input after successful upload
        } catch (error) {
                console.error('Error uploading recording:', error);
                errorMessage.value = 'Failed to upload recording. Please try again.';
        } finally {
                isUploading.value = false;
                audioUrl.value = null;
        }
};

const handleError = (error) => {
        if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
                errorMessage.value = 'Microphone permission was denied. Please allow microphone access in your browser settings and try again.';
        } else if (error.name === 'NotFoundError' || error.name === 'DevicesNotFoundError') {
                errorMessage.value = 'No microphone found. Please connect a microphone and try again.';
        } else if (error.name === 'NotSupportedError') {
                errorMessage.value = 'Your browser does not support audio recording. Please try a different browser.';
        } else {
                errorMessage.value = `Unable to access the microphone: ${error.message}. Please check your browser settings and try again.`;
        }
};

const formattedRecordingTime = computed(() => {
        const minutes = Math.floor(recordingTime.value / 60);
        const seconds = recordingTime.value % 60;
        return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
});


</script>

<style scoped>
.error-message {
        color: red;
        margin-top: 10px;
}

@keyframes blink {
        0% {
                opacity: 1;
        }

        50% {
                opacity: 0;
        }

        100% {
                opacity: 1;
        }
}

.uploading-indicator {
        color: #2196f3;
        font-size: 18px;
        margin-top: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
}
.recording-indicator {
        color: #ff4136;
        font-size: 18px;
        margin-top: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
}

.uploading-indicator i {
        margin-right: 8px;
        animation: spin 1s linear infinite;
}

.recording-indicator i {
        margin-right: 8px;
        animation: spin 1s linear infinite;
}

@keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
}
</style>