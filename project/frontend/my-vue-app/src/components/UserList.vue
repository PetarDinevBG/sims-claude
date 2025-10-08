<template>
  <div>
    <h2>Users</h2>
    <ul>
      <li v-for="user in users" :key="user.id">
        {{ user.username }} ({{ user.email }})
      </li>
    </ul>
    <div v-if="users.length === 0">No users found.</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const users = ref([])

onMounted(async () => {
  const response = await fetch('http://45.137.220.25:8000/users/')
  if (response.ok) {
    users.value = await response.json()
  }
})
</script>