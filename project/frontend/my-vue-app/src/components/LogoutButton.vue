<template>
  <button class="logout-btn" @click="logout">Logout</button>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

function logout() {
  localStorage.removeItem('access_token')
  // notify same-tab listeners
  window.dispatchEvent(new Event('auth-change'))
  router.push('/login')
}
</script>

<style scoped>
.logout-btn{
  background: transparent;
  color: #fff;
  border: 1px solid rgba(255,255,255,0.18);
  padding: 6px 10px;
  border-radius: 6px;
  cursor: pointer;
}
.logout-btn:hover{
  background: rgba(255,255,255,0.06);
}
</style>