import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    showLogin: false,
    tab: 'SEARCH',
    starCount: 0,
    updateStar: true,
    searchJobs: {
      data: [],
      pageCount: 0
    },
    starJobs: {
      data: [],
      pageCount: 0
    },
    captchaMsg: '发送验证码',
    chart: {
      count: [],
      salary: []
    }
  },
  mutations: {
    SHOW_LOGIN (state) {
      state.showLogin = !state.showLogin
    },
    TOGGLE_TAB (state, tab) {
      state.tab = tab
    },
    ADD_STAR (state) {
      state.starCount++
    },
    CLEAR_STAR (state) {
      state.starCount = 0
    },
    UPDATE_STAR (state) {
      state.updateStar = !state.updateStar
    },
    UPDATE_SEARCH_JOBS (state, data) {
      state.searchJobs = data
    },
    UPDATE_STAR_JOBS (state, data) {
      state.starJobs = data
    },
    UPDATE_CAPTCHA_MSG (state, data) {
      state.captchaMsg = data
    },
    UPDATE_CHART (state, data) {
      if (data.chartType === 'COUNT') {
        state.chart.count = data.data
      } else if (data.chartType === 'SALARY') {
        state.chart.salary = data.data
      }
    }
  },
  actions: {
    showLogin ({ commit }) {
      commit('SHOW_LOGIN')
    },
    toggleTab ({ commit }, tab) {
      commit('TOGGLE_TAB', tab)
    },
    showStar ({ commit }, msg) {
      if (msg === 'add') {
        commit('ADD_STAR')
      } else if (msg === 'clear') {
        commit('CLEAR_STAR')
      }
    },
    updateStar ({ commit }) {
      commit('UPDATE_STAR')
    },
    updateSearchJobs ({ commit }, data) {
      commit('UPDATE_SEARCH_JOBS', data)
    },
    updateStarJobs ({ commit }, data) {
      commit('UPDATE_STAR_JOBS', data)
    },
    updateCaptchaMsg ({ commit }, data) {
      commit('UPDATE_CAPTCHA_MSG', data)
    },
    updateChart ({ commit }, data) {
      commit('UPDATE_CHART', data)
    }
  },
  getters: {
    showState: function (state) {
      return state.showLogin
    },
    getTab: function (state) {
      return state.tab
    },
    getStar: function (state) {
      return state.starCount
    },
    getUpdateStar: function (state) {
      return state.updateStar
    },
    getSearchJobs: function (state) {
      return state.searchJobs
    },
    getStarJobs: function (state) {
      return state.starJobs
    },
    getCaptchaMsg: function (state) {
      return state.captchaMsg
    },
    getChart: function (state) {
      return state.chart
    }
  }
})
