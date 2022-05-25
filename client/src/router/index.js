import Vue from 'vue'
import VueRouter from 'vue-router'
import UserLogin from "@/components/UserLogin.vue"
import DashBoard from "@/components/DashBoard.vue"
import ManageUsers from "@/components/ManageUsers.vue"
import DisplayTarget from "@/components/DisplayTarget.vue"



Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: DashBoard
  },
  {
    path: '/login',
    name: 'login',
    component: UserLogin
  },
  {
    path: '/users',
    name: 'users',
    component: ManageUsers
  },
  {
    path: '/target/:id',
    name: 'target',
    component: DisplayTarget
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router

