#!/bin/bash

#make it a while loop

for i in {1..5};
do foo="newdata$i";
echo $foo; 
python ./datagenCutter.py --out_dir=$foo --overlap=0.3
python ./assemble.py --outdir=$foo --f_inference="$foo/frag_train.label" --fragnum=5 --mode="both"
python report.py --outdir=$foo --assembled=$foo/recons_edit.txt --labels=$foo/train.label --mode=edit
python report.py --outdir=$foo --assembled=$foo/recons_hamming.txt --labels=$foo/train.label --mode=hamming
done
