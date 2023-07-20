import 'quasar/dist/quasar.css'
import '@quasar/extras/material-icons/material-icons.css'

import {createApp} from 'vue'
import App from './App.vue'
import {Quasar} from "quasar";
import vue3GoogleLogin from 'vue3-google-login'
import {ApiClientAxios} from "./api/api-client-axios.ts";
import {createPinia} from "pinia";

createApp(App)
    .use(Quasar, {})
    .use(vue3GoogleLogin, {
        clientId: `${import.meta.env.VITE_GOOGLE_LOGIN_CLIENT_ID}`
    })
    .use(ApiClientAxios)
    .use(createPinia())
    .mount('#app')
