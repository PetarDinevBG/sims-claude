import { createRouter, createWebHistory } from 'vue-router'
import UserView from '../views/UserView.vue'
import Home from '../views/Home.vue'
import ItemView from '../views/ItemView.vue'
import Login from '../views/Login.vue' 
import RegisterView from '../views/Register.vue'
import RequestView from '../views/RequestsView.vue'
const routes = [
  { path: '/', component: Home },
  { path: '/users', component: UserView },
  { path: '/items', component: ItemView, meta: { requiresAuth: true } },
  { path: '/login', component: Login},
  { path: '/register', component: RegisterView },
  { path: '/requests', component: RequestView, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})
// Navigation guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  if (to.meta.requiresAuth && !token) {
    next('/login') // redirect to login if no token
  } else {
    next()
  }
})
export default router