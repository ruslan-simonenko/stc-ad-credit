import {z} from "zod";


export enum BusinessRegistrationType {
    CRN = "CRN", VAT = "VAT", NI = "NI"
}

export const BusinessDTOSchema = z.object({
    id: z.number(),
    name: z.string(),
    registration_type: z.nativeEnum(BusinessRegistrationType),
    registration_number: z.string(),
    email: z.string().nullable(),
    facebook_url: z.string().nullable(),
})

export const BusinessDTOPublicSchema = BusinessDTOSchema.omit({
    registration_type: true,
    registration_number: true,
    email: true
})

export type BusinessDTO = z.TypeOf<typeof BusinessDTOSchema>
export type BusinessDTOPublic = z.TypeOf<typeof BusinessDTOPublicSchema>


export type Business = {
    id: number,
    name: string,
    facebook_url: string | null,
    sensitive?: {
        registration_type: BusinessRegistrationType,
        registration_number: string,
        email: string | null,
    }
}

export const BusinessFormDTOSchema = z.object({
    name: z.string(),
    registration_type: z.nativeEnum(BusinessRegistrationType),
    registration_number: z.string(),
    email: z.string().nullable(),
    facebook_url: z.string().nullable(),
})

export type BusinessFormDTO = z.TypeOf<typeof BusinessFormDTOSchema>

export interface Businesses {
    items: Business[],
    fetching: boolean,
    error: boolean,
}

