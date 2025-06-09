# E-File Backend Tax Calculation Libraries

This repository contains three custom Python libraries for US tax calculations, based on research into how companies like TurboTax access IRS data and open-source tax calculation projects.

## Libraries Overview

### 1. python-tax (v0.1.0)
Core tax calculation engine for federal and state taxes
- Federal income tax calculations using official IRS tax brackets
- Payroll tax (FICA) calculations
- Tax credit calculations (Child Tax Credit, Earned Income Credit, etc.)
- Multi-state tax scenarios
- Based on open-source projects like HabuTax and py1040

### 2. irs-forms (v1.0.0) 
Official IRS form processing and e-filing capabilities
- IRS form definitions and field mappings
- PDF form generation and filling
- XML generation for e-filing
- Form validation against IRS requirements
- Automatic form updates from IRS sources

### 3. state-tax-calc (v0.1.0)
Comprehensive state tax calculations for all US states
- State-specific tax calculations for all 50 states + DC
- Multi-state return handling
- Reciprocity agreements between states
- State form generation

## How Tax Software Companies Get IRS Data

Based on research into TurboTax and other tax software companies:

### Official IRS APIs
- **IRS e-Services**: Companies apply for API client IDs through the IRS
- **IRIS (Information Return Intake System)**: For e-filing information returns
- **TIN Matching**: Validate taxpayer identification numbers
- **Transcript Services**: Access tax transcripts with taxpayer consent

### IRS Free File Alliance
- TurboTax and other companies participate in the IRS Free File program
- Public-private partnership providing free filing for eligible taxpayers
- Companies get early access to updated forms and requirements

### Third-Party Services
- **TaxBandits API**: Provides e-filing capabilities for developers
- **FileYourTaxes.com**: Tax calculation and e-filing API
- Companies can integrate these services rather than building from scratch

### Form Updates
- Companies release new versions when IRS completes form revisions
- Download forms from official IRS sources (www.irs.gov)
- Use IRS XML schemas for electronic filing
- Regular updates when tax laws change

## Building the Libraries

### Prerequisites
```bash
# Python 3.8+ required
python --version

# Install build tools
pip install build setuptools wheel
```

### Directory Structure
```
e-file-backend/
├── python-tax/
│   ├── python_tax/
│   │   ├── __init__.py
│   │   ├── calculators.py
│   │   ├── constants.py
│   │   ├── forms.py
│   │   ├── validators.py
│   │   └── utils.py
│   ├── setup.py
│   ├── README.md
│   └── requirements.txt
├── irs-forms/
│   ├── irs_forms/
│   │   ├── __init__.py
│   │   ├── forms/
│   │   ├── generators/
│   │   ├── validators/
│   │   ├── downloaders/
│   │   └── constants/
│   ├── setup.py
│   ├── README.md
│   └── requirements.txt
├── state-tax-calc/
│   ├── state_tax_calc/
│   │   ├── __init__.py
│   │   ├── calculators/
│   │   ├── forms/
│   │   ├── constants/
│   │   ├── validators/
│   │   └── utils/
│   ├── setup.py
│   ├── README.md
│   └── requirements.txt
└── requirements.txt (main project)
```

### Build Steps

1. **Build python-tax library:**
```bash
cd python-tax/
python -m build
pip install dist/python_tax-0.1.0-py3-none-any.whl
```

2. **Build irs-forms library:**
```bash
cd ../irs-forms/
python -m build
pip install dist/irs_forms-1.0.0-py3-none-any.whl
```

3. **Build state-tax-calc library:**
```bash
cd ../state-tax-calc/
python -m build
pip install dist/state_tax_calc-0.1.0-py3-none-any.whl
```

4. **Install in development mode (recommended for development):**
```bash
# From each library directory
pip install -e .
```

## Usage Examples

