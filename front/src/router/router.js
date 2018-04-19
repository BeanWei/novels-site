import Passport from '@/components/passport/Passport'
import Login from '@/components/passport/Login'
import Signin from '@/components/passport/Signin'

export const pageRouter = [
  {
    path: '/passport',
    name: 'Passport',
    component: Passport
    // children: [
    //   {path: 'login', name: 'login', component: Login},
    //   {path: 'signin', name: 'signin', component: Signin}
    // ]
  }
]

export const routers = [
  ...pageRouter,
]