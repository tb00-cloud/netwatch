import Vue from 'vue'
import App from './App.vue'
import VueSession from "vue-session";
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import VueCookies from 'vue-cookies';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faPlus, faCheck, faXmark, faTrashCan, faChartLine, faPen, faMagnifyingGlass, faToggleOff, faToggleOn, faRightFromBracket, faCircleQuestion, faArrowsRotate} from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import Toasted from 'vue-toasted';
import VTooltip from 'v-tooltip';

export const eventBus = new Vue();

library.add(faPlus, faCheck, faXmark, faTrashCan, faChartLine, faPen, faMagnifyingGlass,faToggleOff, faToggleOn, faRightFromBracket, faCircleQuestion, faArrowsRotate)
Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.config.productionTip = false
Vue.use(VueSession);
Vue.use(VueAxios, axios)
Vue.use(VueCookies);
Vue.use(Toasted);
Vue.use(VTooltip);


new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
