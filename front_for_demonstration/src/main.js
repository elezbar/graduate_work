import Vue from 'vue'
import App from './App.vue'
import router from "./router"
import vuetify from './plugins/vuetify'
import VueSwal from "vue-swal"
import VueCookies from 'vue-cookies'

Vue.config.productionTip = false

Vue.use(VueSwal);
Vue.use(VueCookies, { expires: '365d'});

new Vue({
  vuetify,
  router,
  render: h => h(App)
}).$mount('#app')
