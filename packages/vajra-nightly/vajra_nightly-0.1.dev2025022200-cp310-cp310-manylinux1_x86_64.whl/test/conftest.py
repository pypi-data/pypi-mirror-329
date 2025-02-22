from typing import Dict, List, Tuple

from pytest import Config, TestReport
from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({"success": "green", "failure": "red", "skip": "yellow"})
console = Console(theme=custom_theme, force_terminal=True)

_pytest_config: Config | None = None


def pytest_configure(config: Config) -> None:
    """Pytest hook to capture config object."""

    global _pytest_config
    _pytest_config = config


def pytest_runtest_logreport(report: TestReport) -> None:
    """Pytest hook to customize test execution output."""
    if not _pytest_config:
        raise RuntimeError("pytest_configure was not called")

    if report.when == "call":
        if report.outcome == "passed":
            console.print(f"[success]✔ {report.nodeid}[/success]")
        elif report.outcome == "failed":
            console.print(f"[failure]✘ {report.nodeid}[/failure]")
        elif report.outcome == "skipped":
            console.print(f"[skip]s {report.nodeid}[/skip]")


def pytest_report_teststatus(
    report: TestReport,
) -> Tuple[str, str, Tuple[str, Dict[str, bool]]]:
    """Pytest hook to customize test status characters."""
    if report.when == "call":
        if report.outcome == "passed":
            return "pass", "✔", ("success", {"bold": True})
        elif report.outcome == "failed":
            return "fail", "✘", ("failure", {"bold": True})
        elif report.outcome == "skipped":
            return "skipped", "s", ("skip", {"bold": True})
    return "", "", ("", {})  # default return for other phases


def pytest_terminal_summary(terminalreporter) -> None:
    """Pytest hook to add customized terminal summary report."""
    markexpr = terminalreporter.config.option.markexpr

    console.rule(f"[bold magenta]Report for mark '{markexpr}' start[/bold magenta]")

    passed_reports: List[TestReport] = terminalreporter.stats.get("pass", [])
    failed_reports: List[TestReport] = terminalreporter.stats.get("fail", [])
    skipped_reports: List[TestReport] = terminalreporter.stats.get("skip", [])

    passed_count: int = len(passed_reports)
    failed_count: int = len(failed_reports)
    skipped_count: int = len(skipped_reports)

    total_tests: int = 0
    for outcome_list in terminalreporter.stats.values():
        for report in outcome_list:
            if isinstance(report, TestReport) and report.when == "call":
                total_tests += 1

    console.print(f"Total tests run: {total_tests}")
    console.print(f"[success]Passed: {passed_count}[/success]")
    console.print(f"[failure]Failed: {failed_count}[/failure]")
    console.print(f"[skip]Skipped: {skipped_count}[/skip]")

    # detailed list of test results
    if passed_count > 0:
        console.print("\n[success]Passed Tests:[/success]")
        for report in passed_reports:
            console.print(f"  [success]✔ {report.nodeid}[/success]")

    if failed_count > 0:
        console.print("\n[failure]Failed Tests:[/failure]")
        for report in failed_reports:
            console.print(f"  [failure]✘ {report.nodeid}[/failure]")

    if skipped_count > 0:
        console.print("\n[skip]Skipped Tests:[/skip]")
        for report in skipped_reports:
            console.print(f"  [skip]s {report.nodeid}[/skip]")

    if markexpr:
        console.rule(f"[bold magenta]Report for mark '{markexpr}' end[/bold magenta]")
    else:
        console.rule("[bold magenta]Regression report end[/bold magenta]")
