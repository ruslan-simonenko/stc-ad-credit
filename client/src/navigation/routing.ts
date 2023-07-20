import {createRouter, createWebHashHistory, RouteRecordRaw} from "vue-router";
import LoginPage from "../auth/LoginPage.vue";
import AdminPage from "../app/admin/AdminPage.vue";

const routes: RouteRecordRaw[] = [
    {name: 'Admin', path: '/admin', component: AdminPage},
    {name: "Login", path: '/login', component: LoginPage},
    {name: 'Home', path: '/', redirect: {name: 'Login'}},
]

export const appRouter = createRouter({
    history: createWebHashHistory(),
    routes
})

