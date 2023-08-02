export interface Business {
    name: string,
    facebookLink: string,
}


export interface BusinessAddFormDTO {
    name: string,
    facebookLink: string,
}

export interface Businesses {
    items: Business[],
}
