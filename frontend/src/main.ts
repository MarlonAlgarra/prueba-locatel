import App from './App.vue'
import { createApp } from 'vue'
import { registerPlugins } from '@/plugins'
import axios from 'axios'
import store from './store';
import router from './router';

const app = createApp(App)
app.config.globalProperties.$axios = axios;
axios.defaults.baseURL = 'http://localhost:8000/api/';
const savedState = JSON.parse(localStorage.getItem('myAppData') || null);
registerPlugins(app)

router.beforeEach((to, from, next) => {
    const isAuthenticated = sessionStorage.getItem('token');
    if (to.meta.requiresAuth) {
      if (isAuthenticated) {
        next();
      } else {
        next('/');
      }
    } else {
        if (isAuthenticated) {
            if(to.path === '/login' || to.path === '/signup' || to.path === '/'){
                next('/dashboard');
            }
        }

      next();
    }
  });
app.use(store)
if (savedState) {
  store.replaceState(savedState);
}
app.mount('#app')
