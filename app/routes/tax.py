from flask import Blueprint, request, jsonify
from app.services.tax_service import TaxCalculator
from app.models.tax_model import TaxInput, MaritalStatus

bp = Blueprint('tax', __name__, url_prefix='/api/tax')

@bp.route('/calculate', methods=['POST'])
def calculate_tax():
    try:
        data = request.get_json()
        print("Received data:", data)  # Debug print
        
        tax_input = TaxInput(**data)  # Simplified constructor
        
        calculator = TaxCalculator(tax_input)
        
        result = {
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
        
        return jsonify(result), 200
        
    except Exception as e:
        print("Error:", str(e))  # Debug print
        return jsonify({'error': str(e)}), 500