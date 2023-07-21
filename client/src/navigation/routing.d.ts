import 'vue-router'

export {}

declare module 'vue-router' {
    export interface RouteMeta {
        requiresAuth?: boolean
    }
}