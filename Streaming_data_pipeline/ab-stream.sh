#!/bin/bash

# Declare an array of possible host domains
declare -a arr=(".att.com" ".comcast.com" ".spectrum.com" ".xfinity.com")

# Declare an array with possible user actions
declare -a arr2=("http://localhost:5000/" "http://localhost:5000/purchase_a_gold_sword" \
"http://localhost:5000/purchase_a_katana_sword" \
"http://localhost:5000/join_warriors_guild" "http://localhost:5000/join_crusaders_guild" \
"http://localhost:5000/purchase_a_small_crossbow" "http://localhost:5000/purchase_a_medium_crossbow" \
"http://localhost:5000/purchase_a_shield" )

# Loop to create events
while true; do
# Generate random host names
randomhost="Host: user"
ranNum=${RANDOM:0:100000}
randomhost+="$ranNum"
rand=$[ $RANDOM % 4 ]
domain=${arr[$rand]}
randomhost+="$domain" 

# Randomly select a possible event
rand2=$[ $RANDOM % 8 ]
event=${arr2[$rand2]}

# Create random events using random hosts and events from above
docker-compose exec mids ab -n 1 -H "$randomhost" $event

# Pauses the execution of the next command for 1 second
sleep 1

done






