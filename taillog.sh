clear && cat open.txt  && echo > logs && tail -F logs | grep -E "State|Client"
