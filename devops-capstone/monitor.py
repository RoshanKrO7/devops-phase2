#!/usr/bin/env python3

"""
DevOps Monitoring Tool
Author: Roshan Kumar
"""

import time
import os
import sys
import json
import subprocess
import requests
from datetime import datetime

# Return color based on usage percentage
def get_color(percent):
    value = float(percent.replace('%', ''))

    if value < 50:
        return GREEN
    elif value < 80:
        return YELLOW
    else:
        return RED

# Colors
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
NC = '\033[0m'  # No color

# --- Helper ---
# Run a shell command and return stdout or None on failure

def run_cmd(cmd):
	result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
	return result.stdout.strip() if result.returncode == 0 else None 

# ---- System checks ----
# Get current CPU usage percentage
def get_cpu():
    CPU = run_cmd("top -bn1 | grep 'Cpu(s)' | awk '{print $2}'")
    return {"cpu_usage": f"{CPU}%"}

# Get current memory usage percentage
def get_memory():
    memory = run_cmd("free | grep Mem | awk '{printf \"%.0f\", $3/$2 * 100}'")
    return {"memory_usage" : f"{memory}%"}
# Get current disk usage percentage
def get_disk():
    disk = run_cmd("df -h / | awk 'NR==2 {print $5}'")
    return {"disk_usage": f"{disk}"}
# Check if ssh and cron services are running
def get_services():
    services = ["ssh","cron"]
    result = {}
    for service in services:
        output = run_cmd(f"service {service} status")
        if output:
            result[service] = "running"
        else:
            result[service] = "stopped"
    return result
# Fetch GitHub profile stats for given username
# ---- GitHub ----
def get_github(username):
    try:
        r = requests.get(f"https://api.github.com/users/{username}", timeout=5)
        r.raise_for_status()
       	data = r.json()
        return {
       	    "username": data['login'],
            "repos": data['public_repos'],
            "followers": data['followers']
            }
    except Exception as e:
        return {"error": str(e)}

# ---- Report ----
# Generate full system report, save to JSON and push to GitHub

def generate_report():
    cpu = get_cpu()
    memory = get_memory()
    disk = get_disk()
    services = get_services()
    github = get_github("RoshanKrO7")
    report = {
    		"timestamp": str(datetime.now()),
    		"cpu": cpu,
    		"memory": memory,
    		"disk": disk,
    		"services": services,
    		"github": github
		}
    print("==========================================")
    print(f"   System Report - {str(datetime.now())[:19]}")
    print("==========================================")


    cpu_color = get_color(cpu['cpu_usage'])
    mem_color = get_color(memory['memory_usage'])
    disk_color = get_color(disk['disk_usage'])

    print(f"CPU:       {cpu_color}{cpu['cpu_usage']}{NC}")
    print(f"Memory:    {mem_color}{memory['memory_usage']}{NC}")
    print(f"Disk:      {disk_color}{disk['disk_usage']}{NC}")


    ssh_color = GREEN if services['ssh'] == 'running' else RED
    print(f"SSH:       {ssh_color}{services['ssh']}{NC}")

    CRON_color = GREEN if services['cron'] == 'running' else RED
    print(f"Cron:      {CRON_color}{services['cron']}{NC}")

    print(f"GitHub:    {YELLOW}{github['username']} | Repos: {github['repos']} | Followers: {github['followers']}{NC}")


    print("==========================================")
    warnings = []
    if float(cpu['cpu_usage'].replace('%','')) > 80:
        warnings.append(f"{RED}WARNING: CPU usage is high!{NC}")
    if float(memory['memory_usage'].replace('%','')) > 80:
        warnings.append(f"{RED}WARNING: Memory usage is high!{NC}")
    if float(disk['disk_usage'].replace('%','')) > 80:
        warnings.append(f"{RED}WARNING: Disk usage is high!{NC}")
    if warnings:
        print("\n--- ALERTS ---")
        for w in warnings:
            print(w)
    with open("reports/report.json", "w") as f:
      	json.dump(report, f, indent=2)
    print("Report saved to reports/report.json")
    return report

def git_push():
    run_cmd("git add reports/report.json")
    run_cmd(f'git commit -m "Report: {str(datetime.now())[:19]}"')
    result = run_cmd("git push")
    if result is not None:
        print(f"{GREEN}Report pushed to GitHub!{NC}")
    else:
        print(f"{RED}Git push failed{NC}")

def show_history():
    if os.path.exists("reports/report.json"):
        with open("reports/report.json", "r") as f:
            data = json.load(f)
        print(f"Last report: {data['timestamp'][:19]}")
        print(f"CPU: {data['cpu']['cpu_usage']}")
        print(f"Memory: {data['memory']['memory_usage']}")
        print(f"Disk: {data['disk']['disk_usage']}")
    else:
        print("No reports found yet. Run --report first.")

# Watch mode - run report every interval seconds
def watch_mode(interval=30):
    print(f"{YELLOW}Watch mode — running every {interval}s. Ctrl+C to stop.{NC}")
    try:
        while True:
            generate_report()
            print(f"Next report in {interval}s...")
            time.sleep(interval)
    except KeyboardInterrupt:
        print(f"\n{GREEN}Watch mode stopped.{NC}")

# ---- CLI ----
# CLI entry point - handle flags
def main():
    option = sys.argv[1] if len(sys.argv) > 1 else "--help"
    if option == "--report":
        report = generate_report()
        git_push()
    elif option == "--health":
        cpu = get_cpu()
        memory = get_memory()
        disk = get_disk()
        print(f"CPU:    {cpu['cpu_usage']}")
        print(f"Memory: {memory['memory_usage']}")
        print(f"Disk:   {disk['disk_usage']}")
    elif option == "--github":
        github = get_github("RoshanKrO7")
        print(f"GitHub: {github}")
    elif option == "--help":
        print("Usage: python3 monitor.py [--report|--health|--github|--history|--watch|--help]")
    elif option == "--history":
        show_history()
    elif option == "--watch":
        watch_mode()
    else:
        print("Unknown Option")
if __name__ == "__main__":
    main()

