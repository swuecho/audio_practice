import { request } from "@/utils"
export default {
        async uploadAudio(file, fileName) {
                const formData = new FormData();
                formData.append('file', file, fileName);
                return await request.post(`/upload/`, formData, {
                        headers: {
                                'Content-Type': 'multipart/form-data'
                        }
                }
                );
        },
        async getAudioFiles() {
                return await request.get(`/audio-files/`);
        },
        async deleteAudioFile(fileId) {
                return await request.delete(`/audio/file/${fileId}`)
        },
        async getAudioChunk(id) {
                return await request.get(`/audio/chunk/${id}/`)
        },

        async audioChunkTranscript(id) {
                return await request.post(`/audio/chunk/transcript/${id}/`)
        }
};
