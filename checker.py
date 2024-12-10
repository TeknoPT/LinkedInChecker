#!/usr/bin/env python3

import os
import re
import argparse
import csv
from pathlib import Path

# Define the patterns to search for
PATTERNS = {
    "eval()": re.compile(r'\beval\s*\('),
    "new Function()": re.compile(r'\bnew\s+Function\s*\('),
    "setTimeout() with string": re.compile(r'\bsetTimeout\s*\(\s*["\']'),
    "setInterval() with string": re.compile(r'\bsetInterval\s*\(\s*["\']'),
    "innerHTML": re.compile(r'\binnerHTML\s*='),  # Assignment to innerHTML
    "document.write()": re.compile(r'\bdocument\.write\s*\('),
    "XMLHttpRequest": re.compile(r'\bXMLHttpRequest\b'),
    "fetch()": re.compile(r'\bfetch\s*\('),
    "localStorage": re.compile(r'\blocalStorage\b'),
    "sessionStorage": re.compile(r'\bsessionStorage\b'),
    "require() with variable": re.compile(r'\brequire\s*\(\s*\w+\s*\)'),  # Potential dynamic require
    "child_process.exec()": re.compile(r'\bexec\s*\('),
    "child_process.spawn()": re.compile(r'\bspawn\s*\('),
    "child_process.execFile()": re.compile(r'\bexecFile\s*\('),
    "fs module usage": re.compile(r'\bfs\b'),
    "process": re.compile(r'\bprocess\b'),
    "vm module usage": re.compile(r'\bvm\b'),
    "importScripts()": re.compile(r'\bimportScripts\s*\('),
    "postMessage()": re.compile(r'\bpostMessage\s*\('),
}

# File extensions to scan
FILE_EXTENSIONS = {'.js', '.jsx', '.ts', '.tsx'}

def scan_file(file_path, patterns):
    matches = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for lineno, line in enumerate(f, start=1):
                for name, pattern in patterns.items():
                    if pattern.search(line):
                        matches.append((name, lineno, line.strip()))
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return matches

def scan_directory(directory, patterns, exclude_dirs=None):
    all_matches = []
    exclude_dirs = exclude_dirs or set()
    for root, dirs, files in os.walk(directory):
        # Modify dirs in-place to skip excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if Path(file).suffix in FILE_EXTENSIONS:
                file_path = os.path.join(root, file)
                file_matches = scan_file(file_path, patterns)
                for match in file_matches:
                    all_matches.append((file_path, *match))
    return all_matches

def print_report(matches):
    if not matches:
        print("No potentially dangerous JavaScript commands found.")
        return

    print(f"\n{'File':<60} {'Line':<6} {'Issue':<30} {'Code'}")
    print('-' * 120)
    for file_path, issue, lineno, code in matches:
        # Truncate file path if too long
        display_path = (file_path[:57] + '...') if len(file_path) > 60 else file_path
        print(f"{display_path:<60} {lineno:<6} {issue:<30} {code}")
    print(f"\nTotal Issues Found: {len(matches)}")

def export_to_csv(matches, csv_file):
    if not matches:
        print("No issues to export to CSV.")
        return

    # Define CSV headers
    headers = ['File', 'Line', 'Issue', 'Code']

    try:
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for file_path, issue, lineno, code in matches:
                writer.writerow([file_path, lineno, issue, code])
        print(f"Report successfully exported to {csv_file}")
    except Exception as e:
        print(f"Error writing to CSV file {csv_file}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Scan JavaScript files for potentially dangerous commands.")
    parser.add_argument('directory', nargs='?', default='.', help='Directory to scan (default: current directory)')
    parser.add_argument('--output', '-o', help='File to save the report (plain text)')
    parser.add_argument('--csv', '-c', help='File to save the report in CSV format')
    parser.add_argument('--exclude', '-e', nargs='*', help='Directories to exclude from scanning (e.g., node_modules dist build)')
    args = parser.parse_args()

    directory = args.directory
    output_file = args.output
    csv_file = args.csv
    exclude_dirs = set(args.exclude) if args.exclude else set()

    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        return

    print(f"Scanning directory: {os.path.abspath(directory)}\n")
    matches = scan_directory(directory, PATTERNS, exclude_dirs)
    
    if output_file:
        # Export to plain text file
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                if not matches:
                    f.write("No potentially dangerous JavaScript commands found.\n")
                else:
                    f.write(f"{'File':<60} {'Line':<6} {'Issue':<30} {'Code'}\n")
                    f.write('-' * 120 + '\n')
                    for file_path, issue, lineno, code in matches:
                        display_path = (file_path[:57] + '...') if len(file_path) > 60 else file_path
                        f.write(f"{display_path:<60} {lineno:<6} {issue:<30} {code}\n")
                    f.write(f"\nTotal Issues Found: {len(matches)}\n")
            print(f"Report successfully exported to {output_file}")
        except Exception as e:
            print(f"Error writing to {output_file}: {e}")
    
    if csv_file:
        # Export to CSV file
        export_to_csv(matches, csv_file)
    
    if not output_file and not csv_file:
        # If no output files specified, print to console
        print_report(matches)

if __name__ == "__main__":
        main()
