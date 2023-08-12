import {z} from "zod";

export const AdRecordSchema = z.object({
    id: z.number(),
    business_id: z.number(),
    ad_post_url: z.string(),
    creator_id: z.number(),
    created_at: z.coerce.date()
}).required()

export type AdRecord = z.TypeOf<typeof AdRecordSchema>;

export interface AdRecords {
    items: AdRecord[],
    fetching: boolean,
}

export interface AdRecordAddFormDTO {
    business_id: number,
    ad_post_url: string,
}