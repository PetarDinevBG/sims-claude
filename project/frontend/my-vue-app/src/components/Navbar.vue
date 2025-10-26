<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import LogoutButton from './LogoutButton.vue'

const router = useRouter()

// reactive token source
const token = ref(localStorage.getItem('access_token'))

// computed boolean that updates when `token` changes
const isLoggedIn = computed(() => !!token.value)

// keep token in sync across tabs (storage) and same-tab actions (auth-change)
const onStorage = (e: StorageEvent) => {
  if (!e.key || e.key === 'access_token') token.value = localStorage.getItem('access_token')
}
const onAuthChange = () => {
  token.value = localStorage.getItem('access_token')
}

onMounted(() => {
  window.addEventListener('storage', onStorage)
  window.addEventListener('auth-change', onAuthChange)
})

onUnmounted(() => {
  window.removeEventListener('storage', onStorage)
  window.removeEventListener('auth-change', onAuthChange)
})

const goLogin = () => router.push('/login')
</script>

<template>
  <nav class="navbar">
    <div class="nav-content">
      <div class="logo">MyApp</div>
      <ul class="nav-links">
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/users">Users</router-link></li>
        <li><router-link to="/items">Items</router-link></li>
        <li v-if="isLoggedIn "><LogoutButton /></li>
        <li v-else><button class="login-btn" @click="goLogin">Login</button></li>
      </ul>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  background-color: #2e8b57; /* green */
  padding: 12px 0;
  display: flex;
  justify-content: center;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}

.nav-content {
  width: 100%;
  max-width: 960px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24px;
  padding: 0 16px;
}

/* Logo */
.logo {
  color: #fff;
  font-weight: 700;
  font-size: 1.1rem;
  margin-right: 8px;
}

/* Centered nav links */
.nav-links {
  list-style: none;
  display: flex;
  gap: 20px;
  align-items: center;
  margin: 0;
  padding: 0;
}

.nav-links a {
  color: #ffffff;
  text-decoration: none;
  padding: 6px 10px;
  border-radius: 6px;
  transition: background-color 0.15s ease;
}

.nav-links a:hover {
  background: rgba(255,255,255,0.08);
}

.router-link-active {
  text-decoration: underline;
  background: rgba(255,255,255,0.12);
}
.login-btn {
  background: transparent;
  color: #fff;
  border: 1px solid rgba(255,255,255,0.18);
  padding: 6px 10px;
  border-radius: 6px;
  cursor: pointer;
}
.login-btn:hover {
  background: rgba(255,255,255,0.06);
}
</style>