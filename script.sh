#!/bin/bash

#make it a while loop
over=0.1
for i in {1..5};
do foo="newdata$i";
echo $foo; 
python ./datagenCutter.py --out_dir=$foo --overlap=$over

python ./assemble.py --outdir=$foo --f_inference="$foo/frag_train.label" --fragnum=5 --mode="both" --bias=sin
echo "edit sin"
python report.py --outdir=$foo --assembled=$foo/recons_edit_sin.txt --labels=$foo/train.label --mode=edit --bias=sin
echo "hamming sin"
python report.py --outdir=$foo --assembled=$foo/recons_hamming_sin.txt --labels=$foo/train.label --mode=hamming --bias=sin

python ./assemble.py --outdir=$foo --f_inference="$foo/frag_train.label" --fragnum=5 --mode="both" --bias=log
echo "edit log"
python report.py --outdir=$foo --assembled=$foo/recons_edit_log.txt --labels=$foo/train.label --mode=edit --bias=log
echo "hamming log"
python report.py --outdir=$foo --assembled=$foo/recons_hamming_log.txt --labels=$foo/train.label --mode=hamming --bias=log





done
