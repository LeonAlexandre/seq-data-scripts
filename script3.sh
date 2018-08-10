#!/bin/bash

#make it a while loop

foo='/Users/alex/Documents/GitHub/exp_saves/infer_using_seq100by20_01_so' #parent directory
bar='data100by20_01' #place data folder in the foo
tar='inference_data100by20_01_assemble3_test' #name of output dir
car='output_test' #name of inference file
fragnum=5

echo $foo; 

python ./assemble3.py --outdir=$foo/$tar --f_inference="$foo/$car" --fragnum=$fragnum --mode="both" --bias=sin

echo "hamming sin"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_hamming_sin.txt --labels=$foo/$bar/test.label --mode=edit --bias=sin

#done
#/Users/alex/Desktop