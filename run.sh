#!/bin/bash


read -t 30 -p "Waiting 30 seconds to make sure the internet is working"

${HOME}/Documents/src/python/punch_clock/punch/bin/python ${HOME}/Documents/src/python/punch_clock/start_day.py


#cd ${HOME}/src/python/punch_clock/

#source ./punch/bin/activate

# python start_day.py