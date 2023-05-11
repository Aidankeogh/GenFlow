import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'

/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'

/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

/* import specific icons */
import { faHouse, faChalkboard, faPenToSquare, faGear, faFileCsv, faFloppyDisk } from '@fortawesome/free-solid-svg-icons'

/* add icons to the library */
library.add(faHouse, faChalkboard, faPenToSquare, faGear, faFileCsv, faFloppyDisk)


const app = createApp(App)

app.component('font-awesome-icon', FontAwesomeIcon)
app.use(router)
app.use(VueAxios, axios)

app.mount('#app')
