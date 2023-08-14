from pydantic import BaseModel


class AdStrategyDTO(BaseModel):
    rating_medium_min_score: int
    rating_high_min_score: int
    ads_allowance_unknown_rating: int
    ads_allowance_low_rating: int
    ads_allowance_medium_rating: int
    ads_allowance_high_rating: int
    ads_allowance_window_days: int
