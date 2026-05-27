import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
import { router } from './router'

// Restore theme preference
const t = localStorage.getItem('theme')
if (t === 'light') document.documentElement.classList.add('light')

createApp(App).use(createPinia()).use(router).mount('#app')
