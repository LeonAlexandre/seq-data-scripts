#!/bin/bash

#make it a while loop


foo='/Users/alex/Documents/GitHub/exp_saves/infer_using_seq50by10_04' #parent directory
bar='data100by10_04' #place data folder in the foo
tar='inference_data100by10_04_assemble11' #name of output dir
car='test100_04_infer' #name of inference file
fragnum=10
over=0.4


echo $foo; 

#python ./assemble11.py --outdir=$foo/$tar --f_inference="$foo/$car" --fragnum=$fragnum --overlap=$over 

echo "report"
#python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons.txt --trace=$foo/$bar/test.trace0 --labels=$foo/$bar/test.label --mode=none--bias=none

python region_analyzer.py --outdir=$foo/$tar --assembled=$foo/$tar/recons.txt --trace=$foo/$bar/test.trace --labels=$foo/$bar/test.label --mode=none--bias=none

##DONE

