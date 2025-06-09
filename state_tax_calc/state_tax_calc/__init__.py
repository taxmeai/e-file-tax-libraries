"""
State Tax Calculation Library
Comprehensive state income tax calculations for all US states

This library provides:
- State-specific tax calculations for all 50 states + DC
- State form generation and validation
- Multi-state tax scenario handling
- Reciprocity agreements between states
- State-specific deductions and credits
"""

from typing import Dict, List, Any, Optional
from decimal import Decimal
from enum import Enum

from .calculators import (
    StateCalculatorFactory,
    CaliforniaCalculator,
    NewYorkCalculator,
    TexasCalculator,
    FloridaCalculator,
    IllinoisCalculator,
    PennsylvaniaCalculator,
    OhioCalculator,
    GeorgiaCalculator,
    NorthCarolinaCalculator,
    MichiganCalculator,
    NoTaxStateCalculator
)

from .forms import (
    StateFormManager,
    CaliforniaForms,
    NewYorkForms,
    StateForms
)

from .constants import (
    STATE_TAX_RATES_2024,
    STATE_STANDARD_DEDUCTIONS,
    STATE_FILING_STATUS_MAP,
    NO_INCOME_TAX_STATES,
    RECIPROCITY_AGREEMENTS,
    STATE_ABBREVIATIONS
)

from .validators import (
    StateFormValidator,
    ResidencyValidator,
    MultiStateValidator
)

from .utils import (
    determine_residency_status,
    calculate_apportionment,
    handle_reciprocity,
    format_state_currency
)

__version__ = "0.1.0"
__author__ = "E-File Backend Team"
__description__ = "US State Tax Calculation Library"

class StateTaxCalculator:
    """
    Main state tax calculator interface
    
    Handles complex state tax scenarios including:
    - Multi-state returns
    - Part-year residency
    - Reciprocity agreements
    - State-specific forms and calculations
    """
    
    def __init__(self, tax_year: int = 2024):
        self.tax_year = tax_year
        self.calculator_factory = StateCalculatorFactory(tax_year)
        self.form_manager = StateFormManager(tax_year)
        self.residency_validator = ResidencyValidator()
        self.multistate_validator = MultiStateValidator()
    
    def calculate_state_tax(
        self, 
        taxpayer_data: dict, 
        state: str, 
        residency_status: str = 'resident'
    ) -> dict:
        """
        Calculate state income tax for a single state
        
        Args:
            taxpayer_data: Federal tax return data
            state: Two-letter state code
            residency_status: 'resident', 'nonresident', or 'part_year'
            
        Returns:
            dict: State tax calculation results
        """
        if not self._validate_state_code(state):
            raise ValueError(f"Invalid state code: {state}")
        
        # Get state-specific calculator
        calculator = self.calculator_factory.get_calculator(state)
        
        # Calculate state tax
        result = calculator.calculate(taxpayer_data, residency_status)
        
        # Add state-specific metadata
        result.update({
            'state': state,
            'state_name': self._get_state_name(state),
            'residency_status': residency_status,
            'tax_year': self.tax_year,
            'has_income_tax': state not in NO_INCOME_TAX_STATES
        })
        
        return result
    
    def calculate_multistate_tax(
        self, 
        taxpayer_data: dict, 
        state_scenarios: List[dict]
    ) -> dict:
        """
        Calculate taxes for multiple states
        
        Args:
            taxpayer_data: Federal tax return data
            state_scenarios: List of state tax scenarios
                [
                    {'state': 'CA', 'residency': 'resident', 'income': {...}},
                    {'state': 'NY', 'residency': 'nonresident', 'income': {...}}
                ]
                
        Returns:
            dict: Multi-state tax results with optimization
        """
        results = {}
        total_state_tax = Decimal('0')
        
        for scenario in state_scenarios:
            state = scenario['state']
            residency = scenario.get('residency', 'resident')
            state_income = scenario.get('income', taxpayer_data)
            
            # Calculate for this state
            state_result = self.calculate_state_tax(
                state_income, 
                state, 
                residency
            )
            
            results[state] = state_result
            total_state_tax += state_result.get('state_tax_liability', 0)
        
        # Handle reciprocity agreements and credits
        optimized_results = self._optimize_multistate_tax(results, taxpayer_data)
        
        return {
            'individual_states': optimized_results,
            'total_state_tax': total_state_tax,
            'optimization_applied': True,
            'summary': self._generate_multistate_summary(optimized_results)
        }
    
    def estimate_quarterly_payments(
        self, 
        taxpayer_data: dict, 
        state: str
    ) -> dict:
        """Estimate quarterly state tax payments"""
        annual_result = self.calculate_state_tax(taxpayer_data, state)
        
        quarterly_amount = annual_result.get('state_tax_liability', 0) / 4
        
        return {
            'state': state,
            'annual_tax': annual_result.get('state_tax_liability', 0),
            'quarterly_payment': quarterly_amount,
            'due_dates': [
                f'{self.tax_year + 1}-01-15',  # Q4 previous year
                f'{self.tax_year + 1}-04-15',  # Q1
                f'{self.tax_year + 1}-06-15',  # Q2  
                f'{self.tax_year + 1}-09-15'   # Q3
            ]
        }
    
    def get_state_forms_required(
        self, 
        taxpayer_data: dict, 
        state: str,
        residency_status: str = 'resident'
    ) -> List[str]:
        """Get list of required state forms"""
        calculator = self.calculator_factory.get_calculator(state)
        return calculator.get_required_forms(taxpayer_data, residency_status)
    
    def validate_state_return(
        self, 
        taxpayer_data: dict, 
        state: str
    ) -> dict:
        """Validate state tax return data"""
        validator = StateFormValidator(state, self.tax_year)
        return validator.validate(taxpayer_data)
    
    def _validate_state_code(self, state: str) -> bool:
        """Validate state code"""
        return state.upper() in STATE_ABBREVIATIONS
    
    def _get_state_name(self, state: str) -> str:
        """Get full state name from abbreviation"""
        state_names = {
            'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
            'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
            'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
            'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
            'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
            'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
            'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
            'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
            'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
            'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
            'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
            'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
            'WI': 'Wisconsin', 'WY': 'Wyoming', 'DC': 'District of Columbia'
        }
        return state_names.get(state.upper(), state)
    
    def _optimize_multistate_tax(
        self, 
        state_results: dict, 
        taxpayer_data: dict
    ) -> dict:
        """Apply multistate tax optimizations"""
        # Handle reciprocity agreements
        # Apply credits for taxes paid to other states
        # Optimize allocation and apportionment
        
        optimized = state_results.copy()
        
        # Apply reciprocity agreements
        for state1, result1 in state_results.items():
            for state2, result2 in state_results.items():
                if state1 != state2:
                    reciprocity = RECIPROCITY_AGREEMENTS.get(state1, {}).get(state2)
                    if reciprocity:
                        # Apply reciprocity benefits
                        optimized[state1] = self._apply_reciprocity(
                            result1, result2, reciprocity
                        )
        
        return optimized
    
    def _apply_reciprocity(self, state1_result: dict, state2_result: dict, reciprocity: dict) -> dict:
        """Apply reciprocity agreement benefits"""
        # Implementation would depend on specific reciprocity rules
        return state1_result
    
    def _generate_multistate_summary(self, state_results: dict) -> dict:
        """Generate summary of multistate tax situation"""
        total_tax = sum(
            result.get('state_tax_liability', 0) 
            for result in state_results.values()
        )
        
        states_with_tax = [
            state for state, result in state_results.items()
            if result.get('state_tax_liability', 0) > 0
        ]
        
        return {
            'total_state_tax': total_tax,
            'states_with_tax_due': states_with_tax,
            'number_of_states': len(state_results),
            'highest_tax_state': max(
                state_results.items(), 
                key=lambda x: x[1].get('state_tax_liability', 0)
            )[0] if state_results else None
        }

