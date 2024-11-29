from app.models.tax_model import TaxInput, MaritalStatus

class TaxCalculator:
   def __init__(self, tax_input: TaxInput):
       self.input = tax_input
       self._validate_inputs()
       
   def _validate_inputs(self):
       if any(getattr(self.input, field) < 0 for field in [
           'monthly_income', 'bonus', 'other_income', 'social_security',
           'life_insurance', 'health_insurance', 'parent_health_insurance',
           'social_enterprise', 'thai_esg', 'rmf', 'ssf', 'pvd', 'gpf', 
           'nsf', 'pension_insurance', 'general_donation', 
           'education_donation', 'political_donation', 'easy_receipt',
           'secondary_tourism', 'mortgage_interest', 'new_house_cost',
           'pregnancy_expense'
       ]):
           raise ValueError("Monetary values cannot be negative")

   def calculate_total_income(self):
       return round((self.input.monthly_income * 12) + self.input.bonus + self.input.other_income, 2)
       
   def calculate_expense_deduction(self):
       total_income = self.calculate_total_income()
       return round(min(total_income * 0.5, 100000), 2)
       
   def calculate_personal_deduction(self):
       deduction = 60000
       if self.input.marital_status == MaritalStatus.SPOUSE_WITHOUT_INCOME:
           deduction += 60000
       return deduction
       
   def calculate_dependent_deduction(self):
       children_deduction = self.input.num_children * 30000
       parent_deduction = min(self.input.num_parents * 30000, 120000)
       disabled_deduction = self.input.num_disabled_dependents * 60000
       return children_deduction + parent_deduction + disabled_deduction
       
   def calculate_insurance_deduction(self):
       social_security = min(self.input.social_security, 9000)
       life_health_combined = min(
           self.input.life_insurance + self.input.health_insurance,
           100000
       )
       parent_health = min(self.input.parent_health_insurance, 15000)
       return social_security + life_health_combined + parent_health
       
   def calculate_investment_deduction(self):
       total_income = self.calculate_total_income()
       
       social_enterprise = min(self.input.social_enterprise, 100000)
       thai_esg = min(self.input.thai_esg, total_income * 0.3, 300000)
       
       retirement_total = min(sum([
           min(self.input.rmf, total_income * 0.3),
           min(self.input.ssf, total_income * 0.3),
           min(self.input.pvd, total_income * 0.15),
           self.input.gpf,
           self.input.nsf,
           min(self.input.pension_insurance, total_income * 0.15)
       ]), 500000)
       
       return round(social_enterprise + thai_esg + retirement_total, 2)
       
   def calculate_donation_deduction(self):
    # Remove circular dependency
    base_deductions = sum([
        self.calculate_expense_deduction(),
        self.calculate_personal_deduction(),
        self.calculate_dependent_deduction(),
        self.calculate_insurance_deduction(),
        self.calculate_investment_deduction(),
        self.calculate_special_deductions()
    ])
    income_after_deductions = self.calculate_total_income() - base_deductions
    max_donation = income_after_deductions * 0.1
    
    general = min(self.input.general_donation, max_donation)
    education = min(self.input.education_donation * 2, max_donation)
    political = min(self.input.political_donation, 10000)
    
    return round(general + education + political, 2)
       
   def calculate_special_deductions(self):
       easy_receipt = min(self.input.easy_receipt, 50000)
       tourism = min(self.input.secondary_tourism, 15000)
       mortgage = min(self.input.mortgage_interest, 100000)
       house_deduction = min((self.input.new_house_cost // 1000000) * 10000, 100000)
       pregnancy = min(self.input.pregnancy_expense, 60000)
       
       return easy_receipt + tourism + mortgage + house_deduction + pregnancy
       
   def calculate_total_deductions(self):
       return sum([
           self.calculate_expense_deduction(),
           self.calculate_personal_deduction(),
           self.calculate_dependent_deduction(),
           self.calculate_insurance_deduction(),
           self.calculate_investment_deduction(),
           self.calculate_donation_deduction(),
           self.calculate_special_deductions()
       ])
       
   def calculate_taxable_income(self):
       return max(self.calculate_total_income() - self.calculate_total_deductions(), 0)

   def calculate_tax(self):
       taxable_income = self.calculate_taxable_income()
       tax_brackets = [
           (0, 150000, 0),
           (150001, 300000, 0.05),
           (300001, 500000, 0.10),
           (500001, 750000, 0.15),
           (750001, 1000000, 0.20),
           (1000001, 2000000, 0.25),
           (2000001, 5000000, 0.30),
           (5000001, float('inf'), 0.35)
       ]
       
       total_tax = 0
       remaining_income = taxable_income
       
       for min_income, max_income, rate in tax_brackets:
           if remaining_income <= 0:
               break
           bracket_income = min(remaining_income, max_income - min_income + 1)
           total_tax += bracket_income * rate
           remaining_income -= bracket_income
       
       return round(total_tax, 2)