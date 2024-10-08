<template>
        <div class="tiptap-editor">
                <div v-if="editor">
                        <button :disabled="!editor.can().chain().focus().toggleBold().run()"
                                class="m-1 inline-flex items-center rounded-md bg-indigo-50 px-2 py-1 text-md font-medium text-indigo-700 ring-1 ring-inset ring-indigo-700/10"
                                :class="{ 'ring-indigo-900 ring-2': editor.isActive('bold') }"
                                @click="editor.chain().focus().toggleBold().run()">
                                <Icon name='bold' />
                        </button>
                        <button :disabled="!editor.can().chain().focus().toggleItalic().run()"
                                class="m-1 inline-flex items-center rounded-md bg-indigo-50 px-2 py-1 text-md font-medium text-indigo-700 ring-1 ring-inset ring-indigo-700/10"
                                :class="{ 'ring-indigo-900 ring-2': editor.isActive('italic') }"
                                @click="editor.chain().focus().toggleItalic().run()">
                                <Icon name='italic' />
                        </button>
                        <button :disabled="!editor.can().chain().focus().toggleStrike().run()"
                                class="m-1 inline-flex items-center rounded-md bg-indigo-50 px-2 py-1 text-md font-medium text-indigo-700 ring-1 ring-inset ring-indigo-700/10"
                                :class="{ 'ring-indigo-900 ring-2': editor.isActive('strike') }"
                                @click="editor.chain().focus().toggleStrike().run()">
                                <Icon name='strikethrough' />
                        </button>
                        <button :disabled="!editor.can().chain().focus().toggleHighlight().run()"
                                class="m-1 inline-flex items-center rounded-md bg-indigo-50 px-2 py-1 text-md font-medium text-indigo-700 ring-1 ring-inset ring-indigo-700/10"
                                :class="{ 'ring-indigo-900 ring-2': editor.isActive('highlight') }"
                                @click="editor.chain().focus().toggleHighlight().run()">
                                <Icon name='highlight' />
                        </button>


                        <button class="m-1 inline-flex items-center rounded-md bg-indigo-50 px-2 py-1 text-md font-medium text-indigo-700 ring-1 ring-inset ring-indigo-700/10"
                                :class="{ 'ring-indigo-900 ring-2': editor.isActive('heading', { level: 2 }) }"
                                @click="editor.chain().focus().toggleHeading({ level: 2 }).run()">
                                <Icon name='heading' />
                        </button>
                        <button class="m-1 inline-flex items-center rounded-md bg-indigo-50 px-2 py-1 text-md font-medium text-indigo-700 ring-1 ring-inset ring-indigo-700/10"
                                :class="{ 'ring-indigo-900 ring-2': editor.isActive('bulletList') }"
                                @click="editor.chain().focus().toggleBulletList().run()">
                                <Icon name='list-ul' />
                        </button>

                        <button class="m-1 inline-flex items-center rounded-md bg-indigo-50 px-2 py-1 text-md font-medium text-indigo-700 ring-1 ring-inset ring-indigo-700/10"
                                :class="{ 'ring-indigo-900 ring-2': editor.isActive('blockquote') }"
                                @click="editor.chain().focus().toggleBlockquote().run()">
                                <Icon name='indent' />
                        </button>

                        <button class="m-1 inline-flex items-center rounded-md bg-indigo-50 px-2 py-1 text-md font-medium text-indigo-700 ring-1 ring-inset ring-indigo-700/10"
                                @click="editor.chain().focus().setHorizontalRule().run()">
                                <Icon name='horizontal-rule' />
                        </button>

                        <button class="m-1 inline-flex items-center rounded-md  bg-indigo-50 px-2 py-1 text-md font-medium text-indigo-700 ring-1 ring-inset ring-indigo-700/10"
                                :disabled="!editor.can().chain().focus().undo().run()"
                                @click="editor.chain().focus().undo().run()">
                                <icon name="undo"></icon>
                        </button>
                        <button class="m-1 inline-flex items-center rounded-md  bg-indigo-50 px-2 py-1 text-md font-medium  text-indigo-700 ring-1 ring-inset ring-indigo-700/10"
                                :disabled="!editor.can().chain().focus().redo().run()"
                                @click="editor.chain().focus().redo().run()">
                                <icon name="redo"></icon>
                        </button>
                </div>
                <editor-content :editor="editor" class="editor-content" />
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
import Icon from '@/components/common/Icon.vue';

import { debounce } from 'lodash'

const props = defineProps<{
        audioChunkId: number | string
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
.editor-content {
        border-bottom: 1px solid #e2e8f0;
}

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
                border-top: 3px double #333;
                color: #333;
                overflow: visible;
                text-align: center;
                height: 5px;
        }

        hr::after {
                background: #fff;
                content: '§';
                padding: 0 4px;
                position: relative;
                top: -13px;
        }

}
</style>