#!/usr/bin/env bash

function start {
    echo "Starting scrapyd"
    source activate LuxuryInfoSpider
    nohup scrapyd 2>&1 > scrapyd.log &
    echo "scrapyd started"
}

function stop {
    echo "Stopping scrapyd"
    pkill -f "scrapyd"
    echo "scrapyd stopped"
}

case $1 in
    start)   start;;
    stop)    stop;;
    *) echo "usage: $0 start|stop" >&2
       exit 1
       ;;
esac