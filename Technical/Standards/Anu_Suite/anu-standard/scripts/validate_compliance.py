#!/usr/bin/env python3
"""
Anu Standard Compliance Validator

Validates data projects against the Anu Standard for data provenance and quality.

Usage:
    python validate_compliance.py [project_path] [--verbose] [--json]
    
Examples:
    python validate_compliance.py .
    python validate_compliance.py /path/to/project --verbose
    python validate_compliance.py . --json > compliance_report.json
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple


@dataclass
class ValidationResult:
    """Result of a single validation check."""
    check_name: str
    passed: bool
    message: str
    severity: str = "info"  # info, warning, error
    details: Optional[Dict] = None


@dataclass 
class ComplianceReport:
    """Full compliance report for a project."""
    project_path: str
    validation_date: str
    total_checks: int = 0
    passed: int = 0
    failed: int = 0
    warnings: int = 0
    results: List[ValidationResult] = field(default_factory=list)
    datasets: List[str] = field(default_factory=list)
    figures: List[str] = field(default_factory=list)
    
    @property
    def compliance_score(self) -> float:
        if self.total_checks == 0:
            return 0.0
        return (self.passed / self.total_checks) * 100
    
    @property
    def status(self) -> str:
        if self.failed > 0:
            return "ISSUES FOUND"
        elif self.warnings > 0:
            return "VALIDATED WITH WARNINGS"
        else:
            return "ANU STANDARD COMPLIANT"


class AnuStandardValidator:
    """Validates projects against the Anu Standard."""
    
    def __init__(self, project_path: str, verbose: bool = False):
        self.project_path = Path(project_path).resolve()
        self.verbose = verbose
        self.report = ComplianceReport(
            project_path=str(self.project_path),
            validation_date=datetime.now().isoformat()
        )
    
    def log(self, message: str) -> None:
        """Log message if verbose mode is enabled."""
        if self.verbose:
            print(f"[INFO] {message}")
    
    def add_result(self, result: ValidationResult) -> None:
        """Add a validation result to the report."""
        self.report.results.append(result)
        self.report.total_checks += 1
        
        if result.passed:
            self.report.passed += 1
        elif result.severity == "warning":
            self.report.warnings += 1
        else:
            self.report.failed += 1
    
    def validate_directory_structure(self) -> None:
        """Check for required directory structure."""
        self.log("Checking directory structure...")
        
        required_dirs = ["Inputs", "Technical", "Outputs"]
        
        for dir_name in required_dirs:
            dir_path = self.project_path / dir_name
            exists = dir_path.exists() and dir_path.is_dir()
            
            self.add_result(ValidationResult(
                check_name=f"directory_{dir_name.lower()}",
                passed=exists,
                message=f"Required directory '{dir_name}/' {'exists' if exists else 'missing'}",
                severity="error" if not exists else "info"
            ))
    
    def find_datasets(self) -> List[str]:
        """Find all dataset identifiers in the project."""
        datasets = set()
        
        # Look for DPR files
        for dpr_file in self.project_path.rglob("*_DPR.md"):
            # Extract dataset ID from filename
            match = re.match(r"(.+)_DPR\.md$", dpr_file.name)
            if match:
                datasets.add(match.group(1))
        
        # Look for references in transformation log
        transform_log = self.find_transformation_log()
        if transform_log:
            try:
                with open(transform_log, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for t in data.get("transformations", []):
                    for ds in t.get("datasets_affected", []):
                        datasets.add(ds)
            except (json.JSONDecodeError, KeyError):
                pass
        
        self.report.datasets = sorted(datasets)
        return self.report.datasets
    
    def find_figures(self) -> List[str]:
        """Find all figure identifiers in the project."""
        figures = set()
        
        # Look for FPR files
        for fpr_file in self.project_path.rglob("*_FPR.md"):
            match = re.match(r"(.+)_FPR\.md$", fpr_file.name)
            if match:
                figures.add(match.group(1))
        
        self.report.figures = sorted(figures)
        return self.report.figures
    
    def find_transformation_log(self) -> Optional[Path]:
        """Find the transformation log file."""
        for log_file in self.project_path.rglob("TRANSFORMATION_LOG.json"):
            return log_file
        return None
    
    def validate_transformation_log(self) -> None:
        """Validate the transformation log exists and is well-formed."""
        self.log("Checking transformation log...")
        
        log_file = self.find_transformation_log()
        
        if not log_file:
            self.add_result(ValidationResult(
                check_name="transformation_log_exists",
                passed=False,
                message="TRANSFORMATION_LOG.json not found",
                severity="warning"
            ))
            return
        
        self.add_result(ValidationResult(
            check_name="transformation_log_exists",
            passed=True,
            message=f"TRANSFORMATION_LOG.json found at {log_file.relative_to(self.project_path)}"
        ))
        
        # Validate JSON structure
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check required fields
            has_project = "project" in data
            has_transformations = "transformations" in data
            
            self.add_result(ValidationResult(
                check_name="transformation_log_structure",
                passed=has_project and has_transformations,
                message="Transformation log has valid structure" if (has_project and has_transformations) 
                        else "Transformation log missing required fields",
                severity="error" if not (has_project and has_transformations) else "info"
            ))
            
            # Validate each transformation entry
            required_fields = ["transform_id", "operation", "datasets_affected"]
            for i, t in enumerate(data.get("transformations", [])):
                missing = [f for f in required_fields if f not in t]
                if missing:
                    self.add_result(ValidationResult(
                        check_name=f"transformation_{t.get('transform_id', f'index_{i}')}",
                        passed=False,
                        message=f"Transformation missing fields: {', '.join(missing)}",
                        severity="warning"
                    ))
                    
        except json.JSONDecodeError as e:
            self.add_result(ValidationResult(
                check_name="transformation_log_valid_json",
                passed=False,
                message=f"TRANSFORMATION_LOG.json is not valid JSON: {e}",
                severity="error"
            ))
    
    def validate_dpr_files(self) -> None:
        """Validate that all datasets have DPR files."""
        self.log("Checking Data Provenance Records...")
        
        datasets = self.find_datasets()
        
        if not datasets:
            self.add_result(ValidationResult(
                check_name="datasets_found",
                passed=True,
                message="No datasets found (this may be expected for theoretical projects)",
                severity="info"
            ))
            return
        
        for dataset_id in datasets:
            # Look for DPR file
            dpr_found = any(self.project_path.rglob(f"{dataset_id}_DPR.md"))
            
            self.add_result(ValidationResult(
                check_name=f"dpr_{dataset_id}",
                passed=dpr_found,
                message=f"DPR for {dataset_id}: {'found' if dpr_found else 'MISSING'}",
                severity="error" if not dpr_found else "info"
            ))
    
    def validate_fpr_files(self) -> None:
        """Validate that all figures have FPR files."""
        self.log("Checking Figure Provenance Records...")
        
        figures = self.find_figures()
        
        if not figures:
            self.add_result(ValidationResult(
                check_name="figures_found",
                passed=True,
                message="No figures found (this may be expected for data-only projects)",
                severity="info"
            ))
            return
        
        for figure_id in figures:
            fpr_found = any(self.project_path.rglob(f"{figure_id}_FPR.md"))
            
            self.add_result(ValidationResult(
                check_name=f"fpr_{figure_id}",
                passed=fpr_found,
                message=f"FPR for {figure_id}: {'found' if fpr_found else 'MISSING'}",
                severity="error" if not fpr_found else "info"
            ))
    
    def validate_investigation_docs(self) -> None:
        """Check for module investigation documents."""
        self.log("Checking investigation documents...")
        
        investigation_files = list(self.project_path.rglob("*_INVESTIGATION.md"))
        
        self.add_result(ValidationResult(
            check_name="investigation_docs",
            passed=len(investigation_files) > 0,
            message=f"Found {len(investigation_files)} investigation document(s)",
            severity="info" if len(investigation_files) > 0 else "warning",
            details={"files": [str(f.relative_to(self.project_path)) for f in investigation_files]}
        ))
    
    def validate_data_files(self) -> None:
        """Check for data files and basic validation."""
        self.log("Checking data files...")
        
        csv_files = list(self.project_path.rglob("*.csv"))
        json_files = list(self.project_path.rglob("*.json"))
        
        # Exclude transformation log from JSON count
        json_files = [f for f in json_files if "TRANSFORMATION_LOG" not in f.name]
        
        self.add_result(ValidationResult(
            check_name="data_files_exist",
            passed=len(csv_files) > 0 or len(json_files) > 0,
            message=f"Found {len(csv_files)} CSV files and {len(json_files)} JSON data files",
            severity="info"
        ))
    
    def run_all_checks(self) -> ComplianceReport:
        """Run all validation checks."""
        self.log(f"Starting Anu Standard validation for: {self.project_path}")
        
        self.validate_directory_structure()
        self.validate_transformation_log()
        self.validate_dpr_files()
        self.validate_fpr_files()
        self.validate_investigation_docs()
        self.validate_data_files()
        
        self.log(f"Validation complete: {self.report.status}")
        return self.report
    
    def print_report(self) -> None:
        """Print a human-readable report."""
        print("\n" + "=" * 60)
        print("ANU STANDARD COMPLIANCE REPORT")
        print("=" * 60)
        print(f"\nProject: {self.report.project_path}")
        print(f"Date: {self.report.validation_date}")
        print(f"\nStatus: {self.report.status}")
        print(f"Compliance Score: {self.report.compliance_score:.1f}%")
        print(f"\nTotal Checks: {self.report.total_checks}")
        print(f"  Passed: {self.report.passed}")
        print(f"  Failed: {self.report.failed}")
        print(f"  Warnings: {self.report.warnings}")
        
        if self.report.datasets:
            print(f"\nDatasets Found: {len(self.report.datasets)}")
            for ds in self.report.datasets:
                print(f"  - {ds}")
        
        if self.report.figures:
            print(f"\nFigures Found: {len(self.report.figures)}")
            for fig in self.report.figures:
                print(f"  - {fig}")
        
        # Show failed checks
        failed = [r for r in self.report.results if not r.passed and r.severity == "error"]
        if failed:
            print("\n" + "-" * 40)
            print("FAILED CHECKS:")
            for r in failed:
                print(f"  [X] {r.check_name}: {r.message}")
        
        # Show warnings
        warnings = [r for r in self.report.results if not r.passed and r.severity == "warning"]
        if warnings:
            print("\n" + "-" * 40)
            print("WARNINGS:")
            for r in warnings:
                print(f"  [!] {r.check_name}: {r.message}")
        
        print("\n" + "=" * 60)
    
    def to_json(self) -> str:
        """Export report as JSON."""
        return json.dumps({
            "project_path": self.report.project_path,
            "validation_date": self.report.validation_date,
            "status": self.report.status,
            "compliance_score": self.report.compliance_score,
            "total_checks": self.report.total_checks,
            "passed": self.report.passed,
            "failed": self.report.failed,
            "warnings": self.report.warnings,
            "datasets": self.report.datasets,
            "figures": self.report.figures,
            "results": [
                {
                    "check_name": r.check_name,
                    "passed": r.passed,
                    "message": r.message,
                    "severity": r.severity,
                    "details": r.details
                }
                for r in self.report.results
            ]
        }, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Validate a project against the Anu Standard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python validate_compliance.py .
    python validate_compliance.py /path/to/project --verbose
    python validate_compliance.py . --json > report.json
        """
    )
    parser.add_argument(
        "project_path",
        nargs="?",
        default=".",
        help="Path to the project directory (default: current directory)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output report as JSON"
    )
    
    args = parser.parse_args()
    
    validator = AnuStandardValidator(args.project_path, verbose=args.verbose)
    validator.run_all_checks()
    
    if args.json:
        print(validator.to_json())
    else:
        validator.print_report()
    
    # Exit with error code if there are failures
    sys.exit(1 if validator.report.failed > 0 else 0)


if __name__ == "__main__":
    main()
