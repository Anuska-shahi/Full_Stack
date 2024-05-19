import { createApp } from 'vue'
import App from './App.vue'
import router from './router';
import './index.css'

import ToastPlugin from 'vue-toast-notification';
import 'vue-toast-notification/dist/theme-bootstrap.css';

import axios from 'axios'
axios.defaults.baseURL='http://127.0.0.1:8000/account/user/'

const app = createApp(App);
app.use(router); 
app.use(ToastPlugin);
app.mount('#app');