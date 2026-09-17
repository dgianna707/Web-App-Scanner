import json
from scanner.models import ScanResult

# handles formatting the scan results into a JSON string for output
def format_scan_result(scan_result: ScanResult) -> str:
    result_dict = {
        "target": scan_result.target,
        "overall_risk": scan_result.overall_risk,

        "findings": [
            {
                "id": finding.id,
                "severity": finding.severity,
                "description": finding.description,
                "evidence": finding.evidence,
                "remediation": finding.remediation,
            }
            for finding in scan_result.findings
        ],
        
    }
        
    if not scan_result.findings:
       result_dict["findings"] = "No issues found within this scan."
           

    return json.dumps(result_dict, indent=4)


def format_scan_result_markdown(scan_result: ScanResult) -> str:
    lines = [
        "# Security Scan Report",
        f"**Target:** {scan_result.target}",
        f"**Overall Risk:** {scan_result.overall_risk}",
        f"**Findings:** {len(scan_result.findings)}",
        "",
        "---",
        "",
    ]

    if not scan_result.findings:
        lines.append("No issues found within this scan.")
        return "\n".join(lines)

    for finding in scan_result.findings:
        lines += [
            f"### [{finding.severity}] {finding.id}",
            f"**Description:** {finding.description}",
            f"**Evidence:** {finding.evidence}",
            f"**Remediation:** {finding.remediation}",
            "",
        ]

    return "\n".join(lines)