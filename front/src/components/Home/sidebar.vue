<template>
    <div class="sidebar">
        <div>
        <el-menu default-active="1" theme="dark">
            <el-submenu index="1">
              <template slot="title">职位功能</template>
              <el-menu-item index="1-1" @click="toggleTab('SEARCH')">职位查询</el-menu-item>
              <el-menu-item index="1-2" @click="toggleTab('STAR')">我的关注 <span class="badge" v-if="starCount > 0">{{ starCount }}</span></el-menu-item>
              <el-menu-item index="1-3" @click="toggleTab('CHART')">报表分析</el-menu-item>
            </el-submenu>
          </el-menu>
        </div>
    </div>
</template>

<script>
export default {
  data () {
    return {
    }
  },
  computed: {
    starCount () {
      return this.$store.getters.getStar
    }
  },
  methods: {
    // ...mapActions({
    //   toggleTab: 'toggleTab'
    // }),
    toggleTab (tab) {
      this.$store.dispatch('toggleTab', tab)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.sidebar {
  width: 140px;
  height: 100%;
  background-color: #333744;
}
.badge {
  background-color: #FF0000;
}
</style>