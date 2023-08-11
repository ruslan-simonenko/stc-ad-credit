export enum UserRole {
    ADMIN = 'Admin',
    CARBON_AUDITOR = 'Carbon Auditor',
    AD_MANAGER = 'Ad Manager'
}

export interface User {
    id: number,
    name: string,
    email: string,
    picture_url: string,
    roles: Array<UserRole>
}


export interface UserAddFormDTO {
    email: string,
    roles: Array<UserRole>,
}

export interface Users {
    items: User[],
    fetching: boolean,
    error: boolean,
}
