#!/bin/bash

#make it a while loop

foo='/Users/alex/Documents/GitHub/exp_saves/infer_using_seq100by20_01_so' #parent directory
bar='data1000by20_01' #place data folder in the foo
tar='inference_data1000by20_01_assemble2' #name of output dir
car='test_infer_1000_so' #name of inference file
fragnum=50

echo $foo; 

python ./assemble2.py --outdir=$foo/$tar --f_inference="$foo/$car" --fragnum=$fragnum --mode="both" --bias=sin

echo "edit sin"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_edit_sin.txt --labels=$foo/$bar/test.label --mode=edit --bias=sin
echo "hamming sin"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_hamming_sin.txt --labels=$foo/$bar/test.label --mode=hamming --bias=sin

python ./assemble2.py --outdir=$foo/$tar --f_inference="$foo/$car" --fragnum=$fragnum --mode="both" --bias=log
echo "edit log"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_edit_log.txt --labels=$foo/$bar/test.label --mode=edit --bias=log
echo "hamming log"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_hamming_log.txt --labels=$foo/$bar/test.label --mode=hamming --bias=log

python ./assemble2.py --outdir=$foo/$tar --f_inference="$foo/$car" --fragnum=$fragnum --mode="both" --bias=logsin
echo "edit logsin"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_edit_logsin.txt --labels=$foo/$bar/test.label --mode=edit --bias=logsin
echo "hamming logsin"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_hamming_logsin.txt --labels=$foo/$bar/test.label --mode=hamming --bias=logsin

python ./assemble2.py --outdir=$foo/$tar --f_inference="$foo/$car" --fragnum=$fragnum --mode="both" --bias=sigmoid
echo "edit sigmoid"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_edit_logsin.txt --labels=$foo/$bar/test.label --mode=edit --bias=sigmoid
echo "hamming sigmoid"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_hamming_logsin.txt --labels=$foo/$bar/test.label --mode=hamming --bias=sigmoid

python ./assemble2.py --outdir=$foo/$tar --f_inference="$foo/$car" --fragnum=$fragnum --mode="both" --bias=tanh
echo "edit tanh"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_edit_logsin.txt --labels=$foo/$bar/test.label --mode=edit --bias=tanh
echo "hamming tanh"
python report.py --outdir=$foo/$tar --assembled=$foo/$tar/recons_hamming_logsin.txt --labels=$foo/$bar/test.label --mode=hamming --bias=tanh


#done
#/Users/alex/Desktop