<template>
        <div class="audio-player">
                <audio ref="audioElement" :src="audioSrc" @loadedmetadata="onAudioLoaded"></audio>
                <div class="controls">
                        <button @click="togglePlay">{{ isPlaying ? 'Pause' : 'Play' }}</button>
                </div>
                <div class="waveform-container" ref="waveformContainer">
                        <canvas ref="waveformCanvas"></canvas>
                </div>
        </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue';

export default {
        name: 'AudioPlayer',
        props: {
                audioSrc: {
                        type: String,
                        required: true,
                },
        },
        setup(props) {
                const audioElement = ref(null);
                const waveformContainer = ref(null);
                const waveformCanvas = ref(null);
                const isPlaying = ref(false);
                const audioContext = ref(null);
                const analyser = ref(null);
                const dataArray = ref(null);
                const animationId = ref(null);

                const togglePlay = () => {
                        if (audioElement.value.paused) {
                                audioElement.value.play();
                                isPlaying.value = true;
                                drawWaveform();
                        } else {
                                audioElement.value.pause();
                                isPlaying.value = false;
                                cancelAnimationFrame(animationId.value);
                        }
                };

                const onAudioLoaded = () => {
                        setupAudioContext();
                };

                const setupAudioContext = () => {
                        audioContext.value = new (window.AudioContext || window.webkitAudioContext)();
                        analyser.value = audioContext.value.createAnalyser();
                        const source = audioContext.value.createMediaElementSource(audioElement.value);
                        source.connect(analyser.value);
                        analyser.value.connect(audioContext.value.destination);
                        analyser.value.fftSize = 256;
                        const bufferLength = analyser.value.frequencyBinCount;
                        dataArray.value = new Uint8Array(bufferLength);
                };

                const drawWaveform = () => {
                        const canvas = waveformCanvas.value;
                        const canvasCtx = canvas.getContext('2d');
                        const width = canvas.width;
                        const height = canvas.height;

                        canvasCtx.clearRect(0, 0, width, height);
                        analyser.value.getByteTimeDomainData(dataArray.value);

                        canvasCtx.lineWidth = 2;
                        canvasCtx.strokeStyle = 'rgb(0, 0, 0)';
                        canvasCtx.beginPath();

                        const sliceWidth = width * 1.0 / dataArray.value.length;
                        let x = 0;

                        for (let i = 0; i < dataArray.value.length; i++) {
                                const v = dataArray.value[i] / 128.0;
                                const y = v * height / 2;

                                if (i === 0) {
                                        canvasCtx.moveTo(x, y);
                                } else {
                                        canvasCtx.lineTo(x, y);
                                }

                                x += sliceWidth;
                        }

                        canvasCtx.lineTo(width, height / 2);
                        canvasCtx.stroke();

                        animationId.value = requestAnimationFrame(drawWaveform);
                };

                onMounted(() => {
                        const container = waveformContainer.value;
                        const canvas = waveformCanvas.value;
                        canvas.width = container.offsetWidth;
                        canvas.height = container.offsetHeight;
                });

                onBeforeUnmount(() => {
                        cancelAnimationFrame(animationId.value);
                        if (audioContext.value) {
                                audioContext.value.close();
                        }
                });

                return {
                        audioElement,
                        waveformContainer,
                        waveformCanvas,
                        isPlaying,
                        togglePlay,
                        onAudioLoaded,
                };
        },
};
</script>

<style scoped>
.audio-player {
        width: 100%;
        max-width: 600px;
        margin: 0 auto;
}

.controls {
        margin-bottom: 10px;
}

.waveform-container {
        width: 100%;
        height: 100px;
        background-color: #f0f0f0;
}

canvas {
        width: 100%;
        height: 100%;
}
</style>