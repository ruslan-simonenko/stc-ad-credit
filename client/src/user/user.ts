import {CarbonAuditor} from "../app/carbon-auditor/carbon-auditor-store.ts";

export type UserRole = 'Admin' | 'Carbon Auditor'

export interface User {
    name: string,
    email: string,
    picture_url: string,
    roles: Array<UserRole>
}

export interface Users {
    items: User[],
    fetching: boolean,
    error: boolean,
}
