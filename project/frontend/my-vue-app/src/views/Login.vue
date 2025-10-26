<template>
  <div class="page">
    <div class="card">
      <header class="card-header">
        <h2>Welcome Back</h2>
        <p class="muted">Sign in to continue to School Inventory</p>
      </header>

      <form class="form" @submit.prevent="login" novalidate>
        <label class="field">
          <span class="label-text">Username</span>
          <input v-model="username" required autocomplete="username" />
        </label>

        <label class="field pwd-field">
          <span class="label-text">Password</span>
          <div class="pwd-row">
            <input
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              required
              autocomplete="current-password"
              class="with-toggle"
            />
            <button
              class="pwd-toggle"
              type="button"
              @click="togglePassword"
              :aria-pressed="String(showPassword)"
              :aria-label="showPassword ? 'Hide password' : 'Show password'"
            >
              <!-- eye open (show) when password is hidden -->
              <svg v-if="!showPassword" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
                <path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12z" stroke="currentColor" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="1.5" fill="none"/>
              </svg>
              <!-- eye-off (hide) when password is visible -->
              <svg v-else viewBox="0 0 24 24" aria-hidden="true" focusable="false">
                <path d="M17.94 17.94A10.94 10.94 0 0 1 12 19c-7 0-11-7-11-7a20.6 20.6 0 0 1 5.08-6.06" stroke="currentColor" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M1 1l22 22" stroke="currentColor" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
        </label>

        <div class="actions">
          <button class="btn primary" type="submit">Login</button>
          <button class="btn outline" type="button" @click="registUser">Register</button>
        </div>

        <p v-if="error" class="error">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref("");
const password = ref("");
const error = ref("");

const showPassword = ref(false)
const togglePassword = () => { showPassword.value = !showPassword.value }

const login = async () => {
  try {
    const res = await fetch('http://45.137.220.25:8000/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      })
    })
    const data = await res.json()
    if (data.access_token) {
      localStorage.setItem("access_token", data.access_token);
      window.dispatchEvent(new Event('auth-change'))
      router.push('/')
    } else {
      error.value = data.detail || 'Error during login'
    }
  } catch (err) {
    console.error(err);
    error.value = "Invalid username or password.";
  }
};

const registUser = () => {
  router.push('/register')
}
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
}

.page{
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg, linear-gradient(180deg, #eef9f2 0%, #f6fbf8 100%));
  padding: 48px 16px;
  color: var(--text, #082018);
}

.card{
  width: 100%;
  max-width: 460px;
  background: var(--card, #ffffff);
  border-radius: 12px;
  box-shadow: var(--shadow-lg, 0 10px 30px rgba(31,155,74,0.12));
  padding: 30px;
  border: 1px solid rgba(46,139,87,0.06);
  transition: transform .08s ease, box-shadow .12s ease;
}

.card:hover {
  transform: translateY(-2px);
}

.card-header {
  text-align: center;
  margin-bottom: 20px;
}

.card-header h2 {
  margin: 0;
  color: var(--accent, #1f8a4d);
  font-size: 1.5rem;
  font-weight: 800;
  letter-spacing: -0.01em;
}

.muted {
  margin: 6px 0 0;
  color: var(--muted, #6b7280);
  font-size: 0.95rem;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.label-text {
  font-size: 0.88rem;
  color: var(--muted, #374151);
  font-weight: 600;
}

.field input {
  width: 100%;
  box-sizing: border-box;
  height: 48px;
  padding: 10px 12px;
  border: 1px solid rgba(15, 23, 42, 0.06);
  border-radius: 10px;
  background: var(--card, #fbfffb);
  outline: none;
  font-size: 1rem;
  transition: box-shadow 0.12s ease, border-color 0.12s ease, background .12s ease;
  color: var(--text, #082018);
}

.pwd-row { position: relative; }

.with-toggle {
  padding-right: 48px;
}

.pwd-toggle {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  width: 40px;
  height: 40px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  color: var(--accent, #1f8a4d);
  transition: background 0.12s ease, transform 0.06s ease;
}

.pwd-toggle:hover { background: rgba(0,0,0,0.04); }
.pwd-toggle:active { transform: translateY(-49%); }

.pwd-toggle svg {
  width: 18px;
  height: 18px;
  stroke: currentColor;
  fill: none;
}

input:focus {
  box-shadow: 0 0 0 6px rgba(46,139,87,0.06);
  border-color: var(--accent, #1f8a4d);
}

.actions {
  display: flex;
  gap: 12px;
  margin-top: 6px;
}

.btn {
  flex: 1;
  height: 48px;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
  border: 1px solid transparent;
  transition: transform 0.06s ease, box-shadow 0.08s ease, opacity .12s ease;
  color: var(--text, #082018);
}

.btn:active { transform: translateY(1px); }

.btn.primary {
  background: linear-gradient(90deg, var(--accent, #2ecc71), #1f8a4d);
  color: var(--card, #ffffff);
  box-shadow: 0 10px 28px rgba(31,155,74,0.14);
  border: 1px solid rgba(10, 80, 35, 0.08);
}

.btn.primary:hover {
  filter: brightness(0.98);
  box-shadow: 0 12px 36px rgba(31,155,74,0.18);
  transform: translateY(-1px);
}

.btn.primary:focus {
  outline: 3px solid rgba(46,139,87,0.12);
  outline-offset: 2px;
}

.btn.outline {
  background: transparent;
  color: var(--accent, #1f8a4d);
  border: 1px solid rgba(46,139,87,0.12);
}

.error {
  margin-top: 8px;
  color: var(--error, #e55353);
  font-size: 0.95rem;
  text-align: center;
}

/* Responsive */
@media (max-width: 520px){
  .card { padding: 20px; }
  .actions { flex-direction: column; }
  .btn { height: 44px; }
}
</style>