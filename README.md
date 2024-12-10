# LinkedIn Repository Checker

This tool was created to help identify potential scams on LinkedIn, where malicious actors share code repositories (often from platforms like Bitbucket) intending to run harmful code on your machine. The LinkedIn Repository Checker focuses on scanning JavaScript-based projects—including Node.js, React, and other JavaScript libraries—to detect suspicious or potentially malicious code.

## Features

- **JavaScript-Focused:** Designed specifically for Node.js, React, and general JavaScript libraries.
- **Flexible Output Formats:** Generate security reports in both text and CSV formats.
- **Easy Integration:** Clone the repository and run a single command to start scanning.

## Requirements

- **Python 3:** Make sure Python 3 is installed on your system.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/TeknoPT/LinkedInChecker.git
   ```
2. **Navigate to the Project Directory:**
   ```bash
   cd LinkedInChecker
   ```

## How to Run

**Arguments:**

1. **Folder Path:** The path to the folder you want to scan.
2. **--output report.txt:** (Optional) Specify a text file where the report will be saved.
3. **--csv report.csv:** (Optional) Specify a CSV file where the report will be saved.

**Example Command:**

```bash
python3 checker.py /path/to/scan --output report.txt --csv security_report.csv
```

- Replace `/path/to/scan` with the directory you want to inspect.
- `--output report.txt` will create a `report.txt` file with the findings.
- `--csv security_report.csv` will create a `security_report.csv` file with the same findings in CSV format.

**Note:** You can omit the `--output` or `--csv` arguments if you only need one format or none at all.

## Contributing

Contributions are welcome! If you have ideas for improving the scanner, detecting more threats, or supporting additional languages, feel free to open issues or submit pull requests.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use it, modify it, and share it as you see fit.
