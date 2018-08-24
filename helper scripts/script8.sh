#!/bin/bash

#make it a while loop


foo='/Users/alex/Documents/GitHub/exp_saves/infer_using_seq100by20_04' #parent directory
bar='data1000by20_04' #place data folder in the foo
tar='inference_data1000by20_04_assemble8' #name of output dir
car='test1000_04_infer' #name of inference file
fragnum=50

echo $foo; 

python ./assemble8.py --outdir=$foo/$tar --f_inference="$foo/$car" --fragnum=$fragnum --mode="both" --bias=sin

echo "edit sin"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_edit_sin.txt --trace=$foo/$bar/test.trace --labels=$foo/$bar/test.label --mode=edit --bias=sin
echo "hamming sin"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_hamming_sin.txt --trace=$foo/$bar/test.trace --labels=$foo/$bar/test.label --mode=hamming --bias=sin

python ./assemble8.py --outdir=$foo/$tar --f_inference="$foo/$car" --fragnum=$fragnum --mode="both" --bias=log
echo "edit log"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_edit_log.txt --trace=$foo/$bar/test.trace --labels=$foo/$bar/test.label --mode=edit --bias=log
echo "hamming log"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_hamming_log.txt --trace=$foo/$bar/test.trace --labels=$foo/$bar/test.label --mode=hamming --bias=log

python ./assemble8.py --outdir=$foo/$tar --f_inference="$foo/$car" --fragnum=$fragnum --mode="both" --bias=logsin
echo "edit logsin"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_edit_logsin.txt --trace=$foo/$bar/test.trace --labels=$foo/$bar/test.label --mode=edit --bias=logsin
echo "hamming logsin"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_hamming_logsin.txt --trace=$foo/$bar/test.trace --labels=$foo/$bar/test.label --mode=hamming --bias=logsin

#done
#/Users/alex/Desktop