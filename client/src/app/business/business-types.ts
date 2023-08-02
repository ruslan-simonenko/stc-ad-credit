export interface Business {
    id: number,
    name: string,
    facebook_url: string,
}


export interface BusinessAddFormDTO {
    name: string,
    facebook_url: string,
}

export interface Businesses {
    items: Business[],
    fetching: boolean,
    error: boolean,
}
