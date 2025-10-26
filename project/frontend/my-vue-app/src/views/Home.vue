// ...existing code...
<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const itemsCount = ref(null)
const requestsCount = ref(null)
const usersCount = ref(null)
const loading = ref(true)

async function loadCounts() {
  loading.value = true
  try {
    const [itemsRes, reqRes, usersRes] = await Promise.all([
      fetch('http://45.137.220.25:8000/items/'),
      fetch('http://45.137.220.25:8000/requests/'),
      fetch('http://45.137.220.25:8000/users/')
    ])
    if (itemsRes.ok) itemsCount.value = (await itemsRes.json()).length
    if (reqRes.ok) requestsCount.value = (await reqRes.json()).length
    if (usersRes.ok) usersCount.value = (await usersRes.json()).length
  } catch (e) {
    itemsCount.value = itemsCount.value ?? '-'
    requestsCount.value = requestsCount.value ?? '-'
    usersCount.value = usersCount.value ?? '-'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadCounts()
})
</script>

<template>
  <main class="home-page">
    <section class="hero">
      <div class="hero-body">
        <div class="hero-left">
          <h1 class="title">School Equipment Inventory</h1>
          <p class="lead">
            A simple, secure system to track school equipment — laptops, projectors, lab gear and more.
            Staff can list and manage items; students and teachers can request equipment for use; admins review and approve requests.
          </p>

          <div class="cta">
            <button class="btn btn-primary" @click="router.push('/items')">Browse equipment</button>
            <button class="btn btn-outline" @click="router.push('/requests')">View requests</button>
          </div>
        </div>

        <div class="hero-right">
          <div class="stats">
            <div class="stat">
              <div class="num">{{ loading ? '—' : (itemsCount ?? '—') }}</div>
              <div class="label">Items</div>
            </div>
            <div class="stat">
              <div class="num">{{ loading ? '—' : (requestsCount ?? '—') }}</div>
              <div class="label">Requests</div>
            </div>
            <div class="stat">
              <div class="num">{{ loading ? '—' : (usersCount ?? '—') }}</div>
              <div class="label">Users</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="features">
      <h2>How it helps your school</h2>
      <div class="feature-grid">
        <div class="feature">
          <h3>Track equipment</h3>
          <p>Keep a single source of truth for all school-owned devices and supplies — location, condition and serial numbers.</p>
        </div>

        <div class="feature">
          <h3>Request workflow</h3>
          <p>Users submit requests for items. Administrators review, approve or decline, keeping records of who has what.</p>
        </div>

        <div class="feature">
          <h3>Simple admin tools</h3>
          <p>Admins can add, edit, delete items and manage user roles — fast operations with audit-friendly changes.</p>
        </div>
      </div>
    </section>

   
  </main>
</template>

<style scoped>
.home-page {
  max-width: 1100px;
  margin: 28px auto;
  padding: 18px;
  color: var(--text, #082018);
}

/* HERO */
.hero {
  background: linear-gradient(180deg, rgba(46,139,87,0.06), rgba(46,139,87,0.02));
  border-radius: 14px;
  padding: 22px;
  box-shadow: var(--shadow-lg, 0 12px 36px rgba(31,155,74,0.08));
  margin-bottom: 20px;
}

.hero-body {
  display: flex;
  gap: 18px;
  align-items: center;
  justify-content: space-between;
}

.hero-left { flex: 1 1 60%; min-width: 280px; }
.hero-right { flex: 0 0 260px; }

.title {
  margin: 0 0 8px 0;
  font-size: 1.9rem;
  color: var(--accent, #1f9b4a);
  letter-spacing: -0.01em;
}
.lead {
  margin: 0 0 16px 0;
  color: var(--muted, #4b5563);
  font-size: 1.02rem;
  line-height: 1.45;
}

.cta { display:flex; gap:12px; margin-top: 6px; }
.btn {
  border: none;
  padding: 10px 14px;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
}
.btn-primary {
  background: linear-gradient(90deg,#16a34a,#059669);
  color: #fff;
  box-shadow: 0 10px 28px rgba(5,118,61,0.12);
}
.btn-outline {
  background: transparent;
  border: 1px solid rgba(10,20,12,0.06);
  color: var(--text, #082018);
}

/* STATS */
.stats {
  display:flex;
  gap: 12px;
  background: rgba(255,255,255,0.9);
  padding: 12px;
  border-radius: 10px;
  justify-content: space-between;
  align-items: center;
}
.stat { text-align: center; min-width: 70px; }
.stat .num { font-size: 1.4rem; font-weight: 800; color: var(--text, #082018); }
.stat .label { color: var(--muted, #6b7280); font-size: 0.9rem; margin-top: 6px; }

/* FEATURES */
.features { margin-top: 20px; padding: 6px 2px; }
.features h2 { margin-bottom: 12px; color: var(--text); }
.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}
.feature {
  background: var(--card, #fff);
  border-radius: 10px;
  padding: 14px;
  box-shadow: 0 8px 22px rgba(6,121,35,0.06);
}
.feature h3 { margin: 0 0 8px 0; color: var(--accent); }
.feature p { margin: 0; color: var(--muted); }

/* FOOTER CTA */
.footer-cta { margin-top: 20px; text-align: center; padding: 18px; background: transparent; border-radius: 10px; }
.footer-cta .muted { color: var(--muted); margin-bottom: 10px; display:block; }

/* Responsive */
@media (max-width: 920px) {
  .hero-body { flex-direction: column; align-items: stretch; }
  .feature-grid { grid-template-columns: 1fr; }
  .hero-right { margin-top: 12px; }
  .stats { justify-content: space-around; }
}
</style>
// ...existing code...