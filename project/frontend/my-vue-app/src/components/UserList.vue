
<template>
  <section class="user-list">
    <header class="user-list__header">
      <h2>Users ({{ users.length }})</h2>
      <div v-if="loading" class="status">Loading...</div>
      <div v-if="error" class="status error">{{ error }}</div>
    </header>

    <ul v-if="!loading && users.length" class="cards">
      <li v-for="user in users" :key="user.id" class="card">
        <div class="avatar">{{ initials(user.username) }}</div>
        <div class="meta">
          <div class="username">{{ user.username }}</div>
          <div class="email" v-if="user.email">{{ user.email }}</div>
        </div>
        <div class="role-badge" :data-role="user.role">{{ user.role }}</div>
      </li>
    </ul>

    <div v-if="!loading && users.length === 0" class="empty">No users found.</div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const users = ref([])
const loading = ref(false)
const error = ref('')

function initials(name = '') {
  if (!name) return ''
  return name.split(' ').map(n => n[0]?.toUpperCase()).slice(0,2).join('')
}

onMounted(async () => {
  loading.value = true
  error.value = ''
  try {
    const response = await fetch('http://45.137.220.25:8000/users/')
    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`)
    }
    const data = await response.json()
    // ensure we have an array
    users.value = Array.isArray(data) ? data : []
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load users'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.user-list {
  max-width: 900px;
  margin: 20px auto;
  padding: 12px;
}

.user-list__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.user-list__header h2 {
  margin: 0;
  font-size: 1.1rem;
  color: #2b2b2b;
}

.status {
  font-size: 0.9rem;
  color: #666;
}

.status.error {
  color: #b00020;
}

/* card grid */
.cards {
  list-style: none;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 12px;
  padding: 0;
  margin: 0;
}

/* individual card */
.card {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #ffffff;
  border-radius: 8px;
  padding: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  border: 1px solid rgba(0,0,0,0.04);
}

.avatar {
  width: 48px;
  height: 48px;
  min-width: 48px;
  border-radius: 50%;
  background: #2e8b57;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.95rem;
}

.meta {
  flex: 1;
}

.username {
  font-weight: 600;
  color: #111;
}

.email {
  font-size: 0.85rem;
  color: #666;
  margin-top: 4px;
}

.role-badge {
  font-size: 0.8rem;
  padding: 6px 8px;
  border-radius: 999px;
  text-transform: capitalize;
  color: #fff;
  background: #6c757d;
  white-space: nowrap;
}

.role-badge[data-role="admin"] {
  background: #0b5ed7;
}

.role-badge[data-role="user"] {
  background: #2e8b57;
}

.empty {
  text-align: center;
  color: #666;
  padding: 18px 0;
}
</style>
