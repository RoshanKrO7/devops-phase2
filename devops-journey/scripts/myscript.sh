#!/bin/bash

# Basic function
greet() {
    echo "Hello $1!"
}

# Function with multiple args
add_numbers() {
    RESULT=$(( $1 + $2 ))
    echo "$1 + $2 = $RESULT"
}

# Function that checks disk usage
check_disk() {
    USAGE=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
    if [ $USAGE -gt 80 ]; then
	echo "WARNING: Disk usage is at $USAGE%"
    else
        echo "OK: Disk usage is at $USAGE%"
    fi
}

# Call the functions
greet "Roshan"
greet "DevOps"
add_numbers 10 20
add_numbers 100 250
check_disk

