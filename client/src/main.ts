import 'quasar/dist/quasar.css'

import {createApp} from 'vue'
import App from './App.vue'
import {Quasar} from "quasar";

createApp(App)
    .use(Quasar, {})
    .mount('#app')
