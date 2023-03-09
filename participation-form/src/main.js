import { createApp } from 'vue'
import App from './App.vue'

import { library } from '@fortawesome/fontawesome-svg-core'

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import VueSweetAlert2 from 'vue-sweetalert2'
import 'sweetalert2/dist/sweetalert2.min.css'

import { faTrashAlt } from '@fortawesome/free-solid-svg-icons'

import './assets/main.css'

library.add(faTrashAlt)

const app = createApp(App)
app.use(VueSweetAlert2)
app.component('font-awesome-icon', FontAwesomeIcon)
app.mount('#app')
