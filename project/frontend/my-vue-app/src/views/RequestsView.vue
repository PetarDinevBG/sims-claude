<template>
  <div class="page">
    <RequestList />
  </div>
</template>

<script setup>
import RequestList from '../components/RequestList.vue'
</script>

<style scoped>
.page { padding: 18px; min-height: 100vh; background: var(--bg, #f6fbf8); }
</style>