import Vue from "vue"
import VueRouter from "vue-router"
import ChatRoom from "../components/ChatRoom"
import MainPage from "../components/MainPage"

Vue.use(VueRouter)

const routes = [
  {
    path: "/",
    name: "MainPage",
    component: MainPage
  },
  {
    path: "/chatroom/:roomname",
    name: "ChatRoom",
    component: ChatRoom
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
