#!/bin/bash

#make it a while loop

foo='/Users/alex/Documents/GitHub/exp_saves/infer_using_seq50by10_04' #parent directory
bar='data500by10_04' #place data folder in the foo
tar='inference_data500by10_04_assemble10' #name of output dir
car='test500_04_infer' #name of inference file
fragnum=50

echo $foo; 

python ./assemble10.py --outdir=$foo/$tar --f_inference="$foo/$car" --fragnum=$fragnum --mode="both" --bias=sin

echo "edit sin"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_edit_sin.txt --trace=$foo/$bar/test.trace --labels=$foo/$bar/test.label --mode=edit --bias=sin
echo "hamming sin"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_hamming_sin.txt --trace=$foo/$bar/test.trace --labels=$foo/$bar/test.label --mode=hamming --bias=sin

python ./assemble10.py --outdir=$foo/$tar --f_inference="$foo/$car" --fragnum=$fragnum --mode="both" --bias=log
echo "edit log"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_edit_log.txt --trace=$foo/$bar/test.trace --labels=$foo/$bar/test.label --mode=edit --bias=log
echo "hamming log"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_hamming_log.txt --trace=$foo/$bar/test.trace --labels=$foo/$bar/test.label --mode=hamming --bias=log

#done
#/Users/alex/Desktop