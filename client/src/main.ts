import 'quasar/dist/quasar.css'

import {createApp} from 'vue'
import App from './App.vue'
import {Quasar} from "quasar";
import vue3GoogleLogin from 'vue3-google-login'

createApp(App)
    .use(Quasar, {})
    .use(vue3GoogleLogin, {
        clientId: `${import.meta.env.VITE_GOOGLE_LOGIN_CLIENT_ID}`
    })
    .mount('#app')
