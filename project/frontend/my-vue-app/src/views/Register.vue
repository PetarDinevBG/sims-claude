<template>
  <div class="page">
    <div class="card">
      <header class="card-header">
        <h2>Create an account</h2>
        <p class="muted">Join MyApp — quick and free</p>
      </header>

      <form class="form" @submit.prevent="register" novalidate>
        <label class="field">
          <span class="label-text">Username</span>
          <input v-model="username" required autocomplete="username" />
        </label>

        <label class="field">
          <span class="label-text">Email</span>
          <input v-model="email" type="email" required autocomplete="email" />
        </label>

        <label class="field">
          <span class="label-text">Password</span>
          <input v-model="password" type="password" required autocomplete="new-password" />
        </label>

        <div class="actions">
          <button class="btn primary" type="submit">Register</button>
          <button class="btn outline" type="button" @click="gotoLogin">Back to Login</button>
        </div>

        <p v-if="message" :class="messageClass">{{ message }}</p>
      </form>
    </div>
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
const messageClass = ref('')

const register = async () => {
  message.value = ''
  messageClass.value = ''
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
      messageClass.value = 'success'
      setTimeout(() => router.push('/login'), 1000)
    } else {
      const err = await res.json().catch(() => null)
      message.value = err?.detail || 'Registration failed'
      messageClass.value = 'error'
    }
  } catch (err) {
    message.value = 'Network error'
    messageClass.value = 'error'
    console.error(err)
  }
}

const gotoLogin = () => router.push('/login')
</script>

<style scoped>
:root{
  --green-700: #1f8a4d;
  --green-500: #2e8b57;
  --green-300: #66c18d;
  --bg: #f6fbf8;
  --card: #ffffff;
  --muted: #6b7280;
  --error: #e55353;
  --success: #16a34a;
}

.page{
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(180deg, #eef9f2 0%, #f6fbf8 100%);
  padding: 40px 16px;
}

.card{
  width: 100%;
  max-width: 420px;
  background: var(--card);
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(22, 64, 45, 0.08);
  padding: 28px;
  border: 1px solid rgba(46,139,87,0.08);
}

.card-header {
  text-align: center;
  margin-bottom: 18px;
}

.card-header h2 {
  margin: 0;
  color: var(--green-700);
  font-size: 1.4rem;
  font-weight: 700;
}

.muted {
  margin: 6px 0 0;
  color: var(--muted);
  font-size: 0.95rem;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.label-text {
  font-size: 0.85rem;
  color: #374151;
}

/* inputs match Login styles */
.field input {
  width: 100%;
  box-sizing: border-box;
  height: 44px;
  padding: 8px 12px;
  border: 1px solid rgba(15, 23, 42, 0.06);
  border-radius: 8px;
  background: #fbfffb;
  outline: none;
  font-size: 1rem;
  transition: box-shadow 0.12s ease, border-color 0.12s ease;
}

input:focus {
  box-shadow: 0 0 0 4px rgba(46,139,87,0.08);
  border-color: var(--green-500);
}

.actions {
  display: flex;
  gap: 10px;
  margin-top: 6px;
}

.btn {
  flex: 1;
  height: 44px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  border: 1px solid transparent;
  transition: transform 0.06s ease, box-shadow 0.08s ease;
}

.btn:active { transform: translateY(1px); }

.btn.primary {
  background: linear-gradient(180deg, #34a853 0%, var(--green-700) 100%);
  color: #000000;
  box-shadow: 0 10px 30px rgba(46,139,87,0.18);
  border: 1px solid rgba(10, 80, 35, 0.12);
  transition: transform 0.06s ease, box-shadow 0.12s ease, filter 0.06s ease;
}

.btn.primary:hover {
  filter: brightness(0.98);
  box-shadow: 0 12px 36px rgba(46,139,87,0.22);
  transform: translateY(-1px);
}

.btn.primary:focus {
  outline: 3px solid rgba(46,139,87,0.12);
  outline-offset: 2px;
}

.btn.outline {
  background: transparent;
  color: var(--green-700);
  border: 1px solid rgba(46,139,87,0.12);
}

.error {
  margin-top: 8px;
  color: var(--error);
  font-size: 0.95rem;
  text-align: center;
}

.success {
  margin-top: 8px;
  color: var(--success);
  font-size: 0.95rem;
  text-align: center;
}

@media (max-width: 420px){
  .card { padding: 20px; }
  .actions { flex-direction: column; }
}
</style>