### Basic Tax Calculation
```python
from python_tax import TaxCalculator

# Initialize calculator
calculator = TaxCalculator(tax_year=2024)

# Taxpayer data
taxpayer_data = {
    'filing_status': 'single',
    'income_sources': {
        'w2_forms': [{
            'wages_tips_compensation': 75000,
            'federal_income_tax_withheld': 12000,
            'social_security_wages': 75000,
            'social_security_tax_withheld': 4650,
            'medicare_wages': 75000,
            'medicare_tax_withheld': 1087.50
        }]
    },
    'deduction_type': 'standard',
    'dependents': [],
    'state': 'CA'
}

# Calculate taxes
result = calculator.calculate_taxes(taxpayer_data)

print(f"AGI: ${result['federal']['agi']:,.2f}")
print(f"Federal Tax: ${result['federal']['total_tax_liability']:,.2f}")
print(f"State Tax: ${result['state']['state_tax_liability']:,.2f}")
print(f"Refund: ${result['summary']['total_refund']:,.2f}")
```

### IRS Forms Processing
```python
from irs_forms import IRSFormsManager

# Initialize forms manager
forms_manager = IRSFormsManager(tax_year=2024)

# Get Form 1040
form_1040 = forms_manager.get_form('1040')

# Validate form data
validation_result = forms_manager.validate_form_data('1040', form_data)

# Generate PDF
pdf_path = forms_manager.generate_pdf('1040', form_data, 'output/form_1040.pdf')

# Generate e-file XML
xml_content = forms_manager.generate_efile_xml(return_data)
```

### State Tax Calculations
```python
from state_tax_calc import StateTaxCalculator

# Initialize state calculator
state_calc = StateTaxCalculator(tax_year=2024)

# Single state calculation
ca_result = state_calc.calculate_state_tax(
    taxpayer_data, 
    state='CA', 
    residency_status='resident'
)

# Multi-state scenario
multistate_scenarios = [
    {'state': 'CA', 'residency': 'resident', 'income': taxpayer_data},
    {'state': 'NY', 'residency': 'nonresident', 'income': ny_income_data}
]

multistate_result = state_calc.calculate_multistate_tax(
    taxpayer_data, 
    multistate_scenarios
)

print(f"Total state tax: ${multistate_result['total_state_tax']:,.2f}")
```

## Integration with Main Backend

### Updated requirements.txt
```python
# Add to your main requirements.txt:
python-tax==0.1.0
irs-forms==1.0.0
state-tax-calc==0.1.0
```

### Service Integration
```python
# In your existing services/tax_calculation_service.py
from python_tax import TaxCalculator
from irs_forms import IRSFormsManager
from state_tax_calc import StateTaxCalculator

class TaxCalculationService:
    def __init__(self, tax_year: int = 2024):
        self.tax_calculator = TaxCalculator(tax_year)
        self.forms_manager = IRSFormsManager(tax_year)
        self.state_calculator = StateTaxCalculator(tax_year)
    
    async def calculate_complete_tax_return(self, return_id: int, tax_return: dict, force_recalculate: bool, db):
        # Get taxpayer data from database
        taxpayer_data = await self._build_taxpayer_data(return_id, db)
        
        # Calculate using the libraries
        result = self.tax_calculator.calculate_taxes(taxpayer_data)
        
        # Generate forms if needed
        if tax_return.get('generate_forms'):
            form_1040_pdf = self.forms_manager.generate_pdf(
                '1040', 
                result['federal'], 
                f'output/return_{return_id}_1040.pdf'
            )
            result['generated_forms'] = [form_1040_pdf]
        
        return result
```

## Development Setup

### 1. Clone and Setup
```bash
git clone <your-repo>
cd e-file-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt
```

### 2. Install Libraries in Development Mode
```bash
# Install each library in editable mode
pip install -e ./python-tax
pip install -e ./irs-forms  
pip install -e ./state-tax-calc

# Install main project dependencies
pip install -r requirements.txt
```

### 3. Run Tests
```bash
# Test individual libraries
cd python-tax && python -m pytest tests/
cd ../irs-forms && python -m pytest tests/
cd ../state-tax-calc && python -m pytest tests/

# Test main backend
cd ../
python -m pytest tests/
```

## Getting Official IRS Data

### IRS Form Downloads
The irs-forms library can automatically download current forms:

