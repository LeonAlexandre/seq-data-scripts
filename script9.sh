#!/bin/bash

#make it a while loop


foo='/Users/alex/Documents/GitHub/exp_saves/infer_using_seq50by10_04' #parent directory
bar='data1000by10_04' #place data folder in the foo
tar='inference_data1000by10_04_assemble9' #name of output dir
car='test1000_04_infer' #name of inference file
fragnum=100
over=0.4


echo $foo; 

python ./assemble9.py --outdir=$foo/$tar --f_inference="$foo/$car" --fragnum=$fragnum --overlap=$over

echo "report"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons.txt --trace=$foo/$bar/test.trace --labels=$foo/$bar/test.label --mode=none--bias=none

##DONE