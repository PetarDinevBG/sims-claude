<template>
  <form @submit.prevent="addItem">
    <input v-model="name" placeholder="Name" required />
    <input v-model="type" placeholder="Type" required />
    <button type="submit">Add Item</button>
    <div v-if="result">{{ result }}</div>
  </form>
</template>

<script setup>
import { ref } from 'vue'

const name = ref('')
const type = ref('')
const result = ref('')

const addItem = async () => {
  try {
    const response = await fetch('http://45.137.220.25:8000/items/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: name.value,
        type: type.value,
      }),
    })
    if (!response.ok) throw new Error(await response.text())
    const data = await response.json()
    result.value = `Item ${data.name} created!`
    name.value = ''
    type.value = ''
  } catch (e) {
    result.value = `Error: ${e}`
  }
}
</script>