<template>
  <div class="request-list">
    <h2>Requests</h2>

    <div v-if="!loaded" class="empty">Loading requests…</div>

    <!-- Non-admins: show only their own requests -->
    <div v-else-if="!isAdmin">
      <h3>Your requests</h3>
      <table v-if="userRequests.length" class="req-table" role="table" aria-label="Your requests">
        <thead>
          <tr>
            <th>Request ID</th>
            <th>Item</th>
            <th>Status</th>
            <th>Requested At</th>
            <th>Reviewed At</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in userRequests" :key="r.id">
            <td class="muted">{{ r.id }}</td>
            <td>
              <div class="small-strong">{{ itemName(r.item_id) || ('#' + r.item_id) }}</div>
              <div class="muted small">{{ itemType(r.item_id) }}</div>
            </td>
            <td><span class="status" :data-status="r.status">{{ r.status ?? 'pending' }}</span></td>
            <td class="muted small">{{ formatDate(r.requested_at) }}</td>
            <td class="muted small">{{ formatDate(r.reviewed_at) }}</td>
          </tr>
        </tbody>
      </table>

      <div v-else class="empty">You have not submitted any requests.</div>
    </div>

    <!-- Admins: show all requests with requester column and approve/decline actions -->
    <div v-else>
      <table class="req-table" role="table" aria-label="All requests">
        <thead>
          <tr>
            <th>Request ID</th>
            <th>Item</th>
            <th>Requester</th>
            <th>Status</th>
            <th>Requested At</th>
            <th>Reviewed At</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in requests" :key="r.id">
            <td class="muted">{{ r.id }}</td>
            <td>
              <div class="small-strong">{{ itemName(r.item_id) || ('#' + r.item_id) }}</div>
              <div class="muted small">{{ itemType(r.item_id) }}</div>
            </td>
            <td>
              <div class="small-strong">{{ userName(r.user_id) || ('#' + r.user_id) }}</div>
              <div class="muted small">{{ userEmail(r.user_id) }}</div>
            </td>
            <td><span class="status" :data-status="r.status">{{ r.status ?? 'pending' }}</span></td>
            <td class="muted small">{{ formatDate(r.requested_at) }}</td>
            <td class="muted small">{{ formatDate(r.reviewed_at) }}</td>
            <td>
              <div class="actions-col">
                <button
                  class="btn btn-approve"
                  v-if="r.status === 'pending' && !processing[r.id]"
                  @click="updateRequestStatus(r, 'approved')"
                >Approve</button>

                <button
                  class="btn btn-decline"
                  v-if="r.status === 'pending' && !processing[r.id]"
                  @click="updateRequestStatus(r, 'rejected')"
                >Decline</button>

                <span v-if="processing[r.id]" class="muted small">Processing…</span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="requests.length === 0" class="empty">No requests found.</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

const requests = ref([])
const itemsMap = ref({})
const usersMap = ref({})
const loaded = ref(false)
const processing = ref({}) // per-request processing flags

const token = ref(localStorage.getItem('access_token') || '')

// decode JWT payload to get user id / role
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

const payload = decodeJwtPayload(token.value) || {}
console.log(payload)
const userId = payload.id ?? payload.user_id ?? (typeof payload.sub === 'number' ? payload.sub : null)
const isAdmin = computed(() => {
  if (!payload) return false
  if (payload.role && payload.role === 'admin') return true
  if (Array.isArray(payload.roles) && payload.roles.includes('admin')) return true
  return false
})

function formatDate(s) {
  if (!s) return '-'
  try {
    const d = new Date(s)
    if (isNaN(d.getTime())) return s
    return d.toLocaleString()
  } catch {
    return s
  }
}

function itemName(id) {
  return itemsMap.value[id]?.name || ''
}
function itemType(id) {
  return itemsMap.value[id]?.type || ''
}
function userName(id) {
  return usersMap.value[id]?.username || ''
}
function userEmail(id) {
  return usersMap.value[id]?.email || ''
}

