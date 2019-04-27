# nohup allows to run command/process or shell script that can continue running in the background after you log out from a shell.
# ">" 1.txt it forword the output to this file.
# 2>&1 move all the stderr to stdout.
# and & allows you to run a command/process in background on the current shell.
# nohup /anaconda3/bin/python ./app.py > ./logs/app_log.txt 2>&1 &
nohup /home/ubuntu/anaconda3/bin/python ./app.py > /dev/null &