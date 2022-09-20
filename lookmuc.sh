#!/bin/sh

row=`netstat -an | grep ":9000" | awk '$1 == "tcp" && $NF == "LISTEN" {print $0}' | wc -l`

if [ $row -eq 0 ];then
	sh /data/workspace/muc/muc_start.sh
fi
