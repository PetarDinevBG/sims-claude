<template>
  <div class="register">
    <h2>Register</h2>
    <form @submit.prevent="register">
      <input v-model="username" placeholder="Username" required />
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">Register</button>
    </form>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const email = ref('')
const password = ref('')
const message = ref('')

const register = async () => {
  message.value = ''
  try {
    const res = await fetch('http://45.137.220.25:8000/register/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username.value,
        email: email.value,
        password: password.value
      })
    })
    if (res.ok) {
      message.value = 'Registration successful. Redirecting to login...'
      setTimeout(() => router.push('/login'), 1000)
    } else {
      const err = await res.json().catch(() => null)
      message.value = err?.detail || 'Registration failed'
    }
  } catch (err) {
    message.value = 'Network error'
    console.error(err)
  }
}
</script>

<style scoped>
.register {
  max-width: 360px;
  margin: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
</style>