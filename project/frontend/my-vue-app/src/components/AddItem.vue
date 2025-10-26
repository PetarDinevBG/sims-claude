<template>
  <div class="add-item">
    <button class="btn btn-primary" @click="open" aria-haspopup="dialog" aria-expanded="false">
      + Add item
    </button>

    <div v-if="openModal" class="modal-overlay" @keydown.esc="close" tabindex="-1">
      <div class="modal" role="dialog" aria-modal="true" aria-label="Add item">
        <header class="modal-header">
          <h3>Add item</h3>
        </header>

        <section class="modal-body">
          <label class="field">
            <div class="label">Name</div>
            <input v-model="form.name" type="text" required />
          </label>

          <label class="field">
            <div class="label">Type</div>
            <input v-model="form.type" type="text" placeholder="e.g. Laptop" />
          </label>

          <label class="field">
            <div class="label">Serial number</div>
            <input v-model="form.serial_number" type="text" />
          </label>

          <label class="field">
            <div class="label">Location</div>
            <input v-model="form.location" type="text" />
          </label>

          <label class="field">
            <div class="label">Condition</div>
            <select v-model="form.condition">
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
            <select v-model="form.status">
              <option value="">(unspecified)</option>
              <option>Available</option>
              <option>Checked Out</option>
              <option>In Maintenance</option>
              <option>Lost</option>
            </select>
          </label>

          <p v-if="result" :class="{'muted': !error, 'error': error}">{{ result }}</p>
        </section>

        <footer class="modal-actions">
          <button class="btn btn-primary" @click="submit">Create</button>
          <button class="btn" @click="close">Cancel</button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
const openModal = ref(false)
const result = ref('')
const error = ref(false)

const form = reactive({
  name: '',
  type: '',
  serial_number: '',
  location: '',
  condition: '',
  status: ''
})

const token = localStorage.getItem('access_token') || ''

function open() {
  result.value = ''
  error.value = false
  openModal.value = true
}

function close() {
  openModal.value = false
  form.name = ''
  form.type = ''
  form.serial_number = ''
  form.location = ''
  form.condition = ''
  form.status = ''
}

async function submit() {
  result.value = ''
  error.value = false
  try {
    const res = await fetch('http://45.137.220.25:8000/items/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {})
      },
      body: JSON.stringify({
        name: form.name,
        type: form.type,
        serial_number: form.serial_number,
        location: form.location,
        condition: form.condition,
        status: form.status
      })
    })
    if (!res.ok) {
      const txt = await res.text().catch(() => '')
      error.value = true
      result.value = txt || 'Failed to create item'
      return
    }
    const data = await res.json()
    result.value = `Created "${data.name}"`
    // emit created event so parent can insert item into list
    // script-setup: use `defineEmits`
    emitCreated(data)
    // close modal after short delay
    setTimeout(() => {
      close()
    }, 600)
  } catch (e) {
    error.value = true
    result.value = 'Network error'
  }
}

/* emit helper (setup-safe) */
import { getCurrentInstance } from 'vue'
const instance = getCurrentInstance()
function emitCreated(payload) {
  instance?.emit?.('created', payload)
}
</script>

<style scoped>
.add-item { margin-left: 12px; }

/* reuse existing .btn and modal classes from app styles; keep minimal overrides */
.btn {
  border: none;
  padding: 8px 12px;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
}
.btn-primary {
  background: linear-gradient(90deg,#2ecc71,#06e03d);
  color: #fff;
  box-shadow: 0 8px 18px rgba(6,121,35,0.14);
}

/* modal *should* match app modal styles; provide a local baseline */
.modal-overlay {
  position: fixed;
  inset: 0;
  display:flex;
  align-items:center;
  justify-content:center;
  background: rgba(6,10,8,0.45);
  z-index: 2200;
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
.muted { color: var(--muted); }
.error { color: #e55353; }
</style>