<template>
        <div class="tiptap-editor">
                <div v-if="editor">
                        <button :disabled="!editor.can().chain().focus().toggleBold().run()"
                                class="m-1 inline-flex items-center rounded-md bg-indigo-50 px-2 py-1 text-md font-medium text-indigo-700 ring-1 ring-inset ring-indigo-700/10"
                                :class="{ 'ring-indigo-900 ring-2': editor.isActive('bold') }"
                                @click="editor.chain().focus().toggleBold().run()" v-text="'bold'" />
                        <button :disabled="!editor.can().chain().focus().toggleItalic().run()"
                                class="m-1 inline-flex items-center rounded-md bg-indigo-50 px-2 py-1 text-md font-medium text-indigo-700 ring-1 ring-inset ring-indigo-700/10"
                                :class="{ 'ring-indigo-900 ring-2': editor.isActive('italic') }"
                                @click="editor.chain().focus().toggleItalic().run()" v-text="'italic'" />
                        <button :disabled="!editor.can().chain().focus().toggleStrike().run()"
                                class="m-1 inline-flex items-center rounded-md bg-indigo-50 px-2 py-1 text-md font-medium text-indigo-700 ring-1 ring-inset ring-indigo-700/10"
                                :class="{ 'ring-indigo-900 ring-2': editor.isActive('strike') }"
                                @click="editor.chain().focus().toggleStrike().run()" v-text="'strike'" />
                        <button class="m-1 inline-flex items-center rounded-md bg-indigo-50 px-2 py-1 text-md font-medium text-indigo-700 ring-1 ring-inset ring-indigo-700/10"
                                :class="{ 'ring-indigo-900 ring-2': editor.isActive('paragraph') }"
                                @click="editor.chain().focus().setParagraph().run()" v-text="'paragraph'" />
                        <button class="m-1 inline-flex items-center rounded-md bg-indigo-50 px-2 py-1 text-md font-medium text-indigo-700 ring-1 ring-inset ring-indigo-700/10"
                                :class="{ 'ring-indigo-900 ring-2': editor.isActive('heading', { level: 1 }) }"
                                @click="editor.chain().focus().toggleHeading({ level: 1 }).run()" v-text="'h1'" />
                        <button class="m-1 inline-flex items-center rounded-md bg-indigo-50 px-2 py-1 text-md font-medium text-indigo-700 ring-1 ring-inset ring-indigo-700/10"
                                :class="{ 'ring-indigo-900 ring-2': editor.isActive('heading', { level: 2 }) }"
                                @click="editor.chain().focus().toggleHeading({ level: 2 }).run()" v-text="'h2'" />
                        <button class="m-1 inline-flex items-center rounded-md bg-indigo-50 px-2 py-1 text-md font-medium text-indigo-700 ring-1 ring-inset ring-indigo-700/10"
                                :class="{ 'ring-indigo-900 ring-2': editor.isActive('heading', { level: 3 }) }"
                                @click="editor.chain().focus().toggleHeading({ level: 3 }).run()" v-text="'h3'" />
                        <button class="m-1 inline-flex items-center rounded-md bg-indigo-50 px-2 py-1 text-md font-medium text-indigo-700 ring-1 ring-inset ring-indigo-700/10"
                                :class="{ 'ring-indigo-900 ring-2': editor.isActive('bulletList') }"
                                @click="editor.chain().focus().toggleBulletList().run()" v-text="'bullet list'" />
                        <button class="m-1 inline-flex items-center rounded-md bg-indigo-50 px-2 py-1 text-md font-medium text-indigo-700 ring-1 ring-inset ring-indigo-700/10"
                                :class="{ 'ring-indigo-900 ring-2': editor.isActive('orderedList') }"
                                @click="editor.chain().focus().toggleOrderedList().run()" v-text="'ordered list'" />
                        <button class="m-1 inline-flex items-center rounded-md bg-indigo-50 px-2 py-1 text-md font-medium text-indigo-700 ring-1 ring-inset ring-indigo-700/10"
                                :class="{ 'ring-indigo-900 ring-2': editor.isActive('blockquote') }"
                                @click="editor.chain().focus().toggleBlockquote().run()" v-text="'blockquote'" />
                        <button class="m-1 inline-flex items-center rounded-md bg-indigo-50 px-2 py-1 text-md font-medium text-indigo-700 ring-1 ring-inset ring-indigo-700/10"
                                @click="editor.chain().focus().setHorizontalRule().run()" v-text="'horizontal rule'" />
                        <button class="m-1 inline-flex items-center rounded-md bg-indigo-50 px-2 py-1 text-md font-medium text-indigo-700 ring-1 ring-inset ring-indigo-700/10"
                                @click="editor.chain().focus().setHardBreak().run()" v-text="'hard break'" />
                        <button class="m-1 inline-flex items-center rounded-md bg-indigo-50 px-2 py-1 text-md font-medium text-indigo-700 ring-1 ring-inset ring-indigo-700/10"
                                :disabled="!editor.can().chain().focus().undo().run()"
                                @click="editor.chain().focus().undo().run()">
                                <i class="i-fe:corner-up-left" />
                        </button>
                        <button class="m-1 inline-flex items-center rounded-md bg-indigo-50 px-2 py-1 text-md font-medium text-indigo-700 ring-1 ring-inset ring-indigo-700/10"
                                :disabled="!editor.can().chain().focus().redo().run()"
                                @click="editor.chain().focus().redo().run()">
                                <i class="i-fe:corner-down-right" />
                        </button>
                </div>
                <editor-content :editor="editor" />
                <p v-if="saving">Saving...</p>
                <p v-if="error" class="error">{{ error }}</p>
        </div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { Editor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Highlight from '@tiptap/extension-highlight'
import Typography from '@tiptap/extension-typography'
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
                const chunk_response = await request.get(`/audio/chunk/${props.audioChunkId}/`)
                await request.put(`/audio-notes/${chunk_response.note_id}/`, {
                        text: content,
                        chunk: props.audioChunkId
                })
        } catch (err) {
                console.error('Failed to save content:', err)
                error.value = 'Failed to save content. Please try again.'
        } finally {
                saving.value = false
        }
}, 2000)

