# GLoRa: A Benchmark to Evaluate the Ability to Learn Long-Range Dependencies in Graphs

![example](misc/GLoRa_image.png)

A positive (a) and a negative (b) GLoRa examples for `d = 6`: green, blue, and orange nodes have embeddings of form `[1, -]` (source node), `[-, 1]` (normal node), and `[-, 0]` (hole) respectively; **T** marks the target node; and the red-arrows chain is the path justifying the long-range dependency.




This repository contains the code required to reproduce the experimental results for the architectures described in the "**GLoRa: A Benchmark to Evaluate the Ability to Learn Long-Range Dependencies in Graphs**" paper.

## Environment setup with conda
Configured for Linux.
```bash
conda create -n glora-env python=3.9
conda activate glora-env
conda install pytorch=1.9.1 torchvision torchaudio -c pytorch -c nvidia   
conda install pyg=2.0.2 -c pyg -c conda-forge
pip install ogb
pip install performer-pytorch
pip install torchmetrics==0.7.2
conda install pandas scikit-learn
conda install openbabel fsspec rdkit -c conda-forge
pip install tensorboard
pip install tensorboardX
# Check https://www.dgl.ai/pages/start.html to install DGL based on your CUDA requirements
pip install dgl-cu111 -f https://data.dgl.ai/wheels/repo.html
conda install setuptools==58.0.4
pip install numba
pip install tabulate
```

## Generate GLoRa benchmark

From inside `configs/paper_configs/GLoRa` use:

```
bash run_dataset_generation_GLoRa.sh
```

## Reproducing GLoRa experiments
From inside `configs/paper_configs/GLoRa` use:

```
bash run_repeat_exps_GLoRa.sh
```

## Reproducing the GLoRa benchmark single model evaluation
use:
```
python main.py --cfg {path_to_yaml_file}
```
All config files for GLoRa experiments used in the paper are in `configs/paper_configs/GLoRa`

Use custom arguments by appending the above with `{arg_name} {arg_val}`. See config files for arg options. E.g. to change the training batch size append "`train.batch_size 32`"

