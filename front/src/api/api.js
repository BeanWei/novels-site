import fetch from '@/utils/fetch'

//登录
export function login () {
  return fetch ({
    methods: 'post',
    url: `/login`
  })
}

//注册
export function signin () {
  return fetch ({
    methods: 'post',
    url: `/signin`
  })
}