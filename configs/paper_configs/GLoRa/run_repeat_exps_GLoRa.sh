
#!/bin/bash

cd ../../..

##### Vanilla GNN Systems
cfg="configs/paper_configs/GLoRa/vanilla/GLoRa_GCN.yaml"
min_depth=3
max_depth=15
load=True
for ((d=min_depth; d<=max_depth; d+=1))
do
python main.py --repeat 5 --cfg $cfg   GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
done


cfg="configs/paper_configs/GLoRa/vanilla/GLoRa_GAT.yaml"
min_depth=3
max_depth=15
load=True
for ((d=min_depth; d<=max_depth; d+=1))
do
python main.py --repeat 5 --cfg $cfg   GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
done

cfg="configs/paper_configs/GLoRa/vanilla/GLoRa_SGC.yaml"
min_depth=3
max_depth=15
load=True
for ((d=min_depth; d<=max_depth; d+=1))
do
python main.py --repeat 5 --cfg $cfg   GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
done

cfg="configs/paper_configs/GLoRa/vanilla/GLoRa_SAGE.yaml"
min_depth=3
max_depth=15
load=True
for ((d=min_depth; d<=max_depth; d+=1))
do
python main.py --repeat 5 --cfg $cfg   GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
done

cfg="configs/paper_configs/GLoRa/vanilla/GLoRa_GatedGCN.yaml"
min_depth=3
max_depth=15
load=True
for ((d=min_depth; d<=max_depth; d+=1))
do
python main.py --repeat 5 --cfg $cfg   GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
done

cfg="configs/paper_configs/GLoRa/vanilla/GLoRa_GatedGCN+LapPE.yaml"
min_depth=3
max_depth=15
load=True
for ((d=min_depth; d<=max_depth; d+=1))
do
python main.py --repeat 5 --cfg $cfg   GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
done

cfg="configs/paper_configs/GLoRa/vanilla/GLoRa_GIN.yaml"
min_depth=3
max_depth=15
load=True
for ((d=min_depth; d<=max_depth; d+=1))
do
python main.py --repeat 5 --cfg $cfg   GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
done


cfg="configs/paper_configs/GLoRa/vanilla/GLoRa_GGNN.yaml"
min_depth=3
max_depth=15
load=True
for ((d=min_depth; d<=max_depth; d+=1))
do
python main.py --repeat 5 --cfg $cfg   GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
done


#### Over-Smoothing GNN Systems
cfg="configs/paper_configs/GLoRa/over-smoothing/GLoRa_GPRGNN.yaml"
min_depth=3
max_depth=15
load=True
for ((d=min_depth; d<=max_depth; d+=1))
do
python main.py --repeat 5 --cfg $cfg   GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
done

cfg="configs/paper_configs/GLoRa/over-smoothing/GLoRa_GCNII.yaml"
min_depth=3
max_depth=15
load=True
for ((d=min_depth; d<=max_depth; d+=1))
do
python main.py --repeat 5 --cfg $cfg   GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
done

cfg="configs/paper_configs/GLoRa/over-smoothing/GLoRa_APPNP.yaml"
min_depth=3
max_depth=15
load=True
for ((d=min_depth; d<=max_depth; d+=1))
do
python main.py --repeat 5 --cfg $cfg   GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
done

cfg="configs/paper_configs/GLoRa/over-smoothing/GLoRa_DAGNN.yaml"
min_depth=3
max_depth=15
load=True
for ((d=min_depth; d<=max_depth; d+=1))
do
python main.py --repeat 5 --cfg $cfg   GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
done

cfg="configs/paper_configs/GLoRa/over-smoothing/GLoRa_PairNorm.yaml"
min_depth=3
max_depth=15
load=True
for ((d=min_depth; d<=max_depth; d+=1))
do
python main.py --repeat 5 --cfg $cfg   GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
done

