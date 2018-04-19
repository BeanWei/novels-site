import Vue from 'vue'
import Router from 'vue-router'
import Axios from 'axios'
import Login from '@/components/Login/login'
import Register from '@/components/Login/register'
import Index from '@/components/Home/index'

Vue.use(Router)

export default new Router({
  /* eslint-disable */
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/index',
      name: 'index',
      component: Index
    },
    {
      path: '/novels',
      component: require('../components/Home/index.vue'),
      beforeEnter: (to, from, next) => {
        let pattern = /^(\/p)/g
        let token = sessionStorage.getItem('accessToken')
        if (pattern.test(to.path)) {
          Axios.post('http://localhost:5000/api/v1.0/isLogin', {access_token: token})
          .then(res => {
            if (res.data.code === 0) {
              next()
            } else {
              next({name: 'Login'})
            }
          })
          .catch(err => {
            console.log(err)
          })
        }
      }
    },
    {
      path: '*',
      component: require('../components/NotFound.vue')
    }
  ]
})
