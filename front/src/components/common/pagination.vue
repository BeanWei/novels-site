<template>
  <div class="pageButtons" v-if="show">
    <nav aria-label="Page navigation">
      <ul class="pagination">
        <li :class="{disabled: isMin}">
          <a aria-label="Previous">
            <span aria-hidden="true">&laquo;</span>
          </a>
        </li>
        <li v-for="(item, index) of pageList" :class="{active: item.active}" v-if="item.value >= page.min && item.value <= page.max">
          <a @click="onSubmit(index)">{{ item.value }}</a>
        </li>
        <li :class="{disabled: isMax}">
          <a aria-label="Next">
            <span aria-hidden="true">&raquo;</span>
          </a>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>

export default {
  data () {
    return {
      page: {
        selected: 0,  // 选中下标为selected的页数
        count: 0,     // 总页数
        size: 10,      // 最大显示页数
        min: 1,
        max: 1
      },
      pageList: [
        { active: false, value: 1 }
      ],
      isMin: false,
      isMax: false,
      show: false,
      isInit: false
    }
  },
  props: {
    pageCount: {
      type: Number,
      default: 0
    }
  },
  watch: {
    pageCount () {
      this.init(-1)
      this.show = true
      this.onSubmit(0)
    }
  },
  methods: {
    init (index) {
      this.page.count = this.pageCount
      this.page.size = (this.page.count > 10) ? 10 : this.page.count

      if (index === -1) {
        index = 0
        this.page.min = 1
        this.page.max = this.page.size
        this.isInit = false
        this.page.selected = index
      } else {
        this.isInit = true
      }

      if (index >= 6 && (this.page.count - this.pageList[9].value) > 0) {
        pageNumber = this.pageList[1].value
        index--
        this.page.min++
        this.page.max++
      } else if (this.isInit && index < 6 && this.pageList[0].value !== 1) {
        pageNumber = this.pageList[0].value - 1
        index++
        this.page.min--
        this.page.max--
      }
      let pageNumber = this.page.min
      this.pageList = []
      for (let i = 0; i < this.page.size; i++) {
        let item = {
          active: false,
          value: pageNumber
        }
        pageNumber++
        this.pageList.push(item)
      }
      // 改变当前选中页号下标样式
      this.pageList[this.page.selected].active = false
      this.pageList[index].active = true
      this.page.selected = index
    },
    onSubmit (index) {
      this.$emit('pageChanged', this.pageList[index].value)
      this.init(index)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang='less'>

.pageButtons {

  a:hover {
    cursor: pointer;
  }
}

</style>
