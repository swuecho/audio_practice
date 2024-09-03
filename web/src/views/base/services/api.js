import { request } from "@/utils"
export default {
        uploadAudio(file, fileName) {
                const formData = new FormData();
                formData.append('file', file, fileName);
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
        async deleteAudioFile(fileId) {
                await request.delete(`/audio/file/${fileId}`)
        },
        getAudioChunk(id) {
                return request.get(`/audio/chunk/${id}/`)
        },

        async audioChunkTranscript(id) {
                return request.post(`/audio/chunk/transcript/${id}/`)
        }
};
