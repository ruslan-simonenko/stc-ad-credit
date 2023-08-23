export enum UserRole {
    ADMIN = 'Admin',
    AD_MANAGER = 'Ad Manager',
    BUSINESS_MANAGER = 'Business Manager',
    CARBON_AUDITOR = 'Carbon Auditor'
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

export interface UserUpdateFormDTO {
    email: string,
    roles: Array<UserRole>,
}

export interface Users {
    items: User[],
    fetching: boolean,
    error: boolean,
}
