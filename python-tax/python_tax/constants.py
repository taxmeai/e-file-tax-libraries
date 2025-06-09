"""
Tax constants and lookup tables for US federal and state taxes
Based on official IRS publications and tax law
"""

from decimal import Decimal
from typing import Dict, List, Tuple, Any

# Current tax year
TAX_YEAR_2024 = 2024

# Filing status options
FILING_STATUSES = [
    'single',
    'married_filing_jointly', 
    'married_filing_separately',
    'head_of_household',
    'qualifying_widow'
]

# Tax brackets for 2024 (rates are marginal tax rates)
# Format: (min_income, max_income, rate)
TAX_BRACKETS = {
    2024: {
        'single': [
            (Decimal('0'), Decimal('11000'), Decimal('0.10')),
            (Decimal('11000'), Decimal('44725'), Decimal('0.12')),
            (Decimal('44725'), Decimal('95375'), Decimal('0.22')),
            (Decimal('95375'), Decimal('197050'), Decimal('0.24')),
            (Decimal('197050'), Decimal('250525'), Decimal('0.32')),
            (Decimal('250525'), Decimal('609350'), Decimal('0.35')),
            (Decimal('609350'), Decimal('999999999'), Decimal('0.37'))
        ],
        'married_filing_jointly': [
            (Decimal('0'), Decimal('22000'), Decimal('0.10')),
            (Decimal('22000'), Decimal('89450'), Decimal('0.12')),
            (Decimal('89450'), Decimal('190750'), Decimal('0.22')),
            (Decimal('190750'), Decimal('364200'), Decimal('0.24')),
            (Decimal('364200'), Decimal('462500'), Decimal('0.32')),
            (Decimal('462500'), Decimal('693750'), Decimal('0.35')),
            (Decimal('693750'), Decimal('999999999'), Decimal('0.37'))
        ]
    }
}

# Standard deductions for 2024
STANDARD_DEDUCTIONS = {
    2024: {
        'single': Decimal('14600'),
        'married_filing_jointly': Decimal('29200'),
        'married_filing_separately': Decimal('14600'),
        'head_of_household': Decimal('21900'),
        'qualifying_widow': Decimal('29200')
    }
}

# Payroll tax rates and limits for 2024
PAYROLL_TAX_RATES = {
    2024: {
        'social_security_rate': Decimal('0.062'),  # Employee portion
        'medicare_rate': Decimal('0.0145'),
        'social_security_wage_base': Decimal('160200'),
        'additional_medicare_threshold_single': Decimal('200000'),
        'additional_medicare_threshold_married': Decimal('250000'),
        'additional_medicare_rate': Decimal('0.009'),
        'self_employment_ss_rate': Decimal('0.124'),  # Combined employer/employee
        'self_employment_medicare_rate': Decimal('0.029')
    }
}

# Child Tax Credit amounts for 2024
CHILD_TAX_CREDIT_AMOUNTS = {
    2024: {
        'per_child': Decimal('2000'),
        'per_other_dependent': Decimal('500'),
        'refundable_portion': Decimal('1700'),
        'phase_out_single': Decimal('200000'),
        'phase_out_married_filing_jointly': Decimal('400000'),
        'phase_out_married_filing_separately': Decimal('200000'),
        'phase_out_head_of_household': Decimal('200000'),
        'phase_out_qualifying_widow': Decimal('400000')
    }
}

# Earned Income Credit table (simplified - actual IRS table is more complex)
EARNED_INCOME_CREDIT_TABLE = {
    2024: {
        'single': {
            0: {'max_credit': Decimal('600'), 'phase_out_start': Decimal('10000'), 'phase_out_end': Decimal('17640')},
            1: {'max_credit': Decimal('3800'), 'phase_out_start': Decimal('12000'), 'phase_out_end': Decimal('47915')},
            2: {'max_credit': Decimal('6300'), 'phase_out_start': Decimal('12000'), 'phase_out_end': Decimal('53865')},
            3: {'max_credit': Decimal('7100'), 'phase_out_start': Decimal('12000'), 'phase_out_end': Decimal('57414')}
        },
        'married_filing_jointly': {
            0: {'max_credit': Decimal('600'), 'phase_out_start': Decimal('16000'), 'phase_out_end': Decimal('23640')},
            1: {'max_credit': Decimal('3800'), 'phase_out_start': Decimal('18000'), 'phase_out_end': Decimal('53915')},
            2: {'max_credit': Decimal('6300'), 'phase_out_start': Decimal('18000'), 'phase_out_end': Decimal('59865')},
            3: {'max_credit': Decimal('7100'), 'phase_out_start': Decimal('18000'), 'phase_out_end': Decimal('63414')}
        }
    }
}

