<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import LogoutButton from './LogoutButton.vue'

const router = useRouter()

/// reactive token source
const token = ref(localStorage.getItem('access_token'))

// computed boolean that updates when `token` changes
const isLoggedIn = computed(() => !!token.value)

// --- decode JWT payload and isAdmin check ---
function decodeJwtPayload(tokenStr: string | null) {
  if (!tokenStr) return null
  try {
    const parts = tokenStr.split('.')
    if (parts.length < 2) return null
    // base64url -> base64
    const b64 = parts[1].replace(/-/g, '+').replace(/_/g, '/')
    const pad = b64.length % 4
    const padded = b64 + (pad ? '='.repeat(4 - pad) : '')
    const json = atob(padded)
    return JSON.parse(json)
  } catch {
    return null
  }
}

const isAdmin = computed(() => {
  const payload = decodeJwtPayload(token.value)
  if (!payload) return false
  if (payload.role && payload.role === 'admin') return true
  if (Array.isArray(payload.roles) && payload.roles.includes('admin')) return true
  return false
})
// --- end added ---

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
  <header class="navbar" role="banner" aria-label="Main navigation">
    <div class="nav-container">
      <div class="nav-left">
        <button class="brand" @click="router.push('/')">
          <span class="brand-mark" aria-hidden="true">📚✏️</span>
          <span class="brand-text">School Inventory</span>
        </button>

        <nav class="links" aria-label="Primary">
          <router-link class="nav-link" to="/">Home</router-link>
          <router-link v-if="isAdmin" class="nav-link" to="/users">Admin Panel</router-link>
          <router-link class="nav-link" to="/items">Equipment</router-link>
          <router-link class="nav-link" to="/requests">Requests</router-link>
          <router-link class="nav-link" to="/reports">Reports</router-link>
        </nav>
      </div>

      <div class="nav-right">
        <div class="actions" role="navigation" aria-label="User actions">
          <button class="ghost-btn" title="Help" aria-label="Help">?</button>

          <button v-if="isLoggedIn" class="profile-pill" aria-label="Account">Account</button>
          <LogoutButton v-if="isLoggedIn" />

          <button v-else class="login-btn" @click="goLogin">Sign in</button>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
:root{
  --nav-height: 76px;
  --max-width: 1300px;
  --accent: #1f9b4a;
  --bg: #f6fbf8;
  --card: #ffffff;
  --glass: rgba(255,255,255,0.85);
  --muted: #6b7280;
  --text: #082018;
  --shadow-lg: 0 14px 36px rgba(31,155,74,0.14);
}

/* sticky top bar spanning full width with subtle shadow */
.navbar {
  position: sticky;
  top: 0;
  z-index: 1000;
  width: 100%;
  background: linear-gradient(90deg, rgba(31,155,74,0.98), rgba(25,135,60,0.96));
  box-shadow: 0 6px 24px rgba(12, 46, 23, 0.12);
  backdrop-filter: blur(6px);
}

/* center the content and keep rounded edges */
.nav-container {
  max-width: var(--max-width);
  margin: 8px auto;
  padding: 10px 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  border-radius: 10px;
  color: #fff;
}

/* left grouping */
.nav-left {
  display:flex;
  align-items:center;
  gap:18px;
}

/* brand button */
.brand{
  display:flex;
  align-items:center;
  gap:10px;
  background: transparent;
  border: none;
  color: #fff;
  cursor: pointer;
  padding: 6px 8px;
  border-radius: 8px;
}
.brand:hover { background: rgba(255,255,255,0.03); }

.brand-mark {
  font-size: 1.25rem;
  display:inline-flex;
  align-items:center;
  justify-content:center;
  width:36px;
  height:36px;
  border-radius: 8px;
  background: rgba(255,255,255,0.04);
}

.brand-text {
  font-weight: 700;
  font-size: 1.05rem;
  letter-spacing: -0.01em;
}

/* primary links */
.links {
  display:flex;
  gap: 12px;
  align-items:center;
}

.nav-link {
  color: rgba(255,255,255,0.95);
  text-decoration: none;
  padding: 8px 10px;
  border-radius: 8px;
  font-weight:600;
  transition: background .12s ease, transform .12s ease;
}
.nav-link:hover { background: rgba(255,255,255,0.05); transform: translateY(-2px); }
.router-link-active { background: rgba(0,0,0,0.08); }

/* right side actions */
.nav-right .actions {
  display:flex;
  gap:10px;
  align-items:center;
}

/* ghost/help button */
.ghost-btn {
  border: none;
  background: rgba(255,255,255,0.04);
  color: #fff;
  width:40px;
  height:40px;
  border-radius:8px;
  font-weight:700;
  cursor:pointer;
}
.ghost-btn:hover { background: rgba(255,255,255,0.06); transform: translateY(-1px); }

/* profile pill for logged-in user */
.profile-pill {
  background: rgba(0,0,0,0.08);
  color: #fff;
  padding: 8px 12px;
  border-radius: 999px;
  font-weight:700;
  cursor:pointer;
}

/* prominent sign-in button */
.login-btn {
  background: linear-gradient(90deg, #2ecc71, #06e03d);
  color: #032018;
  border: none;
  padding: 8px 14px;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 8px 22px rgba(6, 121, 35, 0.22);
}
.login-btn:hover { transform: translateY(-2px); }

/* Responsive: collapse links on small screens */
@media (max-width: 820px) {
  .links { display:none; }
  .brand-text { display:none; }
  .nav-container { padding: 10px 14px; }
}
</style>