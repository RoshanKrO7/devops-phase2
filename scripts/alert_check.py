import subprocess

THRESHOLDS = {
    'cpu': 80,
    'memory': 80,
    'disk': 80
}

def check_metrics():
    alerts = []

    # Memory
    mem = subprocess.run(['free', '-m'], capture_output=True, text=True)
    lines = mem.stdout.split('\n')
    mem_values = lines[1].split()
    mem_percent = round((int(mem_values[2]) / int(mem_values[1])) * 100, 2)
    if mem_percent > THRESHOLDS['memory']:
        alerts.append(f"ALERT: Memory at {mem_percent}%")

    # Disk
    disk = subprocess.run(['df', '/'], capture_output=True, text=True)
    disk_percent = int(disk.stdout.split('\n')[1].split()[4].replace('%', ''))
    if disk_percent > THRESHOLDS['disk']:
        alerts.append(f"ALERT: Disk at {disk_percent}%")

    return alerts

if __name__ == '__main__':
    print("Running alert check...")
    alerts = check_metrics()
    if alerts:
        for alert in alerts:
            print(alert)
    else:
        print("All metrics OK - no alerts")
