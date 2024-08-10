

<script setup lang="ts">
import { ref } from 'vue'
import { NButton, NForm, NFormItem, NInput, NSwitch } from 'naive-ui'
import { request } from '@/utils'

const emit = defineEmits<Emit>()

const formData = ref<Parameter>({
  name: '',
  description: null,
  value: ''
})

interface Emit {
  (e: 'newRowAdded'): void
}

async function createParameter(value: Parameter) {
  let result = await request.post('/parameters/', value)
  return result
}

async function addRow() {
  // create a new chat model, the name is randon string
  await createParameter(formData.value)
  // add it to the data array
  emit('newRowAdded')
}
</script>

<template>
  <div>
    <NForm :model="formData">
      <NFormItem path="label" label='name'>
        <NInput v-model:value="formData.name" />
      </NFormItem>
      <NFormItem path="label" label='desc'>
        <NInput v-model:value="formData.description" />
      </NFormItem>
      <NFormItem path="label" label='value'>
        <NInput v-model:value="formData.value" />
      </NFormItem>
    </NForm>

    <NButton type="primary" block secondary strong @click="addRow">
      确认
    </NButton>
  </div>
</template>