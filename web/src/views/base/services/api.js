import { request } from "@/utils"
export default {
        uploadAudio(file) {
                const formData = new FormData();
                formData.append('file', file);
                return request.post(`/upload/`, formData, {
                        headers: {
                                'Content-Type': 'multipart/form-data'
                        }
                }
                );
        },
        getAudioFiles() {
                return request.get(`/audio-files/`);
        },
        getAudioChunk(id) {
                return request.get(`/audio/chunk/${id}/`)
        },

        async audioChunkTranscript(id) {
                return request.post(`/audio/chunk/transcript/${id}/`)
        }
};
