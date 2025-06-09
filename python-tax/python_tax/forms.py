"""
Tax form definitions and field mappings
"""

class BaseForm:
    def __init__(self, tax_year):
        self.tax_year = tax_year
    
    def get_field_names(self):
        return []

class Form1040(BaseForm):
    def get_field_names(self):
        return ['filing_status', 'total_income', 'agi', 'taxable_income']
