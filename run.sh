#!/bin/sh

PID1=`pgrep -f wsgi.py`
if [ -z "$PID1" ]; then
    echo "Web server not running"
else
    echo "Web server running; restarting..."
    kill $PID1
fi
python wsgi.py 2>flaskLog &

