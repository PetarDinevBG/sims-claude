// ...existing code...
<template>
  <section class="user-list">
    <header class="user-list__header">
      <div class="header-left">
        <h2>Users <span class="muted">({{ filteredUsers.length }} / {{ users.length }})</span></h2>
        <p class="subtitle">Manage users, change roles and delete accounts</p>
      </div>

      <div class="header-right">
        <div class="search">
          <input
            v-model="query"
            type="search"
            placeholder="Search username or email..."
            aria-label="Search users"
          />
          <button class="refresh" @click="fetchUsers" title="Refresh users">⟳</button>
        </div>
      </div>
    </header>

    <ul v-if="!loading && filteredUsers.length" class="cards">
      <li v-for="user in filteredUsers" :key="user.id" class="card">
        <div class="left">
          <div class="avatar" :style="avatarStyle(user.username)">{{ initials(user.username) }}</div>
          <div class="meta">
            <div class="username">{{ user.username }}</div>
            <div class="email" v-if="user.email">{{ user.email }}</div>
          </div>
        </div>

        <div class="right">
          <div class="role-controls">
            <label class="sr-only">Role for {{ user.username }}</label>
            <select :value="user.role" @change="onRoleChange($event, user)" class="role-select">
              <option value="user">User</option>
              <option value="admin">Admin</option>
            </select>

            <button class="delete-btn" @click="deleteUser(user)" title="Delete user">🗑️</button>
          </div>

          <div class="role-badge" :data-role="user.role">{{ user.role }}</div>
        </div>
      </li>
    </ul>

    <div v-if="!loading && filteredUsers.length === 0" class="empty">
      No users found.
    </div>

    <div v-if="loading" class="loading">Loading users…</div>
    <div v-if="error" class="error">{{ error }}</div>
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

const users = ref([])
const loading = ref(false)
const error = ref('')
const query = ref('')
const baseUrl = 'http://45.137.220.25:8000'

function initials(name = '') {
  if (!name) return ''
  return name.split(' ').map(n => n[0]?.toUpperCase()).slice(0,2).join('')
}

function avatarStyle(name = '') {
  // deterministic pastel color per username
  let hash = 0
  for (let i = 0; i < name.length; i++) hash = name.charCodeAt(i) + ((hash << 5) - hash)
  const hue = Math.abs(hash) % 360
  return `background: linear-gradient(135deg, hsl(${hue} 55% 55%), hsl(${(hue+30)%360} 55% 45%)); color: white;`
}

