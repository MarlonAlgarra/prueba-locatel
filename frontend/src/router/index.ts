// Composables
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('@/views/Home.vue'),
      },
      {
        path: '/login',
        name: 'login',
        component: () => import('@/views/Login.vue'),
      },
      {
        path: '/signup',
        name: 'signup',
        component: () => import('@/views/SignUp.vue'),
      },
    ],
  },
  {
    path: '/dashboard',
    component: () => import('@/layouts/dashboard/DefaultDash.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '/dashboard',
        name: 'dashboard',
        component: () => import('@/views/Dashboard.vue'),
      },
      {
        path: '/dashboard/activity',
        name: 'activity',
        component: () => import( '@/views/Activity.vue'),
      },
    ]
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
