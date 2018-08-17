#!/bin/bash

#make it a while loop

foo='/Users/alex/Documents/GitHub/exp_saves/infer_using_seq2t100by20_04' #parent directory
bar='data2t100by20_04' #place data folder in the foo
tar='inference_data2t100by20_04_assemble12_test' #name of output dir
car='test100_04_infer' #name of inference file
fragnum=5

echo $foo; 


python ./assemble12_test.py --outdir=$foo/$tar --f_inference="$foo/$car" --fragnum=$fragnum --mode="both" --bias=prob --overlap=0.4

echo "edit prob"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_edit_prob.txt --trace=$foo/$bar/test.trace0 --labels=$foo/$bar/test.label --mode=edit --bias=prob 
echo "hamming prob"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_hamming_prob.txt --trace=$foo/$bar/test.trace0 --labels=$foo/$bar/test.label --mode=hamming --bias=prob 

#done
#/Users/alex/Desktop