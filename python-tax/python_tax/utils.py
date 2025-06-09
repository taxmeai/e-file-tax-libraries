"""
Utility functions for tax calculations
"""

from decimal import Decimal, ROUND_HALF_UP

def format_currency(amount):
    """Format amount as currency"""
    return f"${Decimal(str(amount)):,.2f}"

def calculate_agi(income_data):
    """Calculate Adjusted Gross Income"""
    return Decimal('0')

def calculate_taxable_income(agi, deductions):
    """Calculate taxable income"""
    return max(Decimal('0'), agi - deductions)

def apply_tax_brackets(taxable_income, brackets):
    """Apply tax brackets to income"""
    return Decimal('0')

def calculate_credits(taxpayer_data):
    """Calculate tax credits"""
    return {'total': Decimal('0')}

def round_to_cents(amount):
    """Round to nearest cent"""
    return Decimal(str(amount)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
