import {z} from "zod";

export const AdStrategySchema = z.object({
    rating_medium_min_score: z.number(),
    rating_high_min_score: z.number(),
    ads_allowance_unknown_rating: z.number(),
    ads_allowance_low_rating: z.number(),
    ads_allowance_medium_rating: z.number(),
    ads_allowance_high_rating: z.number(),
    ads_allowance_window_days: z.number(),
}).required()

export type AdStrategy = z.TypeOf<typeof AdStrategySchema>;
