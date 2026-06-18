import boto3
import subprocess
import json
from datetime import datetime

def get_system_metrics():
    metrics = {}


    #CPU usage
    cpu = subprocess.run(['top', '-bn1'], capture_output=True, text=True)
    for line in cpu.stdout.split('\n'):
        if 'Cpu(s)' in line:
            metrics['cpu_percent'] = float(line.split()[1].replace('%us,', '').strip())
# Memory usage
    mem = subprocess.run(['free', '-m'], capture_output=True, text=True)
    lines = mem.stdout.split('\n')
    mem_values = lines[1].split()
    total = int(mem_values[1])
    used = int(mem_values[2])
    metrics['memory_percent'] = round((used/total) * 100, 2)

    # Disk usage
    disk = subprocess.run(['df', '-h', '/'], capture_output=True, text=True)
    disk_values = disk.stdout.split('\n')[1].split()
    metrics['disk_percent'] = int(disk_values[4].replace('%', ''))

    return metrics

def generate_report(metrics):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report = f"""
==========================================
EC2 Health Report - {timestamp}
==========================================
CPU Usage:    {metrics['cpu_percent']}%
Memory Usage: {metrics['memory_percent']}%
Disk Usage:   {metrics['disk_percent']}%
==========================================
Status: {'CRITICAL' if any(v > 80 for v in metrics.values()) else 'OK'}
==========================================
"""
    return report

def upload_to_s3(report, filename):
    s3 = boto3.client('s3')
    s3.put_object(
        Bucket='devops-roshan-aws',
        Key=f'week1-project/reports/{filename}',
        Body=report
    )
    print(f"Uploaded {filename} to S3")

if __name__ == '__main__':
    metrics = get_system_metrics()
    report = generate_report(metrics)
    print(report)
    filename = f"health-{datetime.now().strftime('%Y-%m-%d-%H-%M')}.txt"
    upload_to_s3(report, filename)

