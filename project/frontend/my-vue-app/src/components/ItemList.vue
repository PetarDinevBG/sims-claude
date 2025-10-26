<template>
  <div class="item-list">
    <div class="list-header">
      <div class="left">
        <h2>Items</h2>
        <div class="search">
          <input v-model="searchTerm" placeholder="Search items by name, type, serial, location..." />
        </div>
      </div>

 <div class="right">
      <AddItem v-if="isAdmin" @created="onItemCreated" />
      </div>
    </div>

    <ul v-if="filteredItems.length" class="items-grid" role="list">
      <li v-for="(item, idx) in filteredItems" :key="item.id" class="item-card" role="listitem" :aria-label="item.name">
        <div class="item-main">
          <div class="item-title">
            <strong>{{ item.name }}</strong>
            <span class="muted"> • {{ item.type }}</span>
          </div>
          <div class="item-meta">
            <span class="muted">SN: {{ item.serial_number }}</span>
            <span class="muted">Condition: {{ item.condition }}</span>
            <span class="muted">Status: {{ item.status }}</span>
            <span class="muted">Location: {{ item.location }}</span>
          </div>
        </div>

        <div class="item-actions">
            <div v-if="isLoggedIn">
           <button
             v-if="isRequestable(item)"
             class="btn btn-request"
             @click="requestItem(item)"
             :disabled="requesting[item.id]"
           >
           <span v-if="!requesting[item.id]">Request</span>
           <span v-else>Sending...</span>
           </button>
          <button v-else class="btn btn-disabled" disabled title="Item is currently  Unavailable">
           Unavailable
          </button>
         </div>

          <button v-if="isAdmin" class="btn btn-edit" @click="openEditMenu(item, idx)">Edit</button>
          <button v-if="isAdmin" class="btn btn-delete" @click="deleteItem(item, idx)">Delete</button>
        </div>
      </li>
    </ul>

    <div v-else class="empty">No items found.</div>

    <div v-if="lastDeleted" class="undo-bar" role="status" aria-live="polite">
      <span>Item "{{ lastDeleted.item.name }}" deleted.</span>
      <button class="btn btn-undo" @click="undoDelete">Undo</button>
      <small class="muted"> (you have {{ undoTimeoutSec }}s)</small>
    </div>

    <!-- Edit modal/menu (unchanged) -->
    <div v-if="editingItem" class="modal-overlay" @keydown.esc="closeEditMenu" tabindex="-1">
      <div class="modal" role="dialog" aria-modal="true" :aria-label="`Edit ${editingItem.name}`">
        <header class="modal-header">
          <h3>Edit item</h3>
        </header>

        <section class="modal-body">
          <label class="field">
            <div class="label">Name</div>
            <input v-model="editForm.name" type="text" />
          </label>

          <label class="field">
            <div class="label">Type</div>
            <input v-model="editForm.type" type="text" placeholder="e.g. Laptop, Projector" />
          </label>

          <label class="field">
            <div class="label">Serial number</div>
            <input v-model="editForm.serial_number" type="text" />
          </label>

          <label class="field">
            <div class="label">Location</div>
            <input v-model="editForm.location" type="text" />
          </label>

          <label class="field">
            <div class="label">Condition</div>
            <select v-model="editForm.condition">
              <option value="">(unspecified)</option>
              <option>New</option>
              <option>Good</option>
              <option>Fair</option>
              <option>Poor</option>
              <option>Broken</option>
            </select>
          </label>

          <label class="field">
            <div class="label">Status</div>
            <select v-model="editForm.status">
              <option value="">(unspecified)</option>
              <option>Available</option>
              <option>Checked Out</option>
              <option>In Maintenance</option>
              <option>Lost</option>
            </select>
          </label>
        </section>

        <footer class="modal-actions">
          <button class="btn btn-primary" @click="saveEdit">Save</button>
          <button class="btn" @click="closeEditMenu">Cancel</button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, reactive } from 'vue'
