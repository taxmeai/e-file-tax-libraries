"""
IRS Forms Library
Official IRS form definitions, field mappings, and PDF generation

This library provides:
- Official IRS form schemas and field definitions
- PDF form filling capabilities  
- Electronic filing XML generation
- Form validation and compliance checking
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from decimal import Decimal

from .forms import (
    BaseForm,
    Form1040,
    Form1040Schedule1,
    Form1040Schedule2, 
    Form1040Schedule3,
    Form1040ScheduleA,
    Form1040ScheduleB,
    Form1040ScheduleC,
    Form1040ScheduleD,
    Form1040ScheduleE,
    Form1040ScheduleF,
    Form8812,
    Form8889,
    Form8959,
    Form8995,
    FormW2,
    Form1099INT,
    Form1099DIV,
    Form1099MISC,
    Form1099NEC,
    Form1099G,
    Form1099R,
    Form1098
)

from .generators import (
    PDFFormGenerator,
    XMLGenerator,
    EFileGenerator
)

from .validators import (
    FormValidator,
    IRSValidator,
    ComplianceChecker
)

from .downloaders import (
    IRSFormDownloader,
    FormUpdater,
    SchemaDownloader
)

from .constants import (
    CURRENT_TAX_YEAR,
    IRS_FORM_URLS,
    SUPPORTED_FORMS,
    FIELD_MAPPINGS,
    VALIDATION_RULES
)

__version__ = "1.0.0"
__author__ = "E-File Backend Team"
__description__ = "Official IRS Forms Processing Library"

class IRSFormsManager:
    """
    Main interface for IRS forms management
    
    This class provides a unified interface to:
    - Load and manage IRS form definitions
    - Generate PDFs from form data
    - Create e-file XML documents
    - Validate form data against IRS requirements
    - Download latest forms from IRS
    """
    
    def __init__(self, tax_year: int = CURRENT_TAX_YEAR, cache_dir: str = None):
        self.tax_year = tax_year
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / '.irs_forms_cache'
        self.cache_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.pdf_generator = PDFFormGenerator(self.cache_dir)
        self.xml_generator = XMLGenerator(tax_year)
        self.efile_generator = EFileGenerator(tax_year)
        self.validator = IRSValidator(tax_year)
        self.downloader = IRSFormDownloader(self.cache_dir)
        self.form_updater = FormUpdater(self.cache_dir)
        
        # Load form definitions
        self._load_form_definitions()
    
    def _load_form_definitions(self):
        """Load IRS form definitions from cache or download if needed"""
        definitions_file = self.cache_dir / f'form_definitions_{self.tax_year}.json'
        
        if not definitions_file.exists():
            self.update_forms()
        
        with open(definitions_file, 'r') as f:
            self.form_definitions = json.load(f)
    
    def get_form(self, form_name: str) -> BaseForm:
        """Get a specific IRS form class"""
        form_classes = {
            '1040': Form1040,
            '1040Schedule1': Form1040Schedule1,
            '1040Schedule2': Form1040Schedule2,
            '1040Schedule3': Form1040Schedule3,
            '1040ScheduleA': Form1040ScheduleA,
            '1040ScheduleB': Form1040ScheduleB,
            '1040ScheduleC': Form1040ScheduleC,
            '1040ScheduleD': Form1040ScheduleD,
            '1040ScheduleE': Form1040ScheduleE,
            '1040ScheduleF': Form1040ScheduleF,
            '8812': Form8812,
            '8889': Form8889,
            '8959': Form8959,
            '8995': Form8995,
            'W2': FormW2,
            '1099-INT': Form1099INT,
            '1099-DIV': Form1099DIV,
            '1099-MISC': Form1099MISC,
            '1099-NEC': Form1099NEC,
            '1099-G': Form1099G,
            '1099-R': Form1099R,
            '1098': Form1098
        }
        
        if form_name not in form_classes:
            raise ValueError(f"Unsupported form: {form_name}")
        
        return form_classes[form_name](self.tax_year)
    
    def validate_form_data(self, form_name: str, form_data: dict) -> dict:
        """Validate form data against IRS requirements"""
        form = self.get_form(form_name)
        return self.validator.validate_form(form, form_data)
    
    def generate_pdf(self, form_name: str, form_data: dict, output_path: str) -> str:
        """Generate filled PDF form"""
        form = self.get_form(form_name)
        return self.pdf_generator.generate(form, form_data, output_path)
    
    def generate_efile_xml(self, return_data: dict) -> str:
        """Generate e-file XML for IRS submission"""
        return self.efile_generator.generate_return_xml(return_data)
    
    def update_forms(self) -> bool:
        """Download and update IRS forms from official sources"""
        try:
            return self.form_updater.update_all_forms(self.tax_year)
        except Exception as e:
            print(f"Error updating forms: {e}")
            return False
    
    def list_supported_forms(self) -> List[str]:
        """Get list of supported form names"""
        return list(SUPPORTED_FORMS.keys())
    
    def get_form_fields(self, form_name: str) -> List[str]:
        """Get list of fields for a specific form"""
        form = self.get_form(form_name)
        return form.get_field_names()
    
    def get_form_requirements(self, form_name: str) -> dict:
        """Get requirements and validation rules for a form"""
        if form_name in self.form_definitions:
            return self.form_definitions[form_name].get('requirements', {})
        return {}

class FormDataManager:
    """Helper class for managing form data"""
    
    def __init__(self, forms_manager: IRSFormsManager):
        self.forms_manager = forms_manager
    
    def populate_form_from_interview(self, form_name: str, interview_data: dict) -> dict:
        """Convert interview data to form field data"""
        form = self.forms_manager.get_form(form_name)
        return form.populate_from_interview(interview_data)
    
    def calculate_form_fields(self, form_name: str, input_data: dict) -> dict:
        """Calculate computed fields for a form"""
        form = self.forms_manager.get_form(form_name)
        return form.calculate_fields(input_data)
    
    def get_form_summary(self, form_name: str, form_data: dict) -> dict:
        """Get summary information for a completed form"""
        form = self.forms_manager.get_form(form_name)
        return form.get_summary(form_data)

# Export main interfaces
__all__ = [
    'IRSFormsManager',
    'FormDataManager',
    'BaseForm',
    'Form1040',
    'Form1040Schedule1',
    'Form1040Schedule2',
    'Form1040Schedule3', 
    'Form1040ScheduleA',
    'Form1040ScheduleB',
    'Form1040ScheduleC',
    'Form1040ScheduleD',
    'Form1040ScheduleE',
    'Form1040ScheduleF',
    'Form8812',
    'Form8889',
    'Form8959',
    'Form8995',
    'FormW2',
    'Form1099INT',
    'Form1099DIV',
    'Form1099MISC',
    'Form1099NEC',
    'Form1099G',
    'Form1099R',
    'Form1098',
    'PDFFormGenerator',
    'XMLGenerator',
    'EFileGenerator',
    'FormValidator',
    'IRSValidator',
    'ComplianceChecker',
    'IRSFormDownloader',
    'FormUpdater',
    'SchemaDownloader',
    'CURRENT_TAX_YEAR',
    'IRS_FORM_URLS',
    'SUPPORTED_FORMS',
    'FIELD_MAPPINGS',
    'VALIDATION_RULES'
]

# Default instance for easy access
default_forms_manager = IRSFormsManager()

def get_form(form_name: str) -> BaseForm:
    """Convenience function to get a form using default manager"""
    return default_forms_manager.get_form(form_name)

def validate_form(form_name: str, form_data: dict) -> dict:
    """Convenience function to validate form data"""
    return default_forms_manager.validate_form_data(form_name, form_data)

def generate_pdf(form_name: str, form_data: dict, output_path: str) -> str:
    """Convenience function to generate PDF"""
    return default_forms_manager.generate_pdf(form_name, form_data, output_path)
