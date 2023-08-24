from typing import Optional

import email_normalize


async def normalize_email(email: Optional[str]) -> Optional[str]:
    if email is None:
        return None
    result = await email_normalize.Normalizer().normalize(email.strip())
    if not result.mx_records:
        # see https://email-normalize.readthedocs.io/en/stable/result.html
        raise EmailNormalizationError(f'Failed to fetch MX records for email address: `{email}`')
    return result.normalized_address


class EmailNormalizationError(Exception):
    def __init__(self, message):
        super().__init__(message)
