<template>
  <div class="wrapper">
    <Topbar></Topbar>
    <div class="bd">
      <Sidebar></Sidebar>
      <div class="right-bd">
        <div class="main">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Topbar from './topbar'
import Sidebar from './sidebar'

export default {
  components: { Topbar, Sidebar },
  data () {
    return {
    }
  },
  computed: {
    tab () {
      return this.$store.getters.getTab
    }
  },
  methods: {
  }
}
</script>

<style scoped>
.wrapper {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}
.bd {
  display: flex;
  flex-direction: row;
  justify-content: center;
  /*padding-bottom: 100%;*/
  height: 100%;
}
.right-bd {
  flex-basis: 100px;
  flex-grow: 2;
}
.main {
  height: 100%;
}
</style>