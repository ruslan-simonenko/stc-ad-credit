import {createRouter, createWebHashHistory, RouteRecordRaw} from "vue-router";
import LoginPage from "../auth/LoginPage.vue";

const routes: RouteRecordRaw[] = [
    {name: "Login", path: '/login', component: LoginPage},
    {name: 'Home', path: '/', redirect: {name: 'Login'}},
]

export const appRouter = createRouter({
    history: createWebHashHistory(),
    routes
})

