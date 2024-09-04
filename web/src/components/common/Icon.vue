<template>
  <component :is="icon" width="16" height="16" v-bind="$attrs" />
</template>

<script lang="ts">
import { defineComponent, defineAsyncComponent } from 'vue';

export default defineComponent({
  name: 'icon',

  props: {
    name: String,
  },

  computed: {
    icon() {
      //@ts-ignore
      return defineAsyncComponent(() => import(`../../assets/icons/editor/${this.name}.svg`));
    },
  },
});
</script>