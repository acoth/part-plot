#!/bin/sh

PID1=`pgrep -f serve.py`
if [ -z "$PID1" ]; then
    echo "Web server not running"
else
    echo "Web server running; restarting..."
    kill $PID1
fi
python serve.py 2>flaskLog -p $1 &