class StateFormGenerator:
    """Generate state-specific tax forms"""
    
    def __init__(self, tax_year: int = 2024):
        self.tax_year = tax_year
        self.form_manager = StateFormManager(tax_year)
    
    def generate_state_forms(
        self, 
        taxpayer_data: dict, 
        state: str,
        output_dir: str = None
    ) -> List[str]:
        """Generate all required state forms"""
        calculator = StateCalculatorFactory(self.tax_year).get_calculator(state)
        required_forms = calculator.get_required_forms(taxpayer_data)
        
        generated_files = []
        
        for form_name in required_forms:
            form_data = calculator.populate_form_data(taxpayer_data, form_name)
            output_path = self.form_manager.generate_pdf(
                state, form_name, form_data, output_dir
            )
            generated_files.append(output_path)
        
        return generated_files

# Export main interfaces
__all__ = [
    'StateTaxCalculator',
    'StateFormGenerator',
    'StateCalculatorFactory',
    'CaliforniaCalculator',
    'NewYorkCalculator',
    'TexasCalculator',
    'FloridaCalculator',
    'IllinoisCalculator',
    'PennsylvaniaCalculator',
    'OhioCalculator',
    'GeorgiaCalculator', 
    'NorthCarolinaCalculator',
    'MichiganCalculator',
    'NoTaxStateCalculator',
    'StateFormManager',
    'CaliforniaForms',
    'NewYorkForms',
    'StateForms',
    'STATE_TAX_RATES_2024',
    'STATE_STANDARD_DEDUCTIONS',
    'STATE_FILING_STATUS_MAP',
    'NO_INCOME_TAX_STATES',
    'RECIPROCITY_AGREEMENTS',
    'STATE_ABBREVIATIONS',
    'StateFormValidator',
    'ResidencyValidator',
    'MultiStateValidator',
    'determine_residency_status',
    'calculate_apportionment',
    'handle_reciprocity',
    'format_state_currency'
]

# Default calculator instance for easy access
default_state_calculator = StateTaxCalculator()

def calculate_state_tax(taxpayer_data: dict, state: str, residency_status: str = 'resident') -> dict:
    """Convenience function to calculate state tax using default calculator"""
    return default_state_calculator.calculate_state_tax(taxpayer_data, state, residency_status)

def get_no_tax_states() -> List[str]:
    """Get list of states with no income tax"""
    return list(NO_INCOME_TAX_STATES)

def check_reciprocity(state1: str, state2: str) -> Optional[dict]:
    """Check if two states have reciprocity agreements"""
    return RECIPROCITY_AGREEMENTS.get(state1, {}).get(state2)
