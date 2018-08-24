#!/bin/bash

#make it a while loop


foo='/Users/alex/Documents/GitHub/exp_saves/infer_using_seq100by20_04' #parent directory
bar='data1000by20_04' #place data folder in the foo
tar='inference_data1000by20_04_assemble6' #name of output dir
car='test1000_04_infer' #name of inference file
fragnum=50
over=0.4

echo $foo; 

python ./assemble6.py --outdir=$foo/$tar --f_inference="$foo/$car" --fragnum=$fragnum --overlap=$over --delta=0.1 --assembly=super

echo "superposition"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_super.txt --trace=$foo/$bar/test.trace --labels=$foo/$bar/test.label --mode=super --bias=none


python ./assemble6.py --outdir=$foo/$tar --f_inference="$foo/$car" --fragnum=$fragnum --overlap=$over --delta=0.1 --assembly=inter  

echo "interpolation"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_inter.txt --trace=$foo/$bar/test.trace --labels=$foo/$bar/test.label --mode=inter --bias=none

##DONE