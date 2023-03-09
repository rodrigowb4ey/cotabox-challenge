import { createApp } from 'vue'
import App from './App.vue'

import { library } from '@fortawesome/fontawesome-svg-core'

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import { faTrashAlt } from '@fortawesome/free-solid-svg-icons'

import './assets/main.css'

library.add(faTrashAlt)

createApp(App).component('font-awesome-icon', FontAwesomeIcon).mount('#app')
