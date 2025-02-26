#!/usr/bin/env python3
import json
import sys
import urllib.request
import urllib.parse
import urllib.error
import os
import re
import argparse

class SecureShareCLI:
    def __init__(self):
        self.api_url = "https://api.secureshare.dev"

        self.secret_patterns = {
    'API_KEY': r'(?:api[_-]?key|apikey|key|api)["\']?\s*(?::|=)\s*["\']?([a-zA-Z0-9_\-]{8,})["\']?',
    'PASSWORD': r'(?:password|passwd|pwd|psw|psswd|pass)["\']?\s*(?::|=)\s*["\']?([^"\'\s]+)["\']?',
    'TOKEN': r'(?:token|jwt|bearer|auth)["\']?\s*(?::|=)\s*["\']?([a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+)["\']?',
    'SECRET_KEY': r'(?:secret[_-]?key|secretkey|secret)["\']?\s*(?::|=)\s*["\']?([a-zA-Z0-9_\-]{8,})["\']?',
    'ACCESS_KEY': r'(?:access[_-]?key|access)["\']?\s*(?::|=)\s*["\']?([a-zA-Z0-9_\-]{8,})["\']?',
    'PRIVATE_KEY': r'(?:private[_-]?key|private)["\']?\s*(?::|=)\s*["\']?([a-zA-Z0-9_\-/+]{20,}={0,2})["\']?',
    'JWT': r'eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}',
    'INLINE_API_KEY': r'[\?&](?:api[_-]?key|key|apikey|token)=([a-zA-Z0-9_\-]{8,})'
}


    def detect_secrets(self, code):
        secrets = []
        for line_num, line in enumerate(code.split('\n'), 1):
            # Skip lines that are defining the patterns themselves
            if self.is_pattern_definition(line):
                continue
                
            for secret_type, pattern in self.secret_patterns.items():
                for match in re.finditer(pattern, line, re.IGNORECASE):
                    value = match.group(1) if match.groups() else match.group(0)
                    if value:
                        start = match.start(1) if match.groups() else match.start(0)
                        end = match.end(1) if match.groups() else match.end(0)
                        secrets.append({
                            'type': secret_type,
                            'line': line_num,
                            'value': value,
                            'start': start,
                            'end': end
                        })
        return secrets

    def is_pattern_definition(self, line):
        # More accurate way to detect pattern definitions in the code itself
        return "'secret_patterns'" in line or "self.secret_patterns" in line

    def redact_secrets(self, code, secrets):
        lines = code.split('\n')
        # Sort secrets in reverse order to avoid offsetting positions when redacting
        secrets.sort(key=lambda x: (x['line'], -x['start']))
        
        for secret in secrets:
            line_num = secret['line'] - 1
            if 0 <= line_num < len(lines):  # Check if line exists
                line = lines[line_num]
                if line:
                    lines[line_num] = line[:secret['start']] + '[REDACTED]' + line[secret['end']:]
        return '\n'.join(lines)

    def share_code(self, code, title="Untitled Snippet", language="text"):
        try:
            secrets = self.detect_secrets(code)
            redacted_code = self.redact_secrets(code, secrets)
            
            data = {
                "content": redacted_code,
                "title": title,
                "language": language
            }

            headers = {"Content-Type": "application/json"}
            req = urllib.request.Request(
                f"{self.api_url}/share",
                data=json.dumps(data).encode('utf-8'),
                headers=headers,
                method='POST'
            )
            
            with urllib.request.urlopen(req) as response:
                response_data = response.read().decode('utf-8')
                if response.status == 201 and response_data:
                    try:
                        result = json.loads(response_data)
                        if 'share_url' in result:
                            share_url = result['share_url']
                            
                            if secrets:
                                print("\nWarning: Sensitive information detected!")
                                print("The following secrets were found and redacted:")
                                for secret in secrets:
                                    print(f"- {secret['type']} on line {secret['line']}")
                            
                            print("\nCode shared successfully!")
                            print(f"Share URL: {share_url}")
                            return True
                        else:
                            print("Error: API response missing share URL")
                            return False
                    except json.JSONDecodeError:
                        print("Error: Failed to parse API response")
                        return False
                else:
                    print(f"Error: Failed to share code (Status: {response.status})")
                    return False
        except urllib.error.URLError as e:
            print(f"Error: API connection failed - {str(e)}")
            return False
        except Exception as e:
            print(f"Error: Failed to share code - {str(e)}")
            return False

def main():
    parser = argparse.ArgumentParser(description='SecShare CLI - Share code snippets securely')
    parser.add_argument('file', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                      help='File containing code to share (reads from stdin if not specified)')
    parser.add_argument('-t', '--title', default="Untitled Snippet",
                      help='Title for the code snippet')
    parser.add_argument('-l', '--language', default="text",
                      help='Programming language of the code snippet')
    
    args = parser.parse_args()
    
    try:
        code = args.file.read()
        cli = SecureShareCLI()
        cli.share_code(code, args.title, args.language)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        if args.file is not sys.stdin:
            args.file.close()

if __name__ == "__main__":
    main()