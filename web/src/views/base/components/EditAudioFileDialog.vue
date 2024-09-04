<template>
        <n-modal v-model:show="showModal" :mask-closable="false">
                <n-card style="width: 400px" :title="title" :bordered="false" size="huge" role="dialog"
                        aria-modal="true">
                        <n-input v-model:value="localStem" placeholder="Enter new title stem" />
                        <template #footer>
                                <n-space justify="end">
                                        <n-button @click="closeModal">Cancel</n-button>
                                        <n-button type="primary" @click="saveTitle" :disabled="!localStem.trim()">
                                                Save
                                        </n-button>
                                </n-space>
                        </template>
                </n-card>
        </n-modal>
</template>

<script setup lang="ts">
import { ref, watch, computed, onMounted } from 'vue'
import { NModal, NCard, NInput, NSpace, NButton } from 'naive-ui'

const props = defineProps<{
        show: boolean
        title: string
        initialTitle: string
}>()

const emit = defineEmits(['update:show', 'save'])

const showModal = ref(props.show)
const localSuffix = ref('')
const localStem = ref('')

watch(() => props.show, (newValue) => {
        showModal.value = newValue
})

onMounted(() => {
        const { stem, suffix } = splitFileName(props.initialTitle)
        localStem.value = stem
        localSuffix.value = suffix
})

const splitFileName = (fileName: string): { stem: string, suffix: string } => {
        const lastDotIndex = fileName.lastIndexOf('.')
        if (lastDotIndex !== -1) {
                return {
                        stem: fileName.slice(0, lastDotIndex),
                        suffix: fileName.slice(lastDotIndex)
                }
        }
        return {
                stem: fileName,
                suffix: ''
        }
}

const closeModal = () => {
        emit('update:show', false)
}

const saveTitle = () => {
        const newTitle = localStem.value + localSuffix.value
        emit('save', newTitle)
        closeModal()
}
</script>