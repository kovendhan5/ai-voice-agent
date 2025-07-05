#!/usr/bin/env python3
"""
🔒 SECURITY AUDIT SCRIPT
========================
Scans for hardcoded tokens and prevents security leaks
Runs automatically before any git commits
========================
"""

import os
import re
import sys
from pathlib import Path

class SecurityAuditor:
    """Security auditor to prevent token leaks"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.violations = []
        
        # Patterns that indicate security violations
        self.token_patterns = [
            r'hf_[A-Za-z0-9]{34}',  # HuggingFace tokens
            r'sk-[A-Za-z0-9]{48}',  # OpenAI API keys
            r'AIza[A-Za-z0-9]{35}', # Google API keys
            r'AKIA[0-9A-Z]{16}',    # AWS Access Keys
            r'xoxb-[0-9]{12}-[0-9]{12}-[A-Za-z0-9]{24}',  # Slack tokens
        ]
        
        # Files that should be checked
        self.file_patterns = ['*.py', '*.md', '*.txt', '*.json']
        
        # Files/directories to skip
        self.skip_patterns = [
            '__pycache__',
            '.git',
            'venv',
            '.env.example',  # This is safe
        ]
    
    def should_skip_file(self, filepath):
        """Check if file should be skipped"""
        str_path = str(filepath)
        
        # Skip if in skip patterns
        for pattern in self.skip_patterns:
            if pattern in str_path:
                return True
        
        # Skip binary files
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                f.read(100)  # Try to read a bit
        except (UnicodeDecodeError, PermissionError):
            return True
        
        return False
    
    def scan_file(self, filepath):
        """Scan a single file for security violations"""
        if self.should_skip_file(filepath):
            return
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for token patterns
            for pattern in self.token_patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    self.violations.append({
                        'file': filepath,
                        'line': line_num,
                        'type': 'token_pattern',
                        'content': match.group(),
                        'severity': 'HIGH'
                    })
                        
        except Exception as e:
            print(f"⚠️ Error scanning {filepath}: {e}")
    
    def scan_directory(self, directory=None):
        """Scan entire directory for security violations"""
        if directory is None:
            directory = self.project_root
        
        print(f"🔍 Scanning directory: {directory}")
        
        for root, dirs, files in os.walk(directory):
            # Skip directories we don't want to scan
            dirs[:] = [d for d in dirs if not any(skip in d for skip in self.skip_patterns)]
            
            for file in files:
                if any(file.endswith(ext.replace('*', '')) for ext in self.file_patterns):
                    filepath = Path(root) / file
                    self.scan_file(filepath)
    
    def report_violations(self):
        """Report all security violations"""
        if not self.violations:
            print("✅ No security violations found!")
            return True
        
        print(f"\n🚨 SECURITY VIOLATIONS FOUND: {len(self.violations)}")
        print("=" * 60)
        
        for violation in self.violations:
            print(f"🔴 {violation['file']}:{violation['line']}")
            print(f"   Type: {violation['type']}")
            print(f"   Content: {violation['content'][:50]}...")
            print()
        
        print("❌ SECURITY AUDIT FAILED!")
        return False

def main():
    """Main security audit function"""
    print("🔒 ORPHEUS PROJECT SECURITY AUDIT")
    print("=" * 50)
    
    auditor = SecurityAuditor()
    auditor.scan_directory()
    is_safe = auditor.report_violations()
    
    if is_safe:
        print("\n✅ SECURITY AUDIT PASSED!")
        print("🔒 Project is secure for commit")
        return 0
    else:
        print("\n❌ SECURITY AUDIT FAILED!")
        print("🚨 Fix security issues before committing")
        return 1

if __name__ == "__main__":
    sys.exit(main())
