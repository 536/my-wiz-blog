#!/bin/bash
#chkconfig:345 85 15
#description: uwsgi service
if [ ! -n "$1" ]; then #$1：指该脚本后跟的第一个参数，-n：判断$1是否为非空， ！：取相反
    echo "Usages: sh uwsgi.sh [start|stop|restart]"
fi

psid=$(ps aux | grep "uwsgi" | grep -v "grep" | wc -l)psid=$(ps aux | grep "uwsgi" | grep -v "grep" | wc -l)

if [ $1 = start ]; then #如果第一个参数等于start，执行下面命令
    #上面执行了启动之后，判断启动是否正常，grep -v过滤掉“grep”，使用wc -l查看输出几行
    if [[ $psid -gt 4 ]]; then
        echo "uwsgi is running!"
    else
        uwsgi --ini /www/my-wiz-blog/uwsgi/uwsgi.ini
        echo "Start uwsgi service [OK]"
    fi

elif [ $1 = stop ]; then
    uwsgi --stop /www/my-wiz-blog/uwsgi/uwsgi.pid
    echo "Stop uwsgi service [OK]"
elif [ $1 = restart ]; then
    if [ ! -a "/www/my-wiz-blog/uwsgi/uwsgi.pid" ]; then
        uwsgi --reload /www/my-wiz-blog/uwsgi/uwsgi.pid
    else
        uwsgi --ini /www/my-wiz-blog/uwsgi/uwsgi.ini
    fi
    echo "Restart uwsgi service [OK]"
else
    echo "Usages: sh uwsgid.sh [start|stop|restart]"
fi