# State tax rates (simplified - actual rates vary by income level)
STATE_TAX_RATES = {
    'AL': Decimal('0.05'),    # Alabama
    'AK': Decimal('0.00'),    # Alaska - no income tax
    'AZ': Decimal('0.045'),   # Arizona
    'AR': Decimal('0.055'),   # Arkansas
    'CA': Decimal('0.08'),    # California
    'CO': Decimal('0.0463'),  # Colorado
    'CT': Decimal('0.065'),   # Connecticut
    'DE': Decimal('0.055'),   # Delaware
    'FL': Decimal('0.00'),    # Florida - no income tax
    'GA': Decimal('0.055'),   # Georgia
    'HI': Decimal('0.085'),   # Hawaii
    'ID': Decimal('0.058'),   # Idaho
    'IL': Decimal('0.0495'),  # Illinois
    'IN': Decimal('0.032'),   # Indiana
    'IA': Decimal('0.065'),   # Iowa
    'KS': Decimal('0.057'),   # Kansas
    'KY': Decimal('0.05'),    # Kentucky
    'LA': Decimal('0.045'),   # Louisiana
    'ME': Decimal('0.075'),   # Maine
    'MD': Decimal('0.055'),   # Maryland
    'MA': Decimal('0.05'),    # Massachusetts
    'MI': Decimal('0.0425'),  # Michigan
    'MN': Decimal('0.0698'),  # Minnesota
    'MS': Decimal('0.05'),    # Mississippi
    'MO': Decimal('0.054'),   # Missouri
    'MT': Decimal('0.0675'),  # Montana
    'NE': Decimal('0.0684'),  # Nebraska
    'NV': Decimal('0.00'),    # Nevada - no income tax
    'NH': Decimal('0.00'),    # New Hampshire - no income tax on wages
    'NJ': Decimal('0.0637'),  # New Jersey
    'NM': Decimal('0.049'),   # New Mexico
    'NY': Decimal('0.065'),   # New York
    'NC': Decimal('0.049'),   # North Carolina
    'ND': Decimal('0.0295'),  # North Dakota
    'OH': Decimal('0.04'),    # Ohio
    'OK': Decimal('0.05'),    # Oklahoma
    'OR': Decimal('0.075'),   # Oregon
    'PA': Decimal('0.0307'),  # Pennsylvania
    'RI': Decimal('0.0599'),  # Rhode Island
    'SC': Decimal('0.07'),    # South Carolina
    'SD': Decimal('0.00'),    # South Dakota - no income tax
    'TN': Decimal('0.00'),    # Tennessee - no income tax on wages
    'TX': Decimal('0.00'),    # Texas - no income tax
    'UT': Decimal('0.0495'),  # Utah
    'VT': Decimal('0.066'),   # Vermont
    'VA': Decimal('0.0575'),  # Virginia
    'WA': Decimal('0.00'),    # Washington - no income tax
    'WV': Decimal('0.065'),   # West Virginia
    'WI': Decimal('0.0627'),  # Wisconsin
    'WY': Decimal('0.00'),    # Wyoming - no income tax
    'DC': Decimal('0.06')     # District of Columbia
}

# States with no income tax
NO_INCOME_TAX_STATES = ['AK', 'FL', 'NV', 'NH', 'SD', 'TN', 'TX', 'WA', 'WY']

# Alternative Minimum Tax (AMT) exemption amounts for 2024
AMT_EXEMPTIONS = {
    2024: {
        'single': Decimal('85700'),
        'married_filing_jointly': Decimal('133300'),
        'married_filing_separately': Decimal('66650'),
        'head_of_household': Decimal('85700'),
        'qualifying_widow': Decimal('133300')
    }
}

