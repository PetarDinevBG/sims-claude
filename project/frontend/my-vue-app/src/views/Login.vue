<template>
  <div class="login">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <input v-model="username" placeholder="Username" />
      <input v-model="password" type="password" placeholder="Password" />
      <button type="submit">Login</button>
    </form>
     <button @click="registUser"> Register </button>
    <p v-if="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref("");
const password = ref("");
const error = ref("");

const login = async () => {
  try {
    const formData = new URLSearchParams();
    formData.append("username", username.value);
    formData.append("password", password.value);
    const res = await fetch('http://45.137.220.25:8000/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
        })})
    const data = await res.json()
    if(data.access_token){
        localStorage.setItem("access_token", data.access_token);
        alert("Login successful!");
         window.dispatchEvent(new Event('auth-change'))
        router.push('/')
    }else{
      alert("Error during login!");
    }

  } catch (err) {
    console.log(err);
    error.value = "Invalid username or password.";
  }
};
const registUser = () => {
  router.push('/register')
}
</script>

<style scoped>
.login {
  max-width: 300px;
  margin: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
