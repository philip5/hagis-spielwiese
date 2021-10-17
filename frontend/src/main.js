import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Vuetify from './plugins/vuetify'
import Keycloak from "keycloak-js";

Vue.use(Vuetify);
Vue.config.productionTip = false;

new Vue({
    router,
    Keycloak,
    store,
    vuetify: Vuetify,
    render: h => h(App)
}).$mount('#app');
