from flask_restx import Api, Resource, fields
from flask import Blueprint
from app.services.tax_service import TaxCalculator
from app.models.tax_model import TaxInput, MaritalStatus

blueprint = Blueprint('api', __name__)
api = Api(blueprint,
    title='Tax Calculator API',
    version='1.0',
    description='API for calculating Thai tax deductions')

ns = api.namespace('tax', description='Tax calculations')

tax_input = api.model('TaxInput', {
    'monthly_income': fields.Float(required=True, description='Monthly income in baht'),
    'bonus': fields.Float(required=True, description='Annual bonus'),
    'other_income': fields.Float(required=True, description='Other income'),
    'marital_status': fields.String(required=True, enum=['single', 'divorced', 'spouse_with_income', 'spouse_without_income']),
    'num_children': fields.Integer(required=True, description='Number of children'),
    'num_parents': fields.Integer(required=True, description='Number of supported parents'),
    'num_disabled_dependents': fields.Integer(required=True),
    'social_security': fields.Float(required=True),
    'life_insurance': fields.Float(required=True),
    'health_insurance': fields.Float(required=True),
    'parent_health_insurance': fields.Float(required=True),
    'social_enterprise': fields.Float(required=True),
    'thai_esg': fields.Float(required=True),
    'rmf': fields.Float(required=True),
    'ssf': fields.Float(required=True),
    'pvd': fields.Float(required=True),
    'gpf': fields.Float(required=True),
    'nsf': fields.Float(required=True),
    'pension_insurance': fields.Float(required=True),
    'general_donation': fields.Float(required=True),
    'education_donation': fields.Float(required=True),
    'political_donation': fields.Float(required=True),
    'easy_receipt': fields.Float(required=True),
    'secondary_tourism': fields.Float(required=True),
    'mortgage_interest': fields.Float(required=True),
    'new_house_cost': fields.Float(required=True),
    'pregnancy_expense': fields.Float(required=True)
})

@ns.route('/calculate')
class TaxResource(Resource):
    @ns.expect(tax_input)
    @ns.doc('calculate_tax')
    def post(self):
        """Calculate tax deductions"""
        try:
            data = api.payload
            tax_input = TaxInput(**data)
            calculator = TaxCalculator(tax_input)
            
            return {
                'total_income': calculator.calculate_total_income(),
                'total_deductions': calculator.calculate_total_deductions(),
                'taxable_income': calculator.calculate_taxable_income(),
                'tax_amount': calculator.calculate_tax(),
                'deductions_breakdown': {
                    'expense': calculator.calculate_expense_deduction(),
                    'personal': calculator.calculate_personal_deduction(),
                    'dependent': calculator.calculate_dependent_deduction(),
                    'insurance': calculator.calculate_insurance_deduction(),
                    'investment': calculator.calculate_investment_deduction(),
                    'donation': calculator.calculate_donation_deduction(),
                    'special': calculator.calculate_special_deductions()
                }
            }
        except Exception as e:
            api.abort(500, str(e))