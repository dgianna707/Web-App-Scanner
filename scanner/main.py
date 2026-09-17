import argparse
import sys
from scanner.checks.core import run_all_checks
from scanner.reporter import format_scan_result, format_scan_result_markdown
"""
main.py — CLI entrypoint for the Web App Security Scanner

Parses command-line arguments, runs all security checks against a target URL,
and outputs a formatted report (JSON or Markdown). Exits with code 1 if any
CRITICAL findings are found, making it compatible with CI/CD pipelines.

Usage:
    python -m scanner.main --target https://example.com --env prod
    python -m scanner.main --target https://example.com --format json --output report.json
"""

def main():
    parser = argparse.ArgumentParser(
        description="Cloud-aware web application security scanner"
    )
    parser.add_argument("--target", required=True, help="Target URL to scan")
    parser.add_argument(
        "--env",
        default="prod",
        choices=["dev", "staging", "prod"],
        help="Environment label — affects severity context",
    )
    parser.add_argument(
        "--format",
        default="markdown",
        choices=["json", "markdown"],
        help="Output format",
    )
    parser.add_argument("--output", help="Write report to a file instead of stdout")
    args = parser.parse_args()

    print(f"[*] Scanning {args.target} ({args.env})...")
    result = run_all_checks(args.target, args.env)

    report = format_scan_result(result) if args.format == "json" else format_scan_result_markdown(result)

    if args.output:
        with open(args.output, "w") as f:
            f.write(report)
        print(f"[+] Report written to {args.output}")
    else:
        print(report)

    if result.overall_risk == "CRITICAL":
        sys.exit(1)


if __name__ == "__main__":
    main()