import { useRouter } from 'vue-router'
import AddItem from './AddItem.vue'

// ...existing code...
// filepath: /root/sims-claude/project/frontend/my-vue-app/src/components/ItemList.vue
// ...existing code...
const router = useRouter()
const items = ref([])
const lastDeleted = ref(null) // { item, index, timerId, expiresAt }
const undoTimeoutMs = 10000
const undoTimeoutSec = ref(Math.round(undoTimeoutMs / 1000))

const searchTerm = ref('')

function isRequestable(item) {
  // changed: only allow requests when status is exactly "Available" (case-insensitive)
  if (!item || !item.status) return true
  return String(item.status).toLowerCase().trim() === 'available'
}
function decodeJwtPayload(tokenStr) {
  if (!tokenStr) return null
  try {
    const parts = tokenStr.split('.')
    if (parts.length < 2) return null
    let b64 = parts[1].replace(/-/g, '+').replace(/_/g, '/')
    const pad = b64.length % 4
    b64 = b64 + (pad ? '='.repeat(4 - pad) : '')
    const json = atob(b64)
    return JSON.parse(json)
  } catch {
    return null
  }
}

const token = ref(localStorage.getItem('access_token'))
const isAdmin = computed(() => {
  const payload = decodeJwtPayload(token.value)
  if (!payload) return false
  if (payload.role && payload.role === 'admin') return true
  if (Array.isArray(payload.roles) && payload.roles.includes('admin')) return true
  return false
})
const isLoggedIn = computed(() => !!token.value)

const requesting = reactive({})

async function loadItems() {
  try {
    const res = await fetch('http://45.137.220.25:8000/items/')
    if (res.ok) items.value = await res.json()
  } catch (e) {
    // silent fail for now
  }
}

onMounted(() => {
  loadItems()
})

// computed filtered list by search
const filteredItems = computed(() => {
  const q = (searchTerm.value || '').trim().toLowerCase()
  if (!q) return items.value
  return items.value.filter((it) => {
    return (
      (it.name || '').toLowerCase().includes(q) ||
      (it.type || '').toLowerCase().includes(q) ||
      (it.serial_number || '').toLowerCase().includes(q) ||
      (it.location || '').toLowerCase().includes(q)
    )
  })
})

// handler when AddItem emits created
function onItemCreated(newItem) {
  // insert at top so user sees it
  items.value.unshift(newItem)
}
async function requestItem(item) {
  if (!isLoggedIn.value) {
    router.push('/login')
    return
  }

  requesting[item.id] = true

  // try to read user id from token payload (common claim names)
  const payload = decodeJwtPayload(token.value)
  let userId = null
  if (payload) {
    if (payload.id) userId = payload.id
    if (!userId && payload.user_id) userId = payload.user_id
    if (!userId && payload.sub && typeof payload.sub === 'number') userId = payload.sub
  }

  // if we don't have an id, look up users to match by username (sub)
  if (!userId && payload && payload.sub) {
    try {
      const res = await fetch('http://45.137.220.25:8000/users/')
      if (res.ok) {
        const users = await res.json()
        const found = users.find(u => u.username === payload.sub || u.username === payload.username)
        if (found) userId = found.id
      }
    } catch (e) {
      // ignore
    }
  }

  // if still no userId, fail politely
  if (!userId) {
    requesting[item.id] = false
    alert('Could not determine your user id. Please contact an admin.')
    return
  }

  try {
    const res = await fetch('http://45.137.220.25:8000/requests/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token.value ? { Authorization: `Bearer ${token.value}` } : {})
      },
      body: JSON.stringify({
        item_id: item.id,
        user_id: userId
      })
    })
    console.log(item.id, userId)
    if (!res.ok) {
      const txt = await res.text().catch(() => '')
      alert('Request failed' + (txt ? ': ' + txt : ''))
    } else {
      alert('Request submitted')
    }
  } catch (e) {
    alert('Network error while submitting request')
  } finally {
    requesting[item.id] = false
  }
}



 // EDIT modal logic (same as before)
