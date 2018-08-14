#!/bin/bash

#make it a while loop


foo='/Users/alex/Documents/GitHub/exp_saves/infer_using_seq100by20_04' #parent directory
bar='data100by20_04' #place data folder in the foo
tar='inference_data100by20_04_assemble9' #name of output dir
car='test100_04_infer' #name of inference file
fragnum=5
over=0.4


echo $foo; 

python ./assemble9.py --outdir=$foo/$tar --f_inference="$foo/$car" --fragnum=$fragnum --overlap=$over --delta=0.1

echo "report"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons.txt --trace=$foo/$bar/test.trace --labels=$foo/$bar/test.label --mode=none--bias=none

##DONE