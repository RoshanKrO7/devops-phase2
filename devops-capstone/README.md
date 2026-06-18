# DevOps Monitoring Tool

A Python-based CLI tool to monitor system health and GitHub stats.
Built as Phase 1 capstone project of my DevOps journey.

## Features
- Real-time CPU, memory and disk monitoring
- Color coded output (green/yellow/red based on usage)
- Service status checks (SSH, cron)
- GitHub profile stats via API
- Auto commits and pushes reports to GitHub
- JSON report generation

## Requirements
```bash
pip install requests
```

## Usage
```bash
python3 monitor.py --report    # full system report + push to GitHub
python3 monitor.py --health    # CPU, memory, disk only
python3 monitor.py --github    # GitHub stats only
python3 monitor.py --history   # show last saved report
python3 monitor.py --help      # show usage
```

## Example Output
==========================================
System Report - 2026-06-01 17:07:14
CPU:       0.0%
Memory:    13%
Disk:      1%
SSH:       stopped
Cron:      running
GitHub:    RoshanKrO7 | Repos: 11 | Followers: 3
Report saved to reports/report.json
Report pushed to GitHub!

## Project Structure
devops-capstone/
├── monitor.py        # main tool
├── reports/          # JSON reports saved here
├── .gitignore        # ignored files
└── README.md         # this file

## How it works
1. Runs shell commands via Python subprocess
2. Calls GitHub API using requests library
3. Saves report as JSON to reports/
4. Auto commits and pushes to GitHub after every report

## What I learned building this
- Python subprocess, file I/O, JSON, requests
- Linux commands from Python
- Git automation
- CLI argument handling
- Error handling and color output

## Author
Roshan Kumar — DevOps Journey Phase 1