const editingItem = ref(null)
const editingIndex = ref(-1)
const editForm = reactive({
  id: null,
  name: '',
  type: '',
  serial_number: '',
  location: '',
  condition: '',
  status: ''
})

function openEditMenu(item, idx) {
  editingItem.value = item
  // find actual index inside items array (because filteredItems indexes differ)
  const realIndex = items.value.findIndex((i)=>i.id === item.id)
  editingIndex.value = realIndex
  editForm.id = item.id
  editForm.name = item.name ?? ''
  editForm.type = item.type ?? ''
  editForm.serial_number = item.serial_number ?? ''
  editForm.location = item.location ?? ''
  editForm.condition = item.condition ?? ''
  editForm.status = item.status ?? ''
}

function closeEditMenu() {
  editingItem.value = null
  editingIndex.value = -1
  editForm.id = null
  editForm.name = ''
  editForm.type = ''
  editForm.serial_number = ''
  editForm.location = ''
  editForm.condition = ''
  editForm.status = ''
}

async function saveEdit() {
  if (!editingItem.value) return
  const payload = {
    name: editForm.name,
    type: editForm.type,
    serial_number: editForm.serial_number,
    location: editForm.location,
    condition: editForm.condition,
    status: editForm.status
  }
  const idx = editingIndex.value
  const prev = { ...items.value[idx] }
  items.value[idx] = { ...items.value[idx], ...payload }

  try {
    const res = await fetch(`http://45.137.220.25:8000/items/${editForm.id}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        Authorization: token.value ? `Bearer ${token.value}` : undefined
      },
      body: JSON.stringify(payload)
    })
    if (!res.ok) {
      items.value[idx] = prev
      const text = await res.text().catch(() => '')
      alert('Failed to save changes' + (text ? ': ' + text : ''))
    }
  } catch (err) {
    items.value[idx] = prev
    alert('Network error while saving changes')
  } finally {
    closeEditMenu()
  }
}

async function deleteItem(item, idxInFiltered) {
  // compute real index from item id
  const realIndex = items.value.findIndex(i => i.id === item.id)
  if (realIndex === -1) return
  // optimistic remove
  const removed = items.value.splice(realIndex, 1)[0]
  if (lastDeleted.value && lastDeleted.value.timerId) {
    clearInterval(lastDeleted.value.countdownId)
    clearTimeout(lastDeleted.value.timerId)
  }

  const timerId = setTimeout(() => {
    lastDeleted.value = null
  }, undoTimeoutMs)

  const start = Date.now()
  undoTimeoutSec.value = Math.round((undoTimeoutMs) / 1000)
  const countdownId = setInterval(() => {
    const elapsed = Date.now() - start
    const left = Math.max(0, Math.ceil((undoTimeoutMs - elapsed) / 1000))
    undoTimeoutSec.value = left
    if (left <= 0) clearInterval(countdownId)
  }, 250)

  lastDeleted.value = { item: removed, index: realIndex, timerId, countdownId, expiresAt: Date.now() + undoTimeoutMs }

  try {
    await fetch(`http://45.137.220.25:8000/items/${item.id}/`, {
      method: 'DELETE',
      headers: { Authorization: token.value ? `Bearer ${token.value}` : undefined }
    })
  } catch {
    // network fail
  }
}

