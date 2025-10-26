<script setup>
import { ref, onMounted } from 'vue'
const apiData = ref(null);
const kristianData = ref(null);


onMounted(async () => {
  const response = await fetch('http://45.137.220.25:8000/')
  const krisresponse = await fetch('http://45.137.220.25:8000/kristian/')
  apiData.value = await response.json()
  kristianData.value = await krisresponse.json()
})
</script>

<template>
  <div>
    <div>{{ apiData }}</div>
  </div>
</template>