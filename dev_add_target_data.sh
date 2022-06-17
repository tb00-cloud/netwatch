#!/bin/bash

NOW=$(date '+%Y-%m-%d %T')

# USER INPUT --------------------
# ===============================
STARTING="2022-06-17 20:00:00"
ENDING=$NOW
INTERVAL=60
TARGET=1
# ===============================

STARTING=$(date '+%Y-%m-%d %T' --date="$STARTING")
ENDING=$(date '+%Y-%m-%d %T' --date="$ENDING")

DIFF=$(( $(date -d "$ENDING" "+%s") - $(date -d "$STARTING" "+%s") ))
BLOCKS=$(expr $DIFF / $INTERVAL)



round() {
  # $1 is expression to round (should be a valid bc expression)
  # $2 is number of decimal figures (optional). Defaults to three if none given
  local df=${2:-3}
  printf '%.*f\n' "$df" "$(bc -l <<< "a=$1; if(a>0) a+=5/10^($df+1) else if (a<0) a-=5/10^($df+1); scale=$df; a/1")"
}

printf "Entering connection result history for target $TARGET every $INTERVAL seconds from $STARTING to $ENDING\n"

RUNS=1
until [[ "$STARTING" > "$ENDING" ]]; do
  PERCENT=$(round "100/$BLOCKS*$RUNS" 0)
  
  echo -ne "($PERCENT%)\r"

  mysql -h localhost -P 3306 --protocol=tcp -u root -p myapp -pqwerty --silent -e "INSERT INTO connResults (timestamp, targetID, statusID) VALUES (\"$STARTING\",$TARGET,0);" >/dev/null 2>&1
  STARTING=$(date -d "$STARTING $INTERVAL seconds" "+%Y-%m-%d %T")
  RUNS=$((RUNS+1))
done

echo "(100%)"
