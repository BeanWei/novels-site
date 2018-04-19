<template>
  <div class="wrapper">
    <list :page="page"></list>
    <el-button type="primary" @click="loadMore">更多</el-button>
  </div>
</template>

<script>
import List from './list'

export default {
  name: 'loadDemo',
  components: {
    List
  },
  data () {
    return {
      page: 1
    }
  },
  methods: {
    loadMore () {
      this.page++
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.wrapper {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 95%;
}

.el-button {
  width: 100%;
}

</style>
