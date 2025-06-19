import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue' // This is now the new landing page
import About from './views/About.vue'
import MappingPage from './views/MappingPage.vue' // Import the new MappingPage

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/mapping', // New route for the mapping tool
    name: 'MappingPage',
    component: MappingPage
  },
  {
    path: '/about',
    name: 'About',
    component: About
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
