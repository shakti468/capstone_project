#!/bin/bash
# Usage: ./retry_wrapper.sh "<command>"

CMD=$1
MAX_RETRIES=3
COUNT=0

until [ $COUNT -ge $MAX_RETRIES ]
do
   echo "Attempt $((COUNT+1))..."
   eval "$CMD" && break
   COUNT=$((COUNT+1))
   sleep 5
done

if [ $COUNT -eq $MAX_RETRIES ]; then
   echo "❌ Command failed after $MAX_RETRIES retries."
   exit 1
fi
