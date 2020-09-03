#!/bin/bash

# about 100k games per minute with simple players
trials=100000
for player in random estimator estimator_v2 estimator_v3 estimator_v4; do 
    source venv/bin/activate && time python drive.py --player ${player} --trials ${trials}
done

