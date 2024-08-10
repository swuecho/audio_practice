import axios from 'axios';

const API_URL = '/api';

export default {
        uploadAudio(file) {
                const formData = new FormData();
                formData.append('file', file);
                return axios.post(`${API_URL}/upload/`, formData, {
                        headers: {
                                'Content-Type': 'multipart/form-data'
                        }
                }
                );
        },
        getAudioFiles() {
                return axios.get(`${API_URL}/audio-files/`);
        },
        getAudioChunk(id) {
                return axios.get(`${API_URL}/audio/chunk/${id}/`)
        },

        async audioChunkTranscript(id) {
                return axios.post(`${API_URL}/audio/chunk/transcript/${id}/`)
        }
};