```python
from irs_forms import IRSFormsManager

forms_manager = IRSFormsManager()

# Update all forms from IRS
success = forms_manager.update_forms()

# Download specific form
forms_manager.downloader.download_form('1040', 2024)
```

### IRS API Access (For Production)
To access official IRS APIs, you need to:

1. **Apply for IRS API Access:**
   - Visit: https://www.irs.gov/tax-professionals/get-an-api-client-id
   - Complete IRS Form 8633 (Application to Participate in e-file)
   - Get approved as e-file provider

2. **IRS e-Services Registration:**
   - Register at: https://www.irs.gov/e-services
   - Apply for Transmitter Control Code (TCC)
   - Complete security requirements

3. **Testing Environment:**
   - Use IRS Acceptance Testing System (ATS)
   - Test e-file transmissions before production

### Third-Party API Integration
For development/testing, you can use third-party APIs:

```python
# Example TaxBandits API integration
import requests

class TaxBanditsAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://testapi.taxbandits.com"
    
    def validate_tin(self, tin, name):
        response = requests.post(
            f"{self.base_url}/v1.7.1/Business/TINMatching/RequestBySSN",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"TIN": tin, "TINName": name}
        )
        return response.json()
```

## Real-World Implementation Notes

### 1. Form Updates
- IRS typically releases updated forms in December/January
- Your system should check for updates automatically
- Implement form versioning to handle mid-year changes

### 2. State Tax Complexity
- Each state has unique rules and forms
- Some states follow federal AGI, others have modifications
- Multi-state scenarios require careful apportionment

### 3. Compliance Requirements
- Tax software must follow IRS security requirements
- Implement audit trails for all calculations
- Regular testing against known tax scenarios

### 4. Performance Considerations
- Cache frequently used tax tables
- Optimize for large batch calculations
- Consider async processing for complex returns

## Testing Strategy

### 1. Unit Tests
Test individual calculations against known scenarios:

```python
def test_single_filer_standard_deduction():
    calculator = TaxCalculator(2024)
    
    taxpayer_data = {
        'filing_status': 'single',
        'income_sources': {'w2_forms': [{'wages_tips_compensation': 50000}]},
        'deduction_type': 'standard'
    }
    
    result = calculator.calculate_federal_only(taxpayer_data)
    
    # Test known calculations
    assert result['agi'] == 50000
    assert result['taxable_income'] == 35400  # 50000 - 14600 standard deduction
    # Add more assertions for tax liability, etc.
```

### 2. Integration Tests
Test against actual tax scenarios with known correct answers.

### 3. Compliance Tests
Validate calculations against IRS test data and publications.

## Deployment

### 1. Package Distribution
```bash
# Build for distribution
python -m build

# Upload to private PyPI or artifact repository
twine upload dist/* --repository-url <your-private-pypi>
```

### 2. Docker Integration
```dockerfile
# Add to your Dockerfile
COPY python-tax/ ./python-tax/
COPY irs-forms/ ./irs-forms/
COPY state-tax-calc/ ./state-tax-calc/

RUN pip install ./python-tax ./irs-forms ./state-tax-calc
```

### 3. Production Deployment
- Use pinned versions in production
- Implement gradual rollout for library updates
- Monitor calculation accuracy and performance

## Contributing

### Adding New Forms
1. Create form class in appropriate library
2. Add field definitions and validation rules
3. Implement calculation methods
4. Add tests with known scenarios
5. Update documentation

### Adding New States
1. Research state-specific tax rules
2. Implement calculator in state-tax-calc
3. Add state forms and validation
4. Test against state tax publications

## License and Legal

- These libraries are for educational and development purposes
- Always validate calculations against official IRS publications
- Consider professional review for production tax software
- Comply with all applicable regulations for tax software

## Support and Documentation

- API documentation: Generated with Sphinx
- Examples: See `examples/` directory in each library
- Issues: Use GitHub issues for bug reports and features
- Contributing: See CONTRIBUTING.md for guidelines

---

**Note:** This implementation provides a solid foundation for tax calculations based on research into how companies like TurboTax operate. For production use, additional compliance, security, and accuracy measures would be required.