async function loadAll() {
  loaded.value = false
  try {
    const [reqRes, itemsRes, usersRes] = await Promise.all([
      fetch('http://45.137.220.25:8000/requests/'),
      fetch('http://45.137.220.25:8000/items/'),
      fetch('http://45.137.220.25:8000/users/')
    ])

    if (itemsRes.ok) {
      const its = await itemsRes.json()
      itemsMap.value = its.reduce((acc, it) => { acc[it.id] = it; return acc }, {})
    } else {
      itemsMap.value = {}
    }

    if (usersRes.ok) {
      const us = await usersRes.json()
      usersMap.value = us.reduce((acc, u) => { acc[u.id] = u; return acc }, {})
    } else {
      usersMap.value = {}
    }

    if (reqRes.ok) {
      const allReqs = await reqRes.json()
      console.log('Loaded requests:', userId)

      // if user is admin, keep all; otherwise keep only those requested by the current user
      if (isAdmin.value) {
        requests.value = allReqs
      } else {
        // if we don't have a userId, show empty list
        if (!userId) {
          requests.value = []
        } else {
          requests.value = allReqs.filter(r => Number(r.user_id) === Number(userId))
        }
      }
    } else {
      requests.value = []
    }
  } catch (e) {
    requests.value = []
  } finally {
    loaded.value = true
  }
}

onMounted(() => {
  loadAll()
})

// derived list for non-admin UI
const userRequests = computed(() => {
  if (!userId) return []
  return requests.value.filter(r => Number(r.user_id) === Number(userId))
})

// update request status (admin action)
async function updateRequestStatus(req, newStatus) {
  if (!isAdmin.value) return
  processing.value[req.id] = true
  try {
    const res = await fetch(`http://45.137.220.25:8000/requests/${req.id}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        ...(token.value ? { Authorization: `Bearer ${token.value}` } : {})
      },
      body: JSON.stringify({ status: newStatus })
    })
    if (!res.ok) {
      const txt = await res.text().catch(() => '')
      alert('Failed to update request' + (txt ? ': ' + txt : ''))
      return
    }
    const updated = await res.json()
    // update local copy
    const idx = requests.value.findIndex(r => r.id === updated.id)
    if (idx !== -1) requests.value[idx] = updated
    else {
      // if not found, reload all
      await loadAll()
    }
  } catch (e) {
    alert('Network error while updating request')
  } finally {
    processing.value[req.id] = false
  }
}
</script>

<style scoped>
.request-list { max-width: 1100px; margin: 18px auto; padding: 12px; }
h2 { margin: 4px 0 12px; color: var(--text, #082018); }
h3 { margin: 8px 0; color: var(--text, #082018); }

.req-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--card, #fff);
  border-radius: 10px;
  overflow: hidden;
  box-shadow: var(--shadow-lg, 0 10px 30px rgba(31,155,74,0.08));
}
.req-table thead { background: linear-gradient(90deg, rgba(0,0,0,0.02), rgba(0,0,0,0.01)); }
.req-table th, .req-table td {
  padding: 12px 14px;
  text-align: left;
  border-bottom: 1px solid rgba(10,20,12,0.04);
  font-size: 0.95rem;
}
.req-table tbody tr:last-child td { border-bottom: none; }

.muted { color: var(--muted, #6b7280); }
.small { font-size: 0.85rem; }
.small-strong { font-weight: 700; }

.status {
  display: inline-block;
  padding: 6px 10px;
  border-radius: 999px;
  font-weight: 700;
  font-size: 0.85rem;
  color: #082018;
  background: rgba(150, 150, 150, 0.08);
}
.status[data-status="approved"] { background: rgba(34,197,94,0.12); color: #064e2a; }
.status[data-status="Pending"], .status[data-status="pending"] { background: rgba(249,115,22,0.06); color: #7c2d12; }
.status[data-status="rejected"], .status[data-status="denied"] { background: rgba(244,63,94,0.06); color: #58121a; }

.empty { color: var(--muted, #6b7280); padding: 18px; border-radius: 8px; margin-top: 12px; }

.actions-col { display:flex; gap:8px; align-items:center; }
.btn { border:none; padding:8px 10px; border-radius:8px; font-weight:700; cursor:pointer; font-size:0.9rem; }
.btn-approve { background: linear-gradient(90deg,#86efac,#22c55e); color:#08310f; }
.btn-decline { background: linear-gradient(90deg,#ffb4b4,#ff6b6b); color:#5a0b0b; }
</style>