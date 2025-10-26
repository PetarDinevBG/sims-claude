<template>
  <div class="item-list">
    <h2>Items</h2>

    <ul v-if="items.length" class="items-grid" role="list">
      <li v-for="(item, idx) in items" :key="item.id" class="item-card" role="listitem" :aria-label="item.name">
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

    <!-- Edit modal/menu -->
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

// ...existing code...

const items = ref([])
const lastDeleted = ref(null) // { item, index, timerId, expiresAt }
const undoTimeoutMs = 10000
const undoTimeoutSec = ref(Math.round(undoTimeoutMs / 1000))

// decode JWT payload to determine admin role (same approach as Navbar)
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

// EDIT: menu/modal editing
const editingItem = ref(null) // current item object being edited
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
  editingIndex.value = idx
  editForm.id = item.id
  editForm.name = item.name ?? ''
  editForm.type = item.type ?? ''
  editForm.serial_number = item.serial_number ?? ''
  editForm.location = item.location ?? ''
  editForm.condition = item.condition ?? ''
  editForm.status = item.status ?? ''
  // focus handled by browser; modal captures esc key via overlay
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
  // optimistic update locally
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
      // rollback on server error
      items.value[idx] = prev
      const text = await res.text().catch(() => '')
      alert('Failed to save changes' + (text ? ': ' + text : ''))
    }
  } catch (err) {
    // network error, rollback and notify
    items.value[idx] = prev
    alert('Network error while saving changes')
  } finally {
    closeEditMenu()
  }
}

// keep older minimal editItem for compatibility (opens modal)
function editItem(item, idx) {
  openEditMenu(item, idx)
}

async function deleteItem(item, idx) {
  // optimistic remove
  const removed = items.value.splice(idx, 1)[0]
  // clear any existing undo for a different item
  if (lastDeleted.value && lastDeleted.value.timerId) {
    clearInterval(lastDeleted.value.countdownId)
    clearTimeout(lastDeleted.value.timerId)
  }

  const timerId = setTimeout(() => {
    lastDeleted.value = null
  }, undoTimeoutMs)

  // maintain countdown seconds for UI
  const start = Date.now()
  undoTimeoutSec.value = Math.round((undoTimeoutMs) / 1000)
  const countdownId = setInterval(() => {
    const elapsed = Date.now() - start
    const left = Math.max(0, Math.ceil((undoTimeoutMs - elapsed) / 1000))
    undoTimeoutSec.value = left
    if (left <= 0) clearInterval(countdownId)
  }, 250)

  lastDeleted.value = { item: removed, index: idx, timerId, countdownId, expiresAt: Date.now() + undoTimeoutMs }

  // send delete request (best-effort). If fails, keep local deletion but could restore automatically.
  try {
    await fetch(`http://45.137.220.25:8000/items/${item.id}/`, {
      method: 'DELETE',
      headers: { Authorization: token.value ? `Bearer ${token.value}` : undefined }
    })
  } catch {
    // network fail — item already removed locally; Undo will re-insert locally and attempt re-create
  }
}

async function undoDelete() {
  if (!lastDeleted.value) return
  const { item, index, timerId, countdownId } = lastDeleted.value
  clearTimeout(timerId)
  clearInterval(countdownId)

  // Try to restore by re-inserting locally immediately
  const insertIndex = Math.min(index, items.value.length)
  items.value.splice(insertIndex, 0, item)

  // attempt to restore on backend: try PATCH first (in case record still exists), else POST
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

.item-list {
  max-width: 1100px;
  margin: 20px auto;
  padding: 12px;
}

h2 {
  margin: 6px 0 14px;
  color: var(--text);
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

.item-card {
  background: var(--card);
  border-radius: 12px;
  padding: 12px;
  display: flex;
  justify-content: space-between;
  gap: 10px;
  align-items: center;
  box-shadow: var(--shadow-lg);
  transition: transform 0.12s ease, box-shadow 0.12s ease;
  border: 1px solid rgba(10,20,12,0.04);
}
.item-card:hover { transform: translateY(-4px); }

.item-main {
  display: flex;
  flex-direction: column;
  gap: 6px;
  color: var(--text);
  min-width: 0;
}

.item-title { font-size: 1rem; display:flex; gap:8px; align-items:center; }
.item-meta { font-size: 0.86rem; display:flex; gap:12px; flex-wrap:wrap; color: var(--muted); }

.item-actions {
  display:flex;
  gap:8px;
  align-items:center;
  white-space:nowrap;
}

/* buttons */
.btn {
  border: none;
  padding: 8px 10px;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
  font-size: 0.9rem;
}

.btn-edit {
  background: linear-gradient(90deg,#e6f9ef,#c9f3d6);
  color: #04442a;
  box-shadow: 0 8px 20px rgba(6,121,35,0.12);
}
.btn-delete {
  background: linear-gradient(90deg,#ffdddd,#ffc9c9);
  color: #5a0b0b;
  box-shadow: 0 8px 20px rgba(140, 20, 20, 0.06);
}
.btn-undo {
  margin-left: 10px;
  background: transparent;
  color: var(--accent);
  border: 1px solid rgba(31,155,74,0.16);
}

.empty {
  color: var(--muted);
  padding: 18px;
  background: var(--card);
  border-radius: 8px;
  box-shadow: var(--shadow-lg);
}

/* undo bar */
.undo-bar {
  margin-top: 14px;
  padding: 10px 14px;
  background: linear-gradient(90deg, rgba(31,155,74,0.06), rgba(31,155,74,0.03));
  border-radius: 10px;
  display:flex;
  gap:10px;
  align-items:center;
  justify-content:flex-start;
  color: var(--text);
}
.muted { color: var(--muted); font-weight: 500; font-size: 0.88rem; }

/* Modal styles */
.modal-overlay {
  position: fixed;
  inset: 0;
  display:flex;
  align-items:center;
  justify-content:center;
  background: rgba(6,10,8,0.45);
  z-index: 2000;
  padding: 20px;
}
.modal {
  background: var(--card);
  color: var(--text);
  border-radius: 12px;
  width: 520px;
  max-width: calc(100% - 40px);
  box-shadow: var(--shadow-lg);
  padding: 14px;
  border: 1px solid rgba(10,20,12,0.06);
}
.modal-header h3 { margin: 0 0 8px 0; }
.modal-body { display:flex; flex-direction:column; gap:10px; margin-bottom: 8px; }
.field { display:flex; flex-direction:column; gap:6px; }
.field .label { font-weight:600; color:var(--muted); font-size:0.85rem; }
input[type="text"], select {
  padding: 8px 10px;
  border-radius: 8px;
  border: 1px solid rgba(10,20,12,0.06);
  font-size: 0.95rem;
  outline: none;
}
.modal-actions { display:flex; gap:8px; justify-content:flex-end; }
.btn-primary {
  background: linear-gradient(90deg,#2ecc71,#06e03d);
  color: #032018;
  border: none;
  padding: 8px 14px;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 8px 18px rgba(6,121,35,0.14);
}

@media (min-width: 1100px) {
  /* on very wide screens show two columns of rows for density */
  .items-grid { grid-template-columns: 1fr 1fr; gap: 14px; }
}

@media (max-width: 820px) {
  .items-grid { grid-template-columns: 1fr; }
  .item-actions { gap:6px; }
  .modal { width: 100%; max-width: 100%; padding: 12px; }
}
</style>