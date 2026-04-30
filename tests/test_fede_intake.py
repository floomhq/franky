import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("fede_intake", ROOT / "scripts" / "fede_intake.py")
fede_intake = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules["fede_intake"] = fede_intake
SPEC.loader.exec_module(fede_intake)


def test_domain_detection_sales():
    assert fede_intake.choose_domain("CRM notes and sales emails") == "sales"


def test_domain_detection_support():
    assert fede_intake.choose_domain("support tickets and customer replies") == "support"


def test_blank_input_returns_menu():
    assert fede_intake.choose_domain("") is None
    assert "Fede Zero-Input Intake" in fede_intake.starter_menu()


def test_report_contains_template_and_prompt():
    report = fede_intake.build_report(fede_intake.DOMAINS["finance"], "expenses")
    assert "First Output Template" in report
    assert "Expense Categorization Draft" in report
    assert "First Prompt" in report


def test_all_domains_have_workflows():
    assert {"sales", "ops", "support", "recruiting", "finance", "admin"} <= set(fede_intake.DOMAINS)
    assert all(domain.workflows for domain in fede_intake.DOMAINS.values())
