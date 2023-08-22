/// <reference types="vue-router" />

import {UserRole} from "../user/user.ts";

declare module 'vue-router' {
    export interface RouteMeta {
        auth?: {
            required: boolean,
            authorizedRoles?: Array<UserRole>,
        },
        navigationMenu?: {
            type: 'entry'
            entry: { icon: string, label: string }
        } | {
            type: 'linked'
            routeName: string
        },
    }
}

export {}
