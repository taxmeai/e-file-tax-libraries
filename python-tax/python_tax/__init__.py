"""
Python Tax Calculation Library
A comprehensive library for US federal and state tax calculations

Based on research from open-source projects like HabuTax and py1040
"""

from .calculators import (
    FederalTaxCalculator,
    StateTaxCalculator,
    PayrollTaxCalculator,
    TaxSummaryCalculator
)

from .forms import (
    Form1040,
    ScheduleA,
    ScheduleB,
    ScheduleC,
    ScheduleD,
    Form8812,
    FormW2,
    Form1099
)

from .constants import (
    TAX_YEAR_2024,
    TAX_BRACKETS,
    STANDARD_DEDUCTIONS,
    FILING_STATUSES,
    STATE_TAX_RATES
)

from .validators import (
    TaxDataValidator,
    FormValidator,
    CalculationValidator
)

from .utils import (
    format_currency,
    calculate_agi,
    calculate_taxable_income,
    apply_tax_brackets,
    calculate_credits
)

__version__ = "0.1.0"
__author__ = "E-File Backend Team"
__description__ = "US Tax Calculation Library"

# Main calculator class for easy access
class TaxCalculator:
    """
    Main tax calculator interface
    Usage:
        calculator = TaxCalculator(tax_year=2024)
        result = calculator.calculate_taxes(taxpayer_data)
    """
    
    def __init__(self, tax_year: int = 2024):
        self.tax_year = tax_year
        self.federal_calc = FederalTaxCalculator(tax_year)
        self.state_calc = StateTaxCalculator(tax_year)
        self.payroll_calc = PayrollTaxCalculator(tax_year)
        self.summary_calc = TaxSummaryCalculator(tax_year)
        
    def calculate_taxes(self, taxpayer_data: dict) -> dict:
        """Calculate complete tax return"""
        return self.summary_calc.calculate_complete_return(taxpayer_data)
    
    def calculate_federal_only(self, taxpayer_data: dict) -> dict:
        """Calculate federal taxes only"""
        return self.federal_calc.calculate(taxpayer_data)
    
    def calculate_state_only(self, taxpayer_data: dict, state: str) -> dict:
        """Calculate state taxes only"""
        return self.state_calc.calculate(taxpayer_data, state)
    
    def estimate_quarterly_payments(self, taxpayer_data: dict) -> dict:
        """Estimate quarterly tax payments"""
        return self.summary_calc.estimate_quarterly_payments(taxpayer_data)

# Export main interface
__all__ = [
    'TaxCalculator',
    'FederalTaxCalculator',
    'StateTaxCalculator',
    'PayrollTaxCalculator',
    'TaxSummaryCalculator',
    'Form1040',
    'ScheduleA',
    'ScheduleB', 
    'ScheduleC',
    'ScheduleD',
    'Form8812',
    'FormW2',
    'Form1099',
    'TAX_YEAR_2024',
    'TAX_BRACKETS',
    'STANDARD_DEDUCTIONS',
    'FILING_STATUSES',
    'STATE_TAX_RATES',
    'TaxDataValidator',
    'FormValidator',
    'CalculationValidator',
    'format_currency',
    'calculate_agi',
    'calculate_taxable_income',
    'apply_tax_brackets',
    'calculate_credits'
]
