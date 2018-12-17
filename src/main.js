// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import 'bootstrap/dist/css/bootstrap.css';
import BootstrapVue from 'bootstrap-vue';
import Vue from 'vue';
import infiniteScroll from 'vue-infinite-scroll';
import App from './App';
import router from './router';

Vue.config.productionTip = false;

Vue.use(BootstrapVue);
Vue.use(infiniteScroll);

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
});