cfg="configs/paper_configs/GLoRa/over-smoothing/GLoRa_DropEdge.yaml"
min_depth=3
max_depth=15
load=True
for ((d=min_depth; d<=max_depth; d+=1))
do
python main.py --repeat 5 --cfg $cfg   GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
done

cfg="configs/paper_configs/GLoRa/over-smoothing/GLoRa_G2.yaml"
min_depth=3
max_depth=15
load=True
for ((d=min_depth; d<=max_depth; d+=1))
do
python main.py --repeat 5 --cfg $cfg   GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
done

cfg="configs/paper_configs/GLoRa/over-smoothing/GLoRa_JKNet.yaml"
min_depth=3
max_depth=15
load=True
for ((d=min_depth; d<=max_depth; d+=1))
do
python main.py --repeat 5 --cfg $cfg   GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
done

cfg="configs/paper_configs/GLoRa/over-smoothing/GLoRa_SkipSumGCN.yaml"
min_depth=3
max_depth=15
load=True
for ((d=min_depth; d<=max_depth; d+=1))
do
python main.py --repeat 5 --cfg $cfg   GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
done

cfg="configs/paper_configs/GLoRa/over-smoothing/GLoRa_SkipSumGAT.yaml"
min_depth=3
max_depth=15
load=True
for ((d=min_depth; d<=max_depth; d+=1))
do
python main.py --repeat 5 --cfg $cfg   GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
done

cfg="configs/paper_configs/GLoRa/over-smoothing/GLoRa_SkipSumGatedGCN.yaml"
min_depth=3
max_depth=15
load=True
for ((d=min_depth; d<=max_depth; d+=1))
do
python main.py --repeat 5 --cfg $cfg   GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
done

cfg="configs/paper_configs/GLoRa/over-smoothing/GLoRa_SkipConGCN.yaml"
min_depth=3
max_depth=15
load=True
for ((d=min_depth; d<=max_depth; d+=1))
do
python main.py --repeat 5 --cfg $cfg   GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
done

cfg="configs/paper_configs/GLoRa/over-smoothing/GLoRa_SkipConGAT.yaml"
min_depth=3
max_depth=15
load=True
for ((d=min_depth; d<=max_depth; d+=1))
do
python main.py --repeat 5 --cfg $cfg   GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
done

cfg="configs/paper_configs/GLoRa/over-smoothing/GLoRa_SkipConGatedGCN.yaml"
min_depth=3
max_depth=15
load=True
for ((d=min_depth; d<=max_depth; d+=1))
do
python main.py --repeat 5 --cfg $cfg   GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
done

cfg="configs/paper_configs/GLoRa/over-squashing/GLoRa_SDRF.yaml"
min_depth=3
max_depth=15
load=True
for ((d=min_depth; d<=max_depth; d+=1))
do
python main.py --repeat 5 --cfg $cfg   GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
done

cfg="configs/paper_configs/GLoRa/over-squashing/GLoRa_FOSR.yaml"
min_depth=3
max_depth=15
load=True
fosr_dataset="datasets/tmp_fosr"
for ((d=min_depth; d<=max_depth; d+=1))
do
find $fosr_dataset -type f -delete
python main.py --repeat 5 --cfg $cfg dataset.dir $fosr_dataset  GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
find $fosr_dataset -type f -delete
done


cfg="configs/paper_configs/GLoRa/over-squashing/GLoRa_SP-GCN.yaml"
min_depth=3
max_depth=15
load=True
spgcn_dataset="datasets/tmp_spgcn"
for ((d=min_depth; d<=max_depth; d+=1))
do
find $spgcn_dataset -type f -delete
python main.py --repeat 5 --cfg $cfg dataset.dir $spgcn_dataset GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
find $spgcn_dataset -type f -delete
done



cfg="configs/paper_configs/GLoRa/over-squashing/GLoRa_FA-GCN.yaml"
min_depth=3
max_depth=15
load=True
fagcn_dataset="datasets/tmp_fagcn"
for ((d=min_depth; d<=max_depth; d+=1))
do
find $fagcn_dataset -type f -delete
python main.py --repeat 5 --cfg $cfg dataset.dir $fagcn_dataset GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
find $fagcn_dataset -type f -delete
done


