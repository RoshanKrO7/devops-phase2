import boto3
import subprocess
from datetime import datetime

# Run health monitor and capture output
result = subprocess.run(['bash', 'devops-journey/scripts/health-monitor.sh'], 
                      capture_output=True, text=True)

# Save to file
filename = f"health-report-{datetime.now().strftime('%Y-%m-%d-%H-%M')}.txt"
with open(filename, 'w') as f:
    f.write(result.stdout)

# Upload to S3
s3 = boto3.client('s3')
s3.upload_file(filename, 'devops-roshan-aws', f'reports/{filename}')
print(f"Uploaded {filename} to S3")
