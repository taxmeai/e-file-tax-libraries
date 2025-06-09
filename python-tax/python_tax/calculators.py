"""
Tax calculation engines for federal and state taxes
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Any, Optional, Tuple
import logging

from .constants import (
    TAX_BRACKETS, 
    STANDARD_DEDUCTIONS, 
    PAYROLL_TAX_RATES,
    CHILD_TAX_CREDIT_AMOUNTS,
    EARNED_INCOME_CREDIT_TABLE
)
from .utils import (
    calculate_agi,
    calculate_taxable_income,
    apply_tax_brackets,
    round_to_cents
)

logger = logging.getLogger(__name__)

class FederalTaxCalculator:
    """Federal income tax calculator following IRS rules"""
    
    def __init__(self, tax_year: int = 2024):
        self.tax_year = tax_year
        self.tax_brackets = TAX_BRACKETS.get(tax_year, TAX_BRACKETS[2024])
        self.standard_deductions = STANDARD_DEDUCTIONS.get(tax_year, STANDARD_DEDUCTIONS[2024])
        
    def calculate(self, taxpayer_data: dict) -> dict:
        """
        Calculate complete federal tax liability
        
        Args:
            taxpayer_data: Dictionary containing:
                - filing_status: str
                - income_sources: dict (W2s, 1099s, etc.)
                - deductions: dict
                - credits: dict
                - withholdings: dict
                
        Returns:
            dict: Complete federal tax calculation
        """
        try:
            # Step 1: Calculate Adjusted Gross Income (AGI)
            agi = self._calculate_agi(taxpayer_data)
            
            # Step 2: Calculate taxable income
            taxable_income = self._calculate_taxable_income(taxpayer_data, agi)
            
            # Step 3: Calculate income tax using tax brackets
            income_tax = self._calculate_income_tax(
                taxable_income, 
                taxpayer_data['filing_status']
            )
            
            # Step 4: Calculate and apply credits
            credits = self._calculate_credits(taxpayer_data, agi)
            tax_after_credits = max(Decimal('0'), income_tax - credits['total_nonrefundable'])
            
            # Step 5: Calculate other taxes (self-employment, etc.)
            other_taxes = self._calculate_other_taxes(taxpayer_data)
            
            # Step 6: Total tax liability
            total_tax = tax_after_credits + other_taxes
            
            # Step 7: Calculate refund/owe amount
            total_payments = self._calculate_total_payments(taxpayer_data)
            refund_amount = max(Decimal('0'), total_payments - total_tax + credits['total_refundable'])
            owe_amount = max(Decimal('0'), total_tax - total_payments - credits['total_refundable'])
            
            # Step 8: Calculate effective and marginal tax rates
            effective_rate = (total_tax / agi * 100) if agi > 0 else Decimal('0')
            marginal_rate = self._get_marginal_tax_rate(taxable_income, taxpayer_data['filing_status'])
            
            return {
                'agi': round_to_cents(agi),
                'taxable_income': round_to_cents(taxable_income),
                'income_tax_before_credits': round_to_cents(income_tax),
                'total_credits': round_to_cents(credits['total_nonrefundable'] + credits['total_refundable']),
                'tax_after_credits': round_to_cents(tax_after_credits),
                'other_taxes': round_to_cents(other_taxes),
                'total_tax_liability': round_to_cents(total_tax),
                'total_payments': round_to_cents(total_payments),
                'refund_amount': round_to_cents(refund_amount),
                'owe_amount': round_to_cents(owe_amount),
                'effective_tax_rate': round_to_cents(effective_rate),
                'marginal_tax_rate': round_to_cents(marginal_rate),
                'credits_breakdown': credits,
                'calculation_details': {
                    'standard_deduction_used': taxpayer_data.get('deduction_type') == 'standard',
                    'standard_deduction_amount': self.standard_deductions[taxpayer_data['filing_status']],
                    'tax_year': self.tax_year
                }
            }
            
        except Exception as e:
            logger.error(f"Federal tax calculation error: {str(e)}")
            raise
    
    def _calculate_agi(self, taxpayer_data: dict) -> Decimal:
        """Calculate Adjusted Gross Income"""
        income_sources = taxpayer_data.get('income_sources', {})
        
        # W-2 wages
        w2_wages = sum(
            Decimal(str(w2.get('wages_tips_compensation', 0)))
            for w2 in income_sources.get('w2_forms', [])
        )
        
        # 1099 income
        income_1099_total = sum(
            Decimal(str(form_1099.get('amount_1', 0)))
            for form_1099 in income_sources.get('1099_forms', [])
        )
        
        # Other income
        other_income = Decimal(str(income_sources.get('other_income', 0)))
        
        # Total income
        total_income = w2_wages + income_1099_total + other_income
        
        # Above-the-line deductions
        adjustments = taxpayer_data.get('adjustments', {})
        student_loan_interest = Decimal(str(adjustments.get('student_loan_interest', 0)))
        educator_expenses = Decimal(str(adjustments.get('educator_expenses', 0)))
        hsa_deduction = Decimal(str(adjustments.get('hsa_deduction', 0)))
        
        total_adjustments = student_loan_interest + educator_expenses + hsa_deduction
        
        agi = total_income - total_adjustments
        
        return max(Decimal('0'), agi)
    
    def _calculate_taxable_income(self, taxpayer_data: dict, agi: Decimal) -> Decimal:
        """Calculate taxable income after deductions"""
        filing_status = taxpayer_data['filing_status']
        
        # Determine deduction amount
        if taxpayer_data.get('deduction_type') == 'itemized':
            deductions = taxpayer_data.get('itemized_deductions', {})
            total_itemized = sum(
                Decimal(str(amount)) 
                for amount in deductions.values() 
                if isinstance(amount, (int, float, str))
            )
            deduction_amount = total_itemized
        else:
            # Use standard deduction
            deduction_amount = self.standard_deductions[filing_status]
        
        # Calculate taxable income
        taxable_income = agi - deduction_amount
        
        return max(Decimal('0'), taxable_income)
    
    def _calculate_income_tax(self, taxable_income: Decimal, filing_status: str) -> Decimal:
        """Apply tax brackets to calculate income tax"""
        brackets = self.tax_brackets[filing_status]
        tax = Decimal('0')
        
        for min_income, max_income, rate in brackets:
            if taxable_income > min_income:
                bracket_income = min(taxable_income, max_income) - min_income
                if bracket_income > 0:
                    tax += bracket_income * Decimal(str(rate))
                
                if taxable_income <= max_income:
                    break
        
        return tax
    
    def _get_marginal_tax_rate(self, taxable_income: Decimal, filing_status: str) -> Decimal:
        """Get marginal tax rate for given income level"""
        brackets = self.tax_brackets[filing_status]
        
        for min_income, max_income, rate in brackets:
            if min_income <= taxable_income <= max_income:
                return Decimal(str(rate)) * 100
        
        # If above all brackets, return highest rate
        return Decimal(str(brackets[-1][2])) * 100
    
    def _calculate_credits(self, taxpayer_data: dict, agi: Decimal) -> dict:
        """Calculate tax credits"""
        credits = {
            'child_tax_credit': Decimal('0'),
            'earned_income_credit': Decimal('0'),
            'education_credits': Decimal('0'),
            'total_nonrefundable': Decimal('0'),
            'total_refundable': Decimal('0')
        }
        
        # Child Tax Credit
        dependents = taxpayer_data.get('dependents', [])
        qualifying_children = [
            dep for dep in dependents 
            if dep.get('relationship') == 'child' and dep.get('age', 0) < 17
        ]
        
        if qualifying_children:
            child_credit = self._calculate_child_tax_credit(
                len(qualifying_children), 
                agi, 
                taxpayer_data['filing_status']
            )
            credits['child_tax_credit'] = child_credit['total_credit']
            credits['total_refundable'] += child_credit['refundable_portion']
            credits['total_nonrefundable'] += child_credit['nonrefundable_portion']
        
        # Earned Income Credit
        if taxpayer_data.get('earned_income', 0) > 0:
            eic = self._calculate_earned_income_credit(taxpayer_data, agi)
            credits['earned_income_credit'] = eic
            credits['total_refundable'] += eic
        
        # Education Credits
        education_expenses = taxpayer_data.get('education_expenses', 0)
        if education_expenses > 0:
            education_credit = self._calculate_education_credits(education_expenses, agi)
            credits['education_credits'] = education_credit
            credits['total_nonrefundable'] += education_credit
        
        return credits
    
    def _calculate_child_tax_credit(self, num_children: int, agi: Decimal, filing_status: str) -> dict:
        """Calculate Child Tax Credit"""
        credit_amounts = CHILD_TAX_CREDIT_AMOUNTS[self.tax_year]
        
        # Base credit amount
        base_credit = num_children * credit_amounts['per_child']
        
        # Phase-out calculation
        phase_out_threshold = credit_amounts[f'phase_out_{filing_status}']
        if agi > phase_out_threshold:
            phase_out_amount = ((agi - phase_out_threshold) / 1000).to_integral_value(ROUND_HALF_UP) * 50
            base_credit = max(Decimal('0'), base_credit - phase_out_amount)
        
        # Refundable portion
        refundable_portion = min(base_credit, credit_amounts['refundable_portion'] * num_children)
        nonrefundable_portion = base_credit - refundable_portion
        
        return {
            'total_credit': base_credit,
            'refundable_portion': refundable_portion,
            'nonrefundable_portion': nonrefundable_portion
        }
    
    def _calculate_earned_income_credit(self, taxpayer_data: dict, agi: Decimal) -> Decimal:
        """Calculate Earned Income Credit (simplified)"""
        earned_income = Decimal(str(taxpayer_data.get('earned_income', 0)))
        filing_status = taxpayer_data['filing_status']
        num_children = len([
            dep for dep in taxpayer_data.get('dependents', [])
            if dep.get('relationship') == 'child'
        ])
        
        # Simplified EIC calculation - in practice this would use IRS tables
        if filing_status == 'married_filing_jointly':
            income_limit = 60000
        else:
            income_limit = 50000
        
        if agi > income_limit:
            return Decimal('0')
        
        # Basic EIC calculation (simplified)
        if num_children == 0:
            max_credit = 600
        elif num_children == 1:
            max_credit = 3800
        elif num_children == 2:
            max_credit = 6300
        else:
            max_credit = 7100
        
        # Phase-in and phase-out (simplified)
        if earned_income < 10000:
            credit_rate = 0.4 if num_children > 0 else 0.075
            return min(Decimal(str(max_credit)), earned_income * Decimal(str(credit_rate)))
        
        return Decimal(str(max_credit))
    
    def _calculate_education_credits(self, education_expenses: Decimal, agi: Decimal) -> Decimal:
        """Calculate education credits (simplified American Opportunity Credit)"""
        # Simplified calculation - actual implementation would be more complex
        max_credit = Decimal('2500')
        
        # Income phase-out
        if agi > 80000:  # Single filer threshold
            return Decimal('0')
        
        # Credit calculation: 100% of first $2000, 25% of next $2000
        if education_expenses <= 2000:
            return education_expenses
        elif education_expenses <= 4000:
            return Decimal('2000') + (education_expenses - Decimal('2000')) * Decimal('0.25')
        else:
            return max_credit
    
    def _calculate_other_taxes(self, taxpayer_data: dict) -> Decimal:
        """Calculate other taxes (self-employment, etc.)"""
        other_taxes = Decimal('0')
        
        # Self-employment tax
        se_income = Decimal(str(taxpayer_data.get('self_employment_income', 0)))
        if se_income > 0:
            se_tax = self._calculate_self_employment_tax(se_income)
            other_taxes += se_tax
        
        # Additional Medicare tax
        income_sources = taxpayer_data.get('income_sources', {})
        total_medicare_wages = sum(
            Decimal(str(w2.get('medicare_wages', 0)))
            for w2 in income_sources.get('w2_forms', [])
        )
        
        filing_status = taxpayer_data['filing_status']
        medicare_threshold = 250000 if filing_status == 'married_filing_jointly' else 200000
        
        if total_medicare_wages > medicare_threshold:
            additional_medicare = (total_medicare_wages - medicare_threshold) * Decimal('0.009')
            other_taxes += additional_medicare
        
        return other_taxes
    
    def _calculate_self_employment_tax(self, se_income: Decimal) -> Decimal:
        """Calculate self-employment tax"""
        # 92.35% of SE income is subject to SE tax
        se_tax_income = se_income * Decimal('0.9235')
        
        # Social Security portion (up to wage base)
        ss_wage_base = Decimal('160200')  # 2024 amount
        ss_income = min(se_tax_income, ss_wage_base)
        ss_tax = ss_income * Decimal('0.124')  # 12.4%
        
        # Medicare portion (no limit)
        medicare_tax = se_tax_income * Decimal('0.029')  # 2.9%
        
        return ss_tax + medicare_tax
    
    def _calculate_total_payments(self, taxpayer_data: dict) -> Decimal:
        """Calculate total tax payments and withholdings"""
        income_sources = taxpayer_data.get('income_sources', {})
        
        # Federal withholding from W-2s
        federal_withholding = sum(
            Decimal(str(w2.get('federal_income_tax_withheld', 0)))
            for w2 in income_sources.get('w2_forms', [])
        )
        
        # Federal withholding from 1099s
        federal_withholding_1099 = sum(
            Decimal(str(form_1099.get('federal_income_tax_withheld', 0)))
            for form_1099 in income_sources.get('1099_forms', [])
        )
        
        # Estimated tax payments
        estimated_payments = sum(
            Decimal(str(payment))
            for payment in taxpayer_data.get('estimated_payments', [])
        )
        
        return federal_withholding + federal_withholding_1099 + estimated_payments

class PayrollTaxCalculator:
    """Calculate payroll taxes (FICA)"""
    
    def __init__(self, tax_year: int = 2024):
        self.tax_year = tax_year
        self.rates = PAYROLL_TAX_RATES[tax_year]
    
    def calculate(self, taxpayer_data: dict) -> dict:
        """Calculate payroll taxes"""
        income_sources = taxpayer_data.get('income_sources', {})
        
        total_ss_wages = Decimal('0')
        total_medicare_wages = Decimal('0')
        total_ss_withheld = Decimal('0')
        total_medicare_withheld = Decimal('0')
        
        # Sum from all W-2s
        for w2 in income_sources.get('w2_forms', []):
            total_ss_wages += Decimal(str(w2.get('social_security_wages', 0)))
            total_medicare_wages += Decimal(str(w2.get('medicare_wages', 0)))
            total_ss_withheld += Decimal(str(w2.get('social_security_tax_withheld', 0)))
            total_medicare_withheld += Decimal(str(w2.get('medicare_tax_withheld', 0)))
        
        # Calculate correct payroll tax amounts
        ss_wage_base = self.rates['social_security_wage_base']
        limited_ss_wages = min(total_ss_wages, ss_wage_base)
        
        correct_ss_tax = limited_ss_wages * self.rates['social_security_rate']
        correct_medicare_tax = total_medicare_wages * self.rates['medicare_rate']
        
        # Calculate any additional amounts owed or overpaid
        ss_difference = correct_ss_tax - total_ss_withheld
        medicare_difference = correct_medicare_tax - total_medicare_withheld
        
        return {
            'social_security_wages': round_to_cents(total_ss_wages),
            'medicare_wages': round_to_cents(total_medicare_wages),
            'social_security_tax_withheld': round_to_cents(total_ss_withheld),
            'medicare_tax_withheld': round_to_cents(total_medicare_withheld),
            'correct_social_security_tax': round_to_cents(correct_ss_tax),
            'correct_medicare_tax': round_to_cents(correct_medicare_tax),
            'social_security_difference': round_to_cents(ss_difference),
            'medicare_difference': round_to_cents(medicare_difference),
            'total_payroll_tax_difference': round_to_cents(ss_difference + medicare_difference)
        }

class StateTaxCalculator:
    """State tax calculator (simplified)"""
    
    def __init__(self, tax_year: int = 2024):
        self.tax_year = tax_year
    
    def calculate(self, taxpayer_data: dict, state: str) -> dict:
        """Calculate state income tax (simplified)"""
        # This is a simplified implementation
        # prod implementation would have state-specific rules
        
        from .constants import STATE_TAX_RATES
        
        if state in ['AK', 'FL', 'NV', 'NH', 'SD', 'TN', 'TX', 'WA', 'WY']:
            # No state income tax
            return {
                'state': state,
                'state_tax_liability': Decimal('0'),
                'state_withholding': Decimal('0'),
                'state_refund': Decimal('0'),
                'state_owe': Decimal('0'),
                'has_income_tax': False
            }
        
        # Get federal AGI
        federal_calc = FederalTaxCalculator(self.tax_year)
        federal_result = federal_calc.calculate(taxpayer_data)
        agi = federal_result['agi']
        
        # Apply state tax rate (simplified)
        state_rate = STATE_TAX_RATES.get(state, Decimal('0.05'))
        state_tax = agi * state_rate
        
        # Get state withholding
        income_sources = taxpayer_data.get('income_sources', {})
        state_withholding = sum(
            Decimal(str(w2.get('state_income_tax_withheld', 0)))
            for w2 in income_sources.get('w2_forms', [])
        )
        
        # Calculate refund/owe
        refund_amount = max(Decimal('0'), state_withholding - state_tax)
        owe_amount = max(Decimal('0'), state_tax - state_withholding)
        
        return {
            'state': state,
            'state_agi': round_to_cents(agi),
            'state_tax_liability': round_to_cents(state_tax),
            'state_withholding': round_to_cents(state_withholding),
            'state_refund': round_to_cents(refund_amount),
            'state_owe': round_to_cents(owe_amount),
            'has_income_tax': True,
            'state_tax_rate': round_to_cents(state_rate * 100)
        }

class TaxSummaryCalculator:
    """High-level tax summary calculator"""
    
    def __init__(self, tax_year: int = 2024):
        self.tax_year = tax_year
        self.federal_calc = FederalTaxCalculator(tax_year)
        self.state_calc = StateTaxCalculator(tax_year)
        self.payroll_calc = PayrollTaxCalculator(tax_year)
    
    def calculate_complete_return(self, taxpayer_data: dict) -> dict:
        """Calculate complete tax return summary"""
        try:
            # Federal taxes
            federal_result = self.federal_calc.calculate(taxpayer_data)
            
            # State taxes
            state = taxpayer_data.get('state', 'CA')
            state_result = self.state_calc.calculate(taxpayer_data, state)
            
            # Payroll taxes
            payroll_result = self.payroll_calc.calculate(taxpayer_data)
            
            # Combined summary
            total_tax_liability = (
                federal_result['total_tax_liability'] + 
                state_result['state_tax_liability']
            )
            
            total_withholding = (
                federal_result['total_payments'] + 
                state_result['state_withholding']
            )
            
            total_refund = federal_result['refund_amount'] + state_result['state_refund']
            total_owe = federal_result['owe_amount'] + state_result['state_owe']
            
            return {
                'federal': federal_result,
                'state': state_result,
                'payroll': payroll_result,
                'summary': {
                    'total_tax_liability': round_to_cents(total_tax_liability),
                    'total_withholding': round_to_cents(total_withholding),
                    'total_refund': round_to_cents(total_refund),
                    'total_owe': round_to_cents(total_owe),
                    'effective_tax_rate': round_to_cents(
                        (total_tax_liability / federal_result['agi'] * 100) 
                        if federal_result['agi'] > 0 else Decimal('0')
                    )
                },
                'tax_year': self.tax_year,
                'calculation_timestamp': str(Decimal('0'))  # Would use datetime in during implementation
            }
            
        except Exception as e:
            logger.error(f"Complete return calculation error: {str(e)}")
            raise
    
    def estimate_quarterly_payments(self, taxpayer_data: dict) -> dict:
        """Estimate quarterly tax payments"""
        federal_result = self.federal_calc.calculate(taxpayer_data)
        
        # Estimate next year's tax liability
        estimated_annual_tax = federal_result['total_tax_liability']
        
        # Safe harbor: 100% of current year (110% if AGI > $150k)
        safe_harbor_percentage = 1.1 if federal_result['agi'] > 150000 else 1.0
        safe_harbor_amount = estimated_annual_tax * Decimal(str(safe_harbor_percentage))
        
        # Quarterly payment
        quarterly_payment = safe_harbor_amount / 4
        
        return {
            'estimated_annual_tax': round_to_cents(estimated_annual_tax),
            'safe_harbor_amount': round_to_cents(safe_harbor_amount),
            'quarterly_payment': round_to_cents(quarterly_payment),
            'due_dates': [
                f'{self.tax_year + 1}-01-15',  # Q4 previous year
                f'{self.tax_year + 1}-04-15',  # Q1
                f'{self.tax_year + 1}-06-15',  # Q2
                f'{self.tax_year + 1}-09-15'   # Q3
            ]
        }
