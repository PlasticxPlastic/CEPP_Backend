from dataclasses import dataclass
from enum import Enum

class MaritalStatus(Enum):
   SINGLE = "single"
   DIVORCED = "divorced"
   SPOUSE_WITH_INCOME = "spouse_with_income"
   SPOUSE_WITHOUT_INCOME = "spouse_without_income"

@dataclass
class TaxInput:
   # Income
   monthly_income: float
   bonus: float
   other_income: float
   
   # Basic deductions
   marital_status: MaritalStatus
   num_children: int
   num_parents: int
   num_disabled_dependents: int
   
   # Insurance
   social_security: float
   life_insurance: float
   health_insurance: float
   parent_health_insurance: float
   
   # Investment
   social_enterprise: float
   thai_esg: float
   rmf: float
   ssf: float
   pvd: float
   gpf: float
   nsf: float
   pension_insurance: float
   
   # Donations
   general_donation: float
   education_donation: float
   political_donation: float
   
   # Special 2024
   easy_receipt: float
   secondary_tourism: float
   
   # Housing
   mortgage_interest: float
   new_house_cost: float
   
   # Additional
   pregnancy_expense: float