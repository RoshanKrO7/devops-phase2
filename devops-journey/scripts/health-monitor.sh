#!/bin/bash

# ==========================================
# System Health Monitor
# Author: Roshan Kumar
# ==========================================

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No color

# Thresholds
CPU_THRESHOLD=80
MEM_THRESHOLD=80
DISK_THRESHOLD=80

# Functions
print_header() {
    echo "=========================================="
    echo "   System Health Report - $(date)"
    echo "=========================================="
}

check_cpu() {
    CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | tr -d '%us,')
    echo -e "\n[CPU Usage]: $CPU%"
    if (( $(echo "$CPU > $CPU_THRESHOLD" | bc -l) )); then
        echo -e "${RED}WARNING: CPU usage is high!${NC}"
    else
        echo -e "${GREEN}OK: CPU usage is normal${NC}"
    fi
}

check_memory() {
    MEM=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
    echo -e "\n[Memory Usage]: $MEM%"
    if [ $MEM -gt $MEM_THRESHOLD ]; then
        echo -e "${RED}WARNING: Memory usage is high!${NC}"
    else
        echo -e "${GREEN}OK: Memory usage is normal${NC}"
    fi
}

check_disk() {
    DISK=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
    echo -e "\n[Disk Usage]: $DISK%"
    if [ $DISK -gt $DISK_THRESHOLD ]; then
        echo -e "${RED}WARNING: Disk usage is high!${NC}"
    else
        echo -e "${GREEN}OK: Disk usage is normal${NC}"
    fi
}

check_services() {
    echo -e "\n[Services]:"
    SERVICES=("ssh" "cron")
    for SERVICE in "${SERVICES[@]}"; do
        if service $SERVICE status > /dev/null 2>&1; then
            echo -e "${GREEN}OK: $SERVICE is running${NC}"
        else
            echo -e "${RED}DOWN: $SERVICE is not running${NC}"
        fi
    done
}

top_processes() {
    echo -e "\n[Top 3 CPU Processes]:"
    ps aux --sort=-%cpu | awk 'NR==2,NR==4 {print $1, $3"%", $11}'
}

check_network() {
    echo -e "\n[Network Check]:"
    if ping -c 1 google.com &> /dev/null; then
        echo -e "${GREEN}OK: Internet is reachable${NC}"
    else
        echo -e "${RED}DOWN: No internet connection${NC}"
    fi

    echo "Open ports:"
    ss -tuln | grep LISTEN | awk '{print $5}' | tail -n 5
}

usage() {
    echo "Usage: ./health-monitor.sh [option]"
    echo ""
    echo "Options:"
    echo "  --report    Run full health check (default)"
    echo "  --cpu       Check CPU only"
    echo "  --memory    Check memory only"
    echo "  --disk      Check disk only"
    echo "  --network   Check network only"
    echo "  --help      Show this help message"
}

# ---- Run ----
OPTION=${1:-"--report"}

case $OPTION in
    --report)
        print_header
        check_cpu
        check_memory
        check_disk
        check_services
        top_processes
        check_network
        echo -e "\n=========================================="
        echo "Report complete!"
        echo "=========================================="
        ;;
    --cpu)     print_header; check_cpu ;;
    --memory)  print_header; check_memory ;;
    --disk)    print_header; check_disk ;;
    --network) print_header; check_network ;;
    --help)    usage ;;
    *)
        echo "Unknown option: $OPTION"
        usage
        exit 1
        ;;
esac
