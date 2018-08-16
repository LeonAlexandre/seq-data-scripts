#!/bin/bash

#make it a while loop

foo='/Users/alex/Documents/GitHub/exp_saves/infer_using_seq50by10_04' #parent directory
bar='data1000by10_04' #place data folder in the foo
tar='inference_data1000by10_04_assemble12' #name of output dir
car='test1000_04_infer' #name of inference file
fragnum=100

echo $foo; 


python ./assemble12.py --outdir=$foo/$tar --f_inference="$foo/$car" --fragnum=$fragnum --mode="both" --bias=log
echo "edit log"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_edit_log.txt --trace=$foo/$bar/test.trace --labels=$foo/$bar/test.label --mode=edit --bias=log
echo "hamming log"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_hamming_log.txt --trace=$foo/$bar/test.trace --labels=$foo/$bar/test.label --mode=hamming --bias=log

python ./assemble12.py --outdir=$foo/$tar --f_inference="$foo/$car" --fragnum=$fragnum --mode="both" --bias=prob --overlap=0.4

echo "edit prob"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_edit_prob.txt --trace=$foo/$bar/test.trace --labels=$foo/$bar/test.label --mode=edit --bias=prob 
echo "hamming prob"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_hamming_prob.txt --trace=$foo/$bar/test.trace --labels=$foo/$bar/test.label --mode=hamming --bias=prob 

#done
#/Users/alex/Desktop