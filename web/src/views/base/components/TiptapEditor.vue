<template>
        <div class="tiptap-editor">
                <editor-content :editor="editor" />
                <p v-if="saving">Saving...</p>
                <p v-if="error" class="error">{{ error }}</p>
        </div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { Editor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import { request } from '@/utils'

import { debounce } from 'lodash'

const props = defineProps<{
        audioChunkId: number
}>()

const editor = ref<Editor | null>(null)
const saving = ref(false)
const error = ref('')

const saveContent = debounce(async (content: string) => {
        saving.value = true
        error.value = ''
        try {
                await request.put(`/audio-notes/${props.audioChunkId}/`, {
                        text: content,
                        chunk: props.audioChunkId
                })
        } catch (err) {
                console.error('Failed to save content:', err)
                error.value = 'Failed to save content. Please try again.'
        } finally {
                saving.value = false
        }
}, 1000)

onMounted(async () => {
        try {
                const response = await request.get(`/audio-notes/${props.audioChunkId}/`)
                const initialContent = response.data.text || '<p>Start typing here...</p>'

                editor.value = new Editor({
                        extensions: [StarterKit],
                        content: initialContent,
                        autofocus: true,
                        editable: true,
                        onUpdate: ({ editor }) => {
                                saveContent(editor.getHTML())
                        }
                })
        } catch (err) {
                console.error('Failed to fetch initial content:', err)
                error.value = 'Failed to load initial content. Please refresh the page.'
        }
})

onBeforeUnmount(() => {
        editor.value?.destroy()
})
</script>

<style scoped>
.tiptap-editor {
        border: 1px solid #ccc;
        border-radius: 4px;
        padding: 10px;
}

.error {
        color: red;
}
</style>