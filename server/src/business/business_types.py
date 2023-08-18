from enum import Enum


class BusinessRegistrationType(str, Enum):
    CRN = "CRN"
    VAT = "VAT"
    NI = "NI"
