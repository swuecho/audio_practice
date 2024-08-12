<template>
        <div class="tiptap-editor">
                <editor-content :editor="editor" />
        </div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { Editor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'

const editor = ref<Editor | null>(null)

onMounted(() => {
        editor.value = new Editor({
                extensions: [StarterKit],
                content: '<p>Start typing here...</p>',
                autofocus: true,
                editable: true,
        })
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
</style>