<template>
  <div>
    <p>试戴内容展示 {{ props.id }}</p>
  </div>
</template>
<script lang="ts" setup>
const props = defineProps<{
  id: number; // 试戴的ID
}>();
</script>
