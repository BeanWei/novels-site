<template>
    <div class="article-bd">
        <div class="atc-item"  v-for="news of list">
            <p class="title">{{ news.title }}</p>
            <p class="date">{{ news.create_at }}</p>
            <p class="author">By: {{ news.author.loginname }}</p>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      formData: {
        limit: 10,
        tab: 'ask'
      },
      list: []
    }
  },
  created () {
    this.getData()
  },
  props: {
    page: {
      type: Number,
      default: 1
    }
  },
  watch: {
    page () {
      this.getData()
    }
  },
  methods: {
    getData () {
      this.formData.page = this.page
      axios.get('https://cnodejs.org/api/v1/topics', {params: this.formData})
      .then(res => {
        res.data.data.forEach((item) => {
          let d = new Date(item.create_at)
          item.create_at = `${d.getFullYear()}-${d.getMonth() + 1}-${d.getDate()}`
        })
        this.list = res.data.data
      })
      .catch(err => {
        console.log(err)
      })
    }
  }
}
</script>

<style scoped>

.article-bd {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
}

.atc-item {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
    border: 1px solid #1F2D3D;
    margin-bottom: 8px;
}

.atc-item p {
    width: 95%;
    margin: 5px;
    line-height: 20px;
    text-align: left;
}

.title {
  color: #1F2D3D;
}

.date,
.author {
  color: #8492A6;
}

</style>