cfg="configs/paper_configs/GLoRa/over-squashing/GLoRa_DrewGCN.yaml"
min_depth=12
max_depth=12
load=False
drewgcn_dataset="datasets/tmp_drew"
for ((d=min_depth; d<=max_depth; d+=1))
do
find $drewgcn_dataset -type f -delete
python main.py --repeat 5 --cfg $cfg dataset.dir $drewgcn_dataset GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
find $drewgcn_dataset -type f -delete
done


cfg="configs/paper_configs/GLoRa/over-squashing/GLoRa_DrewGCNWoDelay.yaml"
min_depth=3
max_depth=15
load=True
drewgcn_dataset="datasets/tmp_drewgncwodelay"
for ((d=min_depth; d<=max_depth; d+=1))
do
find $drewgcn_dataset -type f -delete
python main.py --repeat 5 --cfg $cfg dataset.dir $drewgcn_dataset GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
find $drewgcn_dataset -type f -delete
done

cfg="configs/paper_configs/GLoRa/over-squashing/GLoRa_DrewGCN+LapPE.yaml"
min_depth=3
max_depth=15
load=True
fagcn_dataset="datasets/tmp_drew+lappe"
for ((d=min_depth; d<=max_depth; d+=1))
do
find $fagcn_dataset -type f -delete
python main.py --repeat 5 --cfg $cfg dataset.dir $fagcn_dataset GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
find $fagcn_dataset -type f -delete
done

cfg="configs/paper_configs/GLoRa/over-squashing/GLoRa_DIGLGatedGCN.yaml"
min_depth=3
max_depth=15
load=True
fagcn_dataset="datasets/tmp_diglgatedgcn"
for ((d=min_depth; d<=max_depth; d+=1))
do
find $fagcn_dataset -type f -delete
python main.py --repeat 5 --cfg $cfg dataset.dir $fagcn_dataset GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
find $fagcn_dataset -type f -delete
done

cfg="configs/paper_configs/GLoRa/over-squashing/GLoRa_DIGLGatedGCN+LapPE.yaml"
min_depth=3
max_depth=15
load=True
fagcn_dataset="datasets/tmp_diglgatedgcn+lappe"
for ((d=min_depth; d<=max_depth; d+=1))
do
find $fagcn_dataset -type f -delete
python main.py --repeat 5 --cfg $cfg dataset.dir $fagcn_dataset GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
find $fagcn_dataset -type f -delete
done


cfg="configs/paper_configs/GLoRa/over-squashing/GLoRa_MixHopGCN.yaml"
min_depth=3
max_depth=15
load=True
for ((d=min_depth; d<=max_depth; d+=1))
do
python main.py --repeat 5 --cfg $cfg  GLoRa.depth $d  GLoRa.load $load gnn.layers_mp $d
done

cfg="configs/paper_configs/GLoRa/transformer/GLoRa_Transformer+LapPE.yaml"
min_depth=3
max_depth=15
load=True
for ((d=min_depth; d<=max_depth; d+=1))
do
python main.py --repeat 5 --cfg $cfg  GLoRa.depth $d  GLoRa.load $load
done

cfg="configs/paper_configs/GLoRa/transformer/GLoRa_GPSGatedGCN+LapPE.yaml"
min_depth=3
max_depth=15
load=True
for ((d=min_depth; d<=max_depth; d+=1))
do
python main.py --repeat 5 --cfg $cfg  GLoRa.depth $d  GLoRa.load $load gt.layers $d
done

cfg="configs/paper_configs/GLoRa/transformer/GLoRa_SAN+LapPE.yaml"
min_depth=3
max_depth=15
load=True
for ((d=min_depth; d<=max_depth; d+=1))
do
python main.py --repeat 5 --cfg $cfg  GLoRa.depth $d  GLoRa.load $load
done

