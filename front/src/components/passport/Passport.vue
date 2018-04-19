<template>
  <div id="Passport">
    <login v-if="login"></login>
    <signin v-if="!login"></signin>
    <br><br>
    <h3>{{msgone}}<a @click="passport">{{msgtwo}}</a></h3>
  </div>
</template>

<script>
import login from './Login.vue'
import signin from './Signin.vue'
export default {
  components: {
    login,
    signin
  },
  data() {
    return {
      login: true,
      msgone: '没有账号',
      msgtwo: '注册'
    }
  },
  methods: {
    passport () {
      this.login = ! this.login
      if (this.msgone === '已有账号' & this.msgtwo === '登录') {
        this.msgone = '没有账号'
        this.msgtwo = '注册'
      } else {
        this.msgone = '已有账号'
        this.msgtwo = '登录'
      }
    }
  }

}
</script>
