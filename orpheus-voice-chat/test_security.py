from security_audit import SecurityAuditor

auditor = SecurityAuditor()
auditor.scan_directory()
result = auditor.report_violations()
print("Security scan complete!")
