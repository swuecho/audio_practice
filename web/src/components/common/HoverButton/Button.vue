<script setup lang='ts'>
interface Emit {
  (e: 'click'): void
}

const emit = defineEmits<Emit>()

function handleClick() {
  emit('click')
}
</script>

<template>
  <n-button type="default"
    @click="handleClick"
  >
    <slot />
  </n-button>
</template>
