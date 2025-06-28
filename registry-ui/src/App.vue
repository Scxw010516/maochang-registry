<template>
  <a-config-provider
    :locale="locale"
    :theme="{ token: { colorPrimary: '#8675ff' } }"
  >
    <router-view />
  </a-config-provider>
</template>

<script setup></script>
