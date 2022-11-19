import { createRouter, createWebHistory } from 'vue-router'
import Clients from '../views/Clients.vue'
import MainPage from "@/views/MainPage.vue";
import LoginPage from "@/views/LoginPage";

const routes = [
  {
    path: "/",
    name: "login",
    component: LoginPage
  },
  {
    path: "/tasks",
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
