#!/bin/bash

#make it a while loop

foo='/Users/alex/Documents/GitHub/exp_saves/infer_using_seq50by10_04' #parent directory
bar='data50by10_04' #place data folder in the foo
tar='inference_data50by10_04_assemble13' #name of output dir
car='test50_04_infer' #name of inference file
fragnum=5

echo $foo; 

python ./assemble13.py --outdir=$foo/$tar --f_inference="$foo/$car" --fragnum=$fragnum --mode="both" --bias=prob --overlap=0.4

echo "edit prob"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_edit_prob.txt --trace=$foo/$bar/test.trace --labels=$foo/$bar/test.label --mode=edit --bias=prob 
echo "hamming prob"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_hamming_prob.txt --trace=$foo/$bar/test.trace --labels=$foo/$bar/test.label --mode=hamming --bias=prob 

#done
#/Users/alex/Desktop