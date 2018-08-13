#!/bin/bash

#make it a while loop

foo='/Users/alex/Documents/GitHub/exp_saves/infer_using_seq100by20_01_so' #parent directory
bar='data1000by20_01' #place data folder in the foo
tar='inference_data1000by20_01_assemble5' #name of output dir
car='test_infer_1000_so' #name of inference file
fragnum=50

echo $foo; 

python ./assemble5.py --outdir=$foo/$tar --f_inference="$foo/$car" --fragnum=$fragnum --overlap=0.1 --delta=0.1

echo "report"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons.txt --trace=$foo/$bar/test.trace --labels=$foo/$bar/test.label --mode=edit --bias=sin

##DONE