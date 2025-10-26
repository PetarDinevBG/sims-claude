// ...existing code...
<script setup>
import UserList from '../components/UserList.vue';
</script>

<template>
  <div class="admin-page">
    <header class="hero">
      <div class="hero-inner">
        <div class="hero-title">
          <h1>Admin Panel</h1>
          <p class="lead">Manage users, change roles and delete accounts — quick and secure.</p>
        </div>
      </div>
    </header>

    <main class="layout">
      <aside class="side">
        <div class="card small">
          <div class="card-header">
            <h2 class="card-title">Admin Tools</h2>
          </div>
          <p>Use the panel to the right to manage users. You can change roles or delete accounts as needed.</p>
          <small class="muted">Ensure you have the necessary permissions before making changes.</small>
   
        </div>
      </aside>

      <section class="content">
        <div class="card">
          <div class="card-header">
            <h2 class="card-title">Users</h2>
            <p class="card-sub">View, edit roles and remove users</p>
          </div>

          <UserList />
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
:root {
  --bg: #f6f8fb;
  --card: #ffffff;
  --muted: #6b7280;
  --accent: #2563eb;
  --glass: rgba(255,255,255,0.6);
  --shadow: 0 8px 24px rgba(16,24,40,0.06);
}

.admin-page {
  max-width: 1200px;
  margin: 28px auto;
  padding: 0 20px 60px;
  color: #0f1720;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
}

/* Hero */
.hero {
  background: linear-gradient(135deg, rgba(37,99,235,0.08), rgba(99,102,241,0.04));
  border-radius: 14px;
  padding: 22px;
  display: flex;
  align-items: center;
  box-shadow: var(--shadow);
  border: 1px solid rgba(37,99,235,0.06);
}

.hero-inner {
  width: 100%;
}

.hero-title h1 {
  margin: 0;
  font-size: 1.6rem;
  letter-spacing: -0.02em;
  color: #0b2546;
}

.lead {
  margin: 6px 0 0;
  color: var(--muted);
  font-size: 0.95rem;
}

/* Layout */
.layout {
  display: grid;
  grid-template-columns: 360px 1fr;
  gap: 20px;
  margin-top: 18px;
  align-items: start;
}

/* Cards */
.card {
  background: var(--card);
  border-radius: 12px;
  padding: 16px;
  box-shadow: var(--shadow);
  border: 1px solid rgba(16,24,40,0.04);
}

.card.small {
  padding: 14px;
}

.card-header {
  display:flex;
  justify-content:space-between;
  align-items:flex-start;
  gap:12px;
  margin-bottom:12px;
}

.card-title {
  margin: 0 0 6px 0;
  font-size: 1.05rem;
  font-weight: 700;
  color: #0f1720;
}

.card-sub {
  margin: 0;
  color: var(--muted);
  font-size: 0.9rem;
}

/* Side panel tweaks */
.side .card {
  position: sticky;
  top: 20px;
}

/* Responsiveness */
@media (max-width: 980px) {
  .layout {
    grid-template-columns: 1fr;
  }
  .side .card {
    position: static;
  }
  .hero {
    padding: 16px;
  }
  .hero-title h1 { font-size: 1.35rem; }
}

/* small visual polish */
.card small {
  color: var(--muted);
  display: block;
  margin-top: 8px;
}

/* Ensure UserList inside fits card padding */
.content .card > .user-list {
  margin: 0;
  background: transparent;
  box-shadow: none;
  border: none;
  padding: 0;
}
</style>
// ...existing code...