/// <reference types="vue-router" />

import {UserRole} from "../user/user.ts";

declare module 'vue-router' {
    export interface RouteMeta {
        auth?: {
            required: boolean,
            authorizedRoles?: Array<UserRole>,
        },
        navigationMenu?: {
            icon: string,
            label: string,
        },
    }
}

export {}
