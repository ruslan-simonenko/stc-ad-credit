from flask import Blueprint, render_template_string

from src.business.business_service import BusinessService
from src.carbon_audit.rating.carbon_audit_rating_service import CarbonAuditRatingService

business_profile_bp = Blueprint('business_profile_bp', __name__, url_prefix='/')


@business_profile_bp.route('/<business_id>/profile', methods=['get'])
def get_business_profile(business_id: int):
    rating = CarbonAuditRatingService.get_for_business(business_id)
    business = BusinessService.get_by_id_or_throw(business_id)

    iframe_content = """
    <!DOCTYPE html>
    <html lang="en-GB">
    <head>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 0; 
                padding: 0; 
                background-color: #f9f9f9; 
                text-align: center; 
            }
            .footer-info { 
                border-top: 1px solid #ccc; 
                padding: 10px; 
            }
        </style>
    </head>
    <body>
        <div class="footer-info">
            Business: {{ business_name }}
            <br/>
            Carbon Footprint Rating: {{ carbon_footprint_rating }}
        </div>
    </body>
    </html>
    """

    return render_template_string(iframe_content,
                                  business_name=business.name,
                                  carbon_footprint_rating=rating.value)
