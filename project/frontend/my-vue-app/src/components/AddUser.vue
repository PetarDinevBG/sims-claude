<template>
  <form @submit.prevent="addUser">
    <input v-model="username" placeholder="Username" required />
    <input v-model="email" placeholder="Email" required type="email" />
    <input v-model="password" placeholder="Password" required type="password" />
    <button type="submit">Add User</button>
    <div v-if="result">{{ result }}</div>
  </form>
</template>

<script setup>
import { ref } from 'vue'

const username = ref('')
const email = ref('')
const password = ref('')
const result = ref('')

const addUser = async () => {
  try {
    const response = await fetch('http://45.137.220.25:8000/users/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username.value,
        email: email.value,
        password: password.value,
      }),
    })
    if (!response.ok) throw new Error(await response.text())
    const data = await response.json()
    result.value = `User ${data.username} created!`
    username.value = ''
    email.value = ''
    password.value = ''
  } catch (e) {
    result.value = `Error: ${e}`
  }
}
</script>