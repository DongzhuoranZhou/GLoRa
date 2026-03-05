

#!/bin/bash

cd ../../..

cfg="configs/paper_configs/GLoRa/GLoRa_data_generate.yaml"

num_graphs=2000
min_depth=3
max_depth=15
for ((d=min_depth; d<=max_depth; d+=1))
do
 python dataset_generation.py --cfg $cfg GLoRa.depth $d GLoRa.num_graphs $num_graphs
done