onMounted(async () => {
        try {
                let chunk_response = await request.get(`/audio/chunk/${props.audioChunkId}/`)
                let note_id = 0;
                if (chunk_response.note_id) {
                        note_id = chunk_response.note_id
                } else {
                        const note_response = await request.post('/audio-notes/', {
                                text: "start typing here...",
                                chunk: props.audioChunkId
                        })
                        note_id = note_response.id
                }
                const resp = await request.get(`/audio-notes/${note_id}/`)
                const initialContent = resp.text || '<p>Start typing here...</p>'

                editor.value = new Editor({
                        extensions: [StarterKit, Highlight,
                                Typography,],
                        content: initialContent,
                        autofocus: true,
                        editable: true,
                        editorProps: {
                                attributes: {
                                        class: 'w-full prose my-6 mx-auto focus:outline-none',
                                },
                        },
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

<style lang="scss">
/* Basic editor styles */
.tiptap {
        :first-child {
                margin-top: 0;
        }

        /* List styles */
        ul,
        ol {
                padding: 0 1rem;
                margin: 1.25rem 1rem 1.25rem 0.4rem;

                li p {
                        margin-top: 0.25em;
                        margin-bottom: 0.25em;
                }
        }

        /* Heading styles */
        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {
                line-height: 1.1;
                margin-top: 2.5rem;
                text-wrap: pretty;
        }

        h1,
        h2 {
                margin-top: 3.5rem;
                margin-bottom: 1.5rem;
        }

        h1 {
                font-size: 1.4rem;
        }

        h2 {
                font-size: 1.2rem;
        }

        h3 {
                font-size: 1.1rem;
        }

        h4,
        h5,
        h6 {
                font-size: 1rem;
        }

        /* Code and preformatted text styles */
        code {
                background-color: var(--purple-light);
                border-radius: 0.4rem;
                color: var(--black);
                font-size: 0.85rem;
                padding: 0.25em 0.3em;
        }

        pre {
                background: var(--black);
                border-radius: 0.5rem;
                color: var(--white);
                font-family: 'JetBrainsMono', monospace;
                margin: 1.5rem 0;
                padding: 0.75rem 1rem;

                code {
                        background: none;
                        color: inherit;
                        font-size: 0.8rem;
                        padding: 0;
                }
        }

        mark {
                background-color: #FAF594;
                border-radius: 0.4rem;
                box-decoration-break: clone;
                padding: 0.1rem 0.3rem;
        }

        blockquote {
                border-left: 3px solid var(--gray-3);
                margin: 1.5rem 0;
                padding-left: 1rem;
        }

        hr {
                border: none;
                border-top: 1px solid var(--gray-2);
                margin: 2rem 0;
        }
}
</style>