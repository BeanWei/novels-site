<template>
    <div class="topbar">
        <div class="title">书匣子</div>
        <div class="topbar-info-dropdown">
          <div class="info" @click="showDropdown">{{ username }}</div>
          <div class="menu" v-show="dropdownMenu">
            <div @click="logout"><i class="fa fa-sign-out">&nbsp;</i>退出登录</div>
          </div>
        </div>
    </div>
</template>

<script>
import router from '../../router'
export default {
  data () {
    return {
      username: sessionStorage.getItem('username'),
      dropdownMenu: false
    }
  },
  methods: {
    showLogin () {
      this.$store.dispatch('showLogin')
    },
    showDropdown () {
      this.dropdownMenu = !this.dropdownMenu
    },
    logout () {
      sessionStorage.removeItem('accessToken')
      sessionStorage.removeItem('username')
      router.push({path: '/'})
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.topbar {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  height: 50px;
  line-height: 50px;
  color: #fff;
  background-color: #333744;
  font-size: 14px;
}
.title {
    margin: 0 20px 0 45px;
    cursor: pointer;
  }
.topbar-info-dropdown .info {
  width: 100px;
  margin: 0 20px 0 20px;
  cursor: pointer;
}
.menu {
  position: absolute;
  right: 0;
  width: 120px;
  height: 50px;
  color: #333744;
  font-size: 14px;
  background-color: #fff;
  transition: all 1s;
  z-index: 99;
  border: 1px solid #ddd;
}
div:hover {
  background-color: #f5f5f5;
  cursor: pointer;
}
</style>