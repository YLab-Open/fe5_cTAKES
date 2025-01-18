#!/bin/bash
nohup python3 -u "Step 1 - Prepare Input.py" > "Step 1 - Prepare Input.log" 2>&1 &
wait
nohup bash "./Step 2 - Run cTAKES.sh" > "Step 2 - Run cTAKES.log" 2>&1 &
wait
nohup python3 -u "Step 3 - Process Output.py" > "Step 3 - Process Output.log" 2>&1 &
wait