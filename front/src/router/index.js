import { createRouter, createWebHistory } from 'vue-router'
import Clients from '../views/Clients.vue'
import MainPage from "@/views/MainPage.vue";

const routes = [
  {
    path: "/",
    name: "tasks",
    component: MainPage
  },
  {
    path: "/clients",
    name: "clients",
    component: Clients
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