async function fetchUsers() {
  loading.value = true
  error.value = ''
  try {
    const response = await fetch(`${baseUrl}/users/`)
    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`)
    }
    const data = await response.json()
    users.value = Array.isArray(data) ? data : []
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load users'
  } finally {
    loading.value = false
  }
}

onMounted(fetchUsers)

const filteredUsers = computed(() => {
  const q = (query.value || '').trim().toLowerCase()
  if (!q) return users.value
  return users.value.filter(u =>
    (u.username || '').toLowerCase().includes(q) ||
    (u.email || '').toLowerCase().includes(q) ||
    (u.role || '').toLowerCase().includes(q)
  )
})

async function onRoleChange(event, user) {
  const newRole = event.target.value
  try {
    const res = await fetch(`${baseUrl}/users/${user.id}/role`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ role: newRole })
    })
    if (!res.ok) {
      const err = await res.json().catch(() => null)
      throw new Error(err?.detail || `Status ${res.status}`)
    }
    const updated = await res.json()
    const idx = users.value.findIndex(u => u.id === updated.id)
    if (idx !== -1) users.value[idx] = updated
  } catch (err) {
    console.error(err)
    error.value = 'Failed to update role'
    await fetchUsers()
  }
}

async function deleteUser(user) {
  if (!confirm(`Delete user "${user.username}"? This cannot be undone.`)) return
  try {
    const res = await fetch(`${baseUrl}/users/${user.id}`, { method: 'DELETE' })
    if (!res.ok) {
      const err = await res.json().catch(() => null)
      throw new Error(err?.detail || `Status ${res.status}`)
    }
    users.value = users.value.filter(u => u.id !== user.id)
  } catch (err) {
    console.error(err)
    error.value = 'Failed to delete user'
  }
}
</script>

<style scoped>
:root{
  --bg: #f6f8fb;
  --card: #ffffff;
  --muted: #7b8694;
  --accent: #0b5ed7;
  --success: #2e8b57;
  --danger: #c92a2a;
  --glass: rgba(255,255,255,0.6);
}

.user-list{
  max-width: 980px;
  margin: 28px auto;
  padding: 18px;
  background: linear-gradient(180deg, var(--bg), #ffffff);
  border-radius: 12px;
  box-shadow: 0 6px 30px rgba(20,30,50,0.06);
  border: 1px solid rgba(30,40,60,0.04);
}

.user-list__header{
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:16px;
  padding:8px 12px;
  margin-bottom:14px;
}

.header-left h2{
  margin:0;
  font-size:1.15rem;
  color:#14202b;
  display:flex;
  gap:8px;
  align-items:center;
}

.subtitle{
  margin:4px 0 0 0;
  font-size:0.85rem;
  color:var(--muted);
}

.muted{
  font-weight:600;
  color:var(--muted);
  font-size:0.95rem;
}

.header-right{
  display:flex;
  gap:8px;
  align-items:center;
}

.search{
  display:flex;
  gap:8px;
  align-items:center;
  background:var(--glass);
  padding:6px;
  border-radius:999px;
}

.search input{
  border: none;
  outline:none;
  background:transparent;
  padding:6px 8px;
  font-size:0.95rem;
  min-width:220px;
}

.search .refresh{
  border: none;
  background: transparent;
  cursor: pointer;
  font-size:1rem;
  padding:6px 8px;
  color:var(--accent);
}

.cards{
  list-style:none;
  display:grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap:12px;
  padding:0;
  margin:0;
}

.card{
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:12px;
  padding:12px;
  background:var(--card);
  border-radius:10px;
  border:1px solid rgba(20,30,50,0.04);
  box-shadow: 0 8px 20px rgba(16,24,40,0.04);
  transition: transform .12s ease, box-shadow .12s ease;
}

.card:hover{
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(16,24,40,0.06);
}

.left{
  display:flex;
  gap:12px;
  align-items:center;
  flex:1;
  min-width:0;
}

.avatar{
  width:56px;
  height:56px;
  min-width:56px;
  border-radius:50%;
  display:flex;
  align-items:center;
  justify-content:center;
  font-weight:700;
  font-size:0.95rem;
  box-shadow: 0 4px 14px rgba(20,30,40,0.06);
}

.meta{
  overflow:hidden;
}

.username{
  font-weight:600;
  color:#0f1720;
  white-space:nowrap;
  text-overflow:ellipsis;
  overflow:hidden;
}

.email{
  font-size:0.85rem;
  color:var(--muted);
  margin-top:4px;
  white-space:nowrap;
  text-overflow:ellipsis;
  overflow:hidden;
}

.right{
  display:flex;
  flex-direction:column;
  align-items:flex-end;
  gap:8px;
}

.role-controls{
  display:flex;
  gap:8px;
  align-items:center;
}

.role-select{
  padding:8px 10px;
  border-radius:8px;
  border:1px solid rgba(20,30,40,0.06);
  background:#fff;
  cursor:pointer;
  font-weight:600;
  color:#0f1720;
}

.delete-btn{
  background:transparent;
  border:none;
  cursor:pointer;
  padding:8px;
  border-radius:8px;
  transition: background .12s ease;
  font-size:1rem;
}

.delete-btn:hover{
  background: rgba(200,30,30,0.08);
  color: var(--danger);
}

.role-badge{
  font-size:0.78rem;
  padding:6px 10px;
  border-radius:999px;
  text-transform:capitalize;
  color:#fff;
  background:#6c757d;
  white-space:nowrap;
  font-weight:700;
}

.role-badge[data-role="admin"]{
  background:var(--accent);
}

.role-badge[data-role="user"]{
  background:var(--success);
}

.empty, .loading, .error{
  text-align:center;
  color:var(--muted);
  padding:18px 0;
}

.error{
  color: var(--danger);
  font-weight:600;
}

/* accessibility helpers */
.sr-only{
  position:absolute!important;
  width:1px;height:1px;
  padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);
  white-space:nowrap;border:0;
}

@media (max-width:640px){
  .header-right .search input{ min-width:120px; }
  .cards{ grid-template-columns: 1fr; }
  .right{ align-items:flex-start; }
}
</style>