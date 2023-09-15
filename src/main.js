import { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router/router.js'
import store from './store'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-icons/font/bootstrap-icons.css';
import alertify from 'alertifyjs';
import 'alertifyjs/build/css/alertify.css';
import 'alertifyjs/build/css/themes/default.css';
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'



createApp(App).use(store).use(router).use(alertify).mount('#app')
const app = createApp(App);

// Disable Vue.js devtools

app.config.devtools = false;
app.config.debug = false
app.config.silent = true

import 'bootstrap/dist/js/bootstrap.js'