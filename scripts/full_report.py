import boto3
import pymysql
import os
from datetime import datetime

def check_alb_targets():
    elbv2 = boto3.client('elbv2', region_name='ap-south-1')
    tg_response = elbv2.describe_target_groups(Names=['devops-tg'])
    tg_arn = tg_response['TargetGroups'][0]['TargetGroupArn']
    health_response = elbv2.describe_target_health(TargetGroupArn=tg_arn)
    targets = []
    for target in health_response['TargetHealthDescriptions']:
        targets.append(f"{target['Target']['Id']}: {target['TargetHealth']['State']}")
    return targets

def check_asg_status():
    autoscaling = boto3.client('autoscaling', region_name='ap-south-1')
    response = autoscaling.describe_auto_scaling_groups(AutoScalingGroupNames=['devops-asg'])
    asg = response['AutoScalingGroups'][0]
    return f"Min: {asg['MinSize']} | Max: {asg['MaxSize']} | Desired: {asg['DesiredCapacity']} | Current: {len(asg['Instances'])}"

def get_rds_servers():
    conn = pymysql.connect(
        host='devops-db.cr4w8cc6sj7h.ap-south-1.rds.amazonaws.com',
        user='admin',
        password=os.environ.get('RDS_PASSWORD'),
        database='devopsdb'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT hostname, ip_address, status FROM servers")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def generate_report():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report = f"==========================================\n"
    report += f"Week 2 Infrastructure Report - {timestamp}\n"
    report += f"==========================================\n\n"
    
    report += "--- ALB Target Health ---\n"
    for t in check_alb_targets():
        report += f"  {t}\n"
    
    report += "\n--- ASG Status ---\n"
    report += f"  {check_asg_status()}\n"
    
    report += "\n--- RDS Server Records ---\n"
    for row in get_rds_servers():
        report += f"  {row[0]} | {row[1]} | {row[2]}\n"
    
    report += "\n=========================================="
    return report

if __name__ == '__main__':
    report = generate_report()
    print(report)
    
    filename = f"infra-report-{datetime.now().strftime('%Y-%m-%d-%H-%M')}.txt"
    with open(filename, 'w') as f:
        f.write(report)
    
    s3 = boto3.client('s3')
    s3.upload_file(filename, 'devops-roshan-aws', f'week2-project/{filename}')
    print(f"\nUploaded {filename} to S3")
