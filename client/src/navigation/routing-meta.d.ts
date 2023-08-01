/// <reference types="vue-router" />

import {UserRole} from "../user/user.ts";

declare module 'vue-router' {
    export interface RouteMeta {
        auth?: {
            allowedRoles: Array<UserRole>,
            navIcon: string,
            navLabel: string,
        }
    }
}

export {}
