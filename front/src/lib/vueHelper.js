import api from '../api/index'
import store from '../vuex/store'
import router from '../router'
/*eslint-disable*/
// 显示提示框
export const showMsg = (that, close, msg, type) => {
  that.$message({
    showClose: close,
    message: msg,
    type: type
  })
}

// 获取查询结果 ALL查询结果 STAR关注结果
export const searchJobs = (type, data) => {
  let apiItem, action
  let result = {
    data: [],
    pageCount: 1
  }
  if (type === 'ALL') {
    apiItem = api.searchJobs
    action = 'updateSearchJobs'
  } else if (type === 'STAR') {
    apiItem = api.getStarJob
    action = 'updateStarJobs'
  }
  apiItem(data)
  .then(res => {
    if (res.data.pageCount > 0) {
      result = {
        data: res.data.results,
        pageCount: res.data.pageCount
      }
      store.dispatch(action, result)
    } else {
      store.dispatch(action, result)
    }
  })
  .catch(err => {
    console.log(err)
  })
}

// doLogin
export const doLogin = (that, data) => {
  api.login(data)
  .then(res => {
    if (res.data.code === 0) {
      sessionStorage.setItem('accessToken', res.data.access_token)
      sessionStorage.setItem('username', res.data.data.username)
      sessionStorage.setItem('uid', res.data.data._id)
      store.dispatch('showLogin')
      showMsg(that, true, '登录成功', 'success')
      router.push({path: '/p/index', params: { username: res.data.username }})
    } else {
      showMsg(that, true, '登录失败，账号或密码错误', 'error')
    }
  })
  .catch(err => {
    console.log(err)
  })
}

// doRegister
export const doRegister = (that, data) => {
  api.register(data)
  .then(res => {
    if (res.data.code === 0) {
      showMsg(that, true, '注册成功', 'success')
      router.push({name: 'Login'})
    } else if (res.data.code === 88) {
      showMsg(that, true, '验证码错误', 'error')
    } else if (res.data.code === 99) {
      showMsg(that, true, '用户名已被注册', 'error')
    }
  })
  .catch(err => {
    console.log(err)
  })
}

// sendCaptcha
export const sendCaptcha = (that, data) => {
  api.getCaptcha(data)
  .then(res => {
    let code = res.data.code
    if (code === 0) {
      store.dispatch('updateCaptchaMsg', '发送成功')
    } else if (code === 88) {
      store.dispatch('updateCaptchaMsg', '已经发送')
    } else if (code === 99) {
      showMsg(that, true, '验证码发送失败', 'error')
    }
  })
  .catch(err => {
    console.log(err)
  })
}

// doStarJob
export const doStarJob = (that, data) => {
  api.addStarJob(data)
  .then(res => {
    if (res.data.code === 0) {
      showMsg(that, false, '关注成功', 'success')
      store.dispatch('showStar', 'add')
    } else if (res.data.code === 99) {
      showMsg(that, false, '已添加关注', 'error')
    }
  })
  .catch(err => {
    console.log(err)
  })
}

// doFollowComp
export const doFollowComp = (that, data) => {
  api.addFollowComp(data)
  .then(res => {
    if (res.data.code === 0) {
      showMsg(that, false, '跟踪成功', 'success')
      // store.dispatch('showStar', 'add')
    } else if (res.data.code === 99) {
      showMsg(that, false, '已添加跟踪', 'error')
    }
  })
  .catch(err => {
    console.log(err)
  })
}

// doCancleStar
export const doCancleStar = (that, data) => {
  api.cancleStar(data)
  .then(res => {
    if (res.data.code === 0) {
      showMsg(that, false, '取消成功', 'success')
      store.dispatch('updateStar')
    } else if (res.data.code === 99) {
      showMsg(that, false, '取消失败', 'error')
    }
  })
  .catch(err => {
    console.log(err)
  })
}

// getChartData
export const getChartData = (data) => {
  api.getChartData(data)
  .then(res => {
    if (res.data.code === 0) {
      let result = {
        chartType: res.data.chartType,
        data: res.data.chart
      }
      store.dispatch('updateChart', result)
    } else if (res.data.code === 99) {
      console.log('err')
    }
  })
  .catch(err => {
    console.log(err)
  })
}
