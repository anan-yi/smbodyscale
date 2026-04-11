import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import MeasurementView from '../views/MeasurementView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/measurement',
      name: 'measurement',
      component: MeasurementView,
    },
  ],
})

export default router