async function undoDelete() {
  if (!lastDeleted.value) return
  const { item, index, timerId, countdownId } = lastDeleted.value
  clearTimeout(timerId)
  clearInterval(countdownId)

  const insertIndex = Math.min(index, items.value.length)
  items.value.splice(insertIndex, 0, item)

  const tryPatch = async () => {
    try {
      const res = await fetch(`http://45.137.220.25:8000/items/${item.id}/`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json', Authorization: token.value ? `Bearer ${token.value}` : undefined },
        body: JSON.stringify(item)
      })
      return res.ok
    } catch {
      return false
    }
  }
  const tryPost = async () => {
    try {
      const res = await fetch(`http://45.137.220.25:8000/items/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: token.value ? `Bearer ${token.value}` : undefined },
        body: JSON.stringify(item)
      })
      return res.ok
    } catch {
      return false
    }
  }

  const patched = await tryPatch()
  if (!patched) {
    await tryPost()
  }

  lastDeleted.value = null
}


</script>

<style scoped>
:root {
  --accent: #1f9b4a;
  --bg: #f6fbf8;
  --card: #ffffff;
  --muted: #6b7280;
  --text: #082018;
  --shadow-lg: 0 14px 36px rgba(31,155,74,0.14);
}

/* header with search and add button on right */
.list-header {
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:12px;
  margin-bottom: 12px;
}
.list-header .left {
  display:flex;
  gap:12px;
  align-items:center;
}
.search input {
  height: 40px;
  padding: 8px 12px;
  border-radius: 10px;
  border: 1px solid rgba(10,20,12,0.06);
  background: var(--card);
  color: var(--text);
  min-width: 320px;
}

/* rows layout: items arranged in full-width rows */
.items-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
  list-style: none;
  padding: 0;
  margin: 0;
}

/* rest styles unchanged (kept concise) */
.item-card { background: var(--card); border-radius: 12px; padding: 12px; display:flex; justify-content:space-between; align-items:center; box-shadow: var(--shadow-lg); border: 1px solid rgba(10,20,12,0.04); }
.item-main { display:flex; flex-direction:column; gap:6px; min-width:0; }
.item-title { font-size:1rem; display:flex; gap:8px; align-items:center; }
.item-meta { font-size:0.86rem; display:flex; gap:12px; flex-wrap:wrap; color:var(--muted); }
.item-actions { display:flex; gap:8px; align-items:center; white-space:nowrap; }

/* buttons */
.btn { border:none; padding:8px 10px; border-radius:8px; font-weight:700; cursor:pointer; font-size:0.9rem; }
.btn-edit { background: linear-gradient(90deg,#e6f9ef,#c9f3d6); color:#04442a; box-shadow:0 8px 20px rgba(6,121,35,0.12); }
.btn-delete { background: linear-gradient(90deg,#ffdddd,#ffc9c9); color:#5a0b0b; box-shadow:0 8px 20px rgba(140,20,20,0.06); }
.btn-undo { background:transparent; color:var(--accent); border:1px solid rgba(31,155,74,0.16); margin-left:10px; }

/* request styles */
.btn-request {
  background: linear-gradient(90deg,#60a5fa,#3b82f6);
  color: #05204a;
  box-shadow: 0 8px 20px rgba(37,99,235,0.12);
}
.btn-disabled {
  background: linear-gradient(90deg,#e6e9ee,#d7dbe1);
  color: var(--muted);
  box-shadow: none;
  cursor: not-allowed;
  border: 1px solid rgba(10,20,12,0.04);
}

/* rest unchanged */
.empty { color: var(--muted); padding:18px; background:var(--card); border-radius:8px; box-shadow:var(--shadow-lg); }

/* modal basics */
.modal-overlay { position: fixed; inset: 0; display:flex; align-items:center; justify-content:center; background: rgba(6,10,8,0.45); z-index:2000; padding:20px; }
.modal { background: var(--card); color: var(--text); border-radius:12px; width:520px; max-width:calc(100% - 40px); box-shadow:var(--shadow-lg); padding:14px; border:1px solid rgba(10,20,12,0.06); }
.field .label { font-weight:600; color:var(--muted); font-size:0.85rem; }
input[type="text"], select { padding:8px 10px; border-radius:8px; border:1px solid rgba(10,20,12,0.06); font-size:0.95rem; outline:none; }

@media (min-width: 1100px) {
  .items-grid { grid-template-columns: 1fr 1fr; gap: 14px; }
}

@media (max-width: 820px) {
  .search input { min-width: 140px; }
  .items-grid { grid-template-columns: 1fr; }
  .modal { width: 100%; max-width: 100%; padding: 12px; }
}
</style>