# AMT tax rates
AMT_TAX_RATES = {
    2024: {
        'rate_1': Decimal('0.26'),  # First bracket
        'rate_2': Decimal('0.28'),  # Second bracket
        'bracket_threshold_single': Decimal('220700'),
        'bracket_threshold_married_jointly': Decimal('220700'),
        'bracket_threshold_married_separately': Decimal('110350')
    }
}

# IRS processing and status codes
IRS_STATUS_CODES = {
    'pending': '201',
    'accepted': '202', 
    'rejected': '901',
    'transmitted': '200',
    'acknowledged': '203'
}

# Form validation rules
FORM_VALIDATION_RULES = {
    'ssn': {
        'pattern': r'^\d{3}-\d{2}-\d{4}Decimal('364200'), Decimal('462500'), Decimal('0.32')),
            (Decimal('462500'), Decimal('693750'), Decimal('0.35')),
            (Decimal('693750'), Decimal('999999999'), Decimal('0.37'))
        ],
        'married_filing_separately': [
            (Decimal('0'), Decimal('11000'), Decimal('0.10')),
            (Decimal('11000'), Decimal('44725'), Decimal('0.12')),
            (Decimal('44725'), Decimal('95375'), Decimal('0.22')),
            (Decimal('95375'), Decimal('182050'), Decimal('0.24')),
            (Decimal('182050'), Decimal('231250'), Decimal('0.32')),
            (Decimal('231250'), Decimal('346875'), Decimal('0.35')),
            (Decimal('346875'), Decimal('999999999'), Decimal('0.37'))
        ],
        'head_of_household': [
            (Decimal('0'), Decimal('15700'), Decimal('0.10')),
            (Decimal('15700'), Decimal('59850'), Decimal('0.12')),
            (Decimal('59850'), Decimal('95350'), Decimal('0.22')),
            (Decimal('95350'), Decimal('197050'), Decimal('0.24')),
            (Decimal('197050'), Decimal('250525'), Decimal('0.32')),
            (Decimal('250525'), Decimal('609350'), Decimal('0.35')),
            (Decimal('609350'), Decimal('999999999'), Decimal('0.37'))
        ],
        'qualifying_widow': [
            (Decimal('0'), Decimal('22000'), Decimal('0.10')),
            (Decimal('22000'), Decimal('89450'), Decimal('0.12')),
            (Decimal('89450'), Decimal('190750'), Decimal('0.22')),
            (Decimal('190750'), Decimal('364200'), Decimal('0.24')),
            (,
        'required': True,
        'length': 11
    },
    'ein': {
        'pattern': r'^\d{2}-\d{7}Decimal('364200'), Decimal('462500'), Decimal('0.32')),
            (Decimal('462500'), Decimal('693750'), Decimal('0.35')),
            (Decimal('693750'), Decimal('999999999'), Decimal('0.37'))
        ],
        'married_filing_separately': [
            (Decimal('0'), Decimal('11000'), Decimal('0.10')),
            (Decimal('11000'), Decimal('44725'), Decimal('0.12')),
            (Decimal('44725'), Decimal('95375'), Decimal('0.22')),
            (Decimal('95375'), Decimal('182050'), Decimal('0.24')),
            (Decimal('182050'), Decimal('231250'), Decimal('0.32')),
            (Decimal('231250'), Decimal('346875'), Decimal('0.35')),
            (Decimal('346875'), Decimal('999999999'), Decimal('0.37'))
        ],
        'head_of_household': [
            (Decimal('0'), Decimal('15700'), Decimal('0.10')),
            (Decimal('15700'), Decimal('59850'), Decimal('0.12')),
            (Decimal('59850'), Decimal('95350'), Decimal('0.22')),
            (Decimal('95350'), Decimal('197050'), Decimal('0.24')),
            (Decimal('197050'), Decimal('250525'), Decimal('0.32')),
            (Decimal('250525'), Decimal('609350'), Decimal('0.35')),
            (Decimal('609350'), Decimal('999999999'), Decimal('0.37'))
        ],
        'qualifying_widow': [
            (Decimal('0'), Decimal('22000'), Decimal('0.10')),
            (Decimal('22000'), Decimal('89450'), Decimal('0.12')),
            (Decimal('89450'), Decimal('190750'), Decimal('0.22')),
            (Decimal('190750'), Decimal('364200'), Decimal('0.24')),
            (,
        'required': True,
        'length': 10
    },
    'currency': {
        'min_value': Decimal('-999999999.99'),
        'max_value': Decimal('999999999.99'),
        'decimal_places': 2
    },
    'percentage': {
        'min_value': Decimal('0'),
        'max_value': Decimal('100'),
        'decimal_places': 3
    }
}

# Education credit limits and phase-outs for 2024
EDUCATION_CREDITS = {
    2024: {
        'american_opportunity': {
            'max_credit': Decimal('2500'),
            'refundable_portion': Decimal('0.40'),  # 40% of credit is refundable
            'expense_limit': Decimal('4000'),
            'phase_out_start_single': Decimal('80000'),
            'phase_out_end_single': Decimal('90000'),
            'phase_out_start_married': Decimal('160000'),
            'phase_out_end_married': Decimal('180000'),
            'max_years': 4
        },
        'lifetime_learning': {
            'max_credit': Decimal('2000'),
            'credit_rate': Decimal('0.20'),  # 20% of qualified expenses
            'expense_limit': Decimal('10000'),
            'phase_out_start_single': Decimal('80000'),
            'phase_out_end_single': Decimal('90000'),
            'phase_out_start_married': Decimal('160000'),
            'phase_out_end_married': Decimal('180000')
        }
    }
}

# Health Savings Account (HSA) contribution limits for 2024
HSA_LIMITS = {
    2024: {
        'individual_coverage': Decimal('4150'),
        'family_coverage': Decimal('8300'),
        'catch_up_contribution': Decimal('1000'),  # For age 55+
        'minimum_deductible_individual': Decimal('1600'),
        'minimum_deductible_family': Decimal('3200'),
        'max_out_of_pocket_individual': Decimal('8050'),
        'max_out_of_pocket_family': Decimal('16100')
    }
}

# Retirement plan contribution limits for 2024
RETIREMENT_LIMITS = {
    2024: {
        '401k': {
            'employee_contribution': Decimal('23000'),
            'catch_up_contribution': Decimal('7500'),  # For age 50+
            'total_limit': Decimal('69000')  # Employee + employer
        },
        'ira': {
            'contribution_limit': Decimal('7000'),
            'catch_up_contribution': Decimal('1000'),  # For age 50+
            'roth_phase_out_start_single': Decimal('138000'),
            'roth_phase_out_end_single': Decimal('153000'),
            'roth_phase_out_start_married': Decimal('218000'),
            'roth_phase_out_end_married': Decimal('228000')
        },
        'sep_ira': {
            'contribution_rate': Decimal('0.25'),  # 25% of compensation
            'max_contribution': Decimal('69000')
        }
    }
}

# Capital gains tax rates for 2024
CAPITAL_GAINS_RATES = {
    2024: {
        'short_term': 'ordinary_income',  # Taxed as ordinary income
        'long_term': {
            'rate_0': {
                'rate': Decimal('0.00'),
                'single_threshold': Decimal('47025'),
                'married_jointly_threshold': Decimal('94050'),
                'married_separately_threshold': Decimal('47025'),
                'head_of_household_threshold': Decimal('63000')
            },
            'rate_15': {
                'rate': Decimal('0.15'),
                'single_threshold': Decimal('518900'),
                'married_jointly_threshold': Decimal('583750'),
                'married_separately_threshold': Decimal('291875'),
                'head_of_household_threshold': Decimal('551350')
            },
            'rate_20': {
                'rate': Decimal('0.20'),
                'applies_above_threshold': True  # For income above the 15% thresholds
            }
        }
    }
}

# Net Investment Income Tax (NIIT) thresholds for 2024
NIIT_THRESHOLDS = {
    2024: {
        'rate': Decimal('0.038'),  # 3.8%
        'single_threshold': Decimal('200000'),
        'married_jointly_threshold': Decimal('250000'),
        'married_separately_threshold': Decimal('125000'),
        'head_of_household_threshold': Decimal('200000')
    }
}

# Affordable Care Act (ACA) penalty amounts for 2024
ACA_PENALTY = {
    2024: {
        'penalty_amount': Decimal('0'),  # No federal penalty as of 2019
        'minimum_essential_coverage_required': False
    }
}

# Dependency exemption amounts (historical - not applicable for 2024)
DEPENDENCY_EXEMPTIONS = {
    2017: Decimal('4050'),  # Last year before TCJA eliminated personal exemptions
    2024: Decimal('0')      # No personal exemptions under TCJA
}

# Standard mileage rates for 2024
MILEAGE_RATES = {
    2024: {
        'business': Decimal('0.67'),      # Per mile for business use
        'medical': Decimal('0.21'),       # Per mile for medical/moving
        'charitable': Decimal('0.14')     # Per mile for charitable purposes
    }
}

# Per diem rates for travel (federal rates)
PER_DIEM_RATES = {
    2024: {
        'meals_and_incidentals': {
            'standard': Decimal('68'),
            'high_cost': Decimal('80')
        },
        'lodging': {
            'varies_by_location': True,
            'standard_conus': Decimal('98')
        }
    }
}

# Self-employment tax calculation factors
SE_TAX_FACTORS = {
    2024: {
        'deduction_factor': Decimal('0.9235'),  # 92.35% of SE income subject to SE tax
        'deduction_rate': Decimal('0.5'),       # 50% of SE tax is deductible
        'ss_wage_base': Decimal('160200'),      # Social Security wage base
        'medicare_additional_threshold_single': Decimal('200000'),
        'medicare_additional_threshold_married': Decimal('250000')
    }
}

# State abbreviations and names mapping
STATE_ABBREVIATIONS = {
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

# Tax form due dates
TAX_DUE_DATES = {
    2024: {
        'individual_returns': '2025-04-15',
        'corporate_returns': '2025-04-15',
        'partnership_returns': '2025-03-15',
        'extension_deadline': '2025-10-15',
        'quarterly_estimates': [
            '2024-04-15',  # Q1
            '2024-06-17',  # Q2
            '2024-09-16',  # Q3
            '2025-01-15'   # Q4
        ]
    }
}

# Maximum adjustments to income for 2024
ADJUSTMENT_LIMITS = {
    2024: {
        'student_loan_interest': Decimal('2500'),
        'educator_expenses': Decimal('300'),
        'tuition_and_fees': Decimal('0'),  # Expired after 2020
        'ira_deduction_single': Decimal('7000'),
        'ira_deduction_married': Decimal('7000'),
        'hsa_individual': Decimal('4150'),
        'hsa_family': Decimal('8300')
    }
}Decimal('364200'), Decimal('462500'), Decimal('0.32')),
            (Decimal('462500'), Decimal('693750'), Decimal('0.35')),
            (Decimal('693750'), Decimal('999999999'), Decimal('0.37'))
        ],
        'married_filing_separately': [
            (Decimal('0'), Decimal('11000'), Decimal('0.10')),
            (Decimal('11000'), Decimal('44725'), Decimal('0.12')),
            (Decimal('44725'), Decimal('95375'), Decimal('0.22')),
            (Decimal('95375'), Decimal('182050'), Decimal('0.24')),
            (Decimal('182050'), Decimal('231250'), Decimal('0.32')),
            (Decimal('231250'), Decimal('346875'), Decimal('0.35')),
            (Decimal('346875'), Decimal('999999999'), Decimal('0.37'))
        ],
        'head_of_household': [
            (Decimal('0'), Decimal('15700'), Decimal('0.10')),
            (Decimal('15700'), Decimal('59850'), Decimal('0.12')),
            (Decimal('59850'), Decimal('95350'), Decimal('0.22')),
            (Decimal('95350'), Decimal('197050'), Decimal('0.24')),
            (Decimal('197050'), Decimal('250525'), Decimal('0.32')),
            (Decimal('250525'), Decimal('609350'), Decimal('0.35')),
            (Decimal('609350'), Decimal('999999999'), Decimal('0.37'))
        ],
        'qualifying_widow': [
            (Decimal('0'), Decimal('22000'), Decimal('0.10')),
            (Decimal('22000'), Decimal('89450'), Decimal('0.12')),
            (Decimal('89450'), Decimal('190750'), Decimal('0.22')),
            (Decimal('190750'), Decimal('364200'), Decimal('0.24')),
            ]
            }
