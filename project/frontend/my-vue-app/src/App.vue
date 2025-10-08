<script setup>
import { ref, onMounted } from 'vue'
import AddUser from './components/AddUser.vue';
import UserList from './components/UserList.vue';
const apiData = ref(null);

onMounted(async () => {
  const response = await fetch('http://45.137.220.25:8000/')
  apiData.value = await response.json()
})
</script>

<template>
  <div>
    <h1>FastAPI response:</h1>
    <pre>{{ apiData }}</pre>
    <AddUser />
    <UserList />
  </div>
</template>