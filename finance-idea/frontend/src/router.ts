import { createRouter, createWebHistory } from 'vue-router'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'dashboard',
      component: () => import('./views/DashboardView.vue') },
    { path: '/idea/:id', name: 'idea',
      component: () => import('./views/IdeaDetailView.vue'), props: true },
  ],
})
