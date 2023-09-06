import {z} from "zod";

export const AdAllowanceSchema = z.object({
    business_id: z.number(),
    window_start: z.coerce.date(),
    window_end: z.coerce.date(),
    allowance: z.number(),
    used_allowance: z.number(),
}).required()

export type AdAllowance = z.TypeOf<typeof AdAllowanceSchema>;

export interface AdAllowances {
    indexed: { [business_id: number]: AdAllowance },
    fetching: boolean,
}