<template>
  <div>
    <h2>Items</h2>
    <ul>
      <li v-for="item in items" :key="item.id">
        {{ item.name }} ({{ item.type }})
      </li>
    </ul>
    <div v-if="items.length === 0">No items found.</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const items = ref([])

onMounted(async () => {
  const response = await fetch('http://45.137.220.25:8000/items/')
  if (response.ok) {
    items.value = await response.json()
  }
})
</script>