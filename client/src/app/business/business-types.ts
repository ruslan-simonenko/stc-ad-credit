import {z} from "zod";


export enum BusinessRegistrationType {
    CRN = "CRN", VAT = "VAT", NI = "NI"
}


export const BusinessSchema = z.object({
    id: z.number(),
    name: z.string(),
    registration_type: z.nativeEnum(BusinessRegistrationType),
    registration_number: z.string(),
    email: z.string().nullable(),
    facebook_url: z.string().nullable(),
}).partial({
    registration_type: true,
    registration_number: true,
    email: true,
})

export type Business = z.TypeOf<typeof BusinessSchema>

export const BusinessAddFormDTOSchema = z.object({
    name: z.string(),
    registration_type: z.nativeEnum(BusinessRegistrationType),
    registration_number: z.string(),
    email: z.string(),
    facebook_url: z.string(),
})

export type BusinessAddFormDTO = z.TypeOf<typeof BusinessAddFormDTOSchema>

export interface Businesses {
    items: Business[],
    fetching: boolean,
    error: boolean,
}

