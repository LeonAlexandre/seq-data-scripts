#!/bin/bash

#make it a while loop

foo='/Users/alex/Desktop/seq100by20_01_biadam_bahdanau'

echo $foo; 

python ./assemble.py --outdir=$foo --f_inference="$foo/output_test" --fragnum=5 --mode="both" --bias=sin

echo "edit sin"
python report.py --outdir=$foo --assembled=$foo/recons_edit_sin.txt --labels=$foo/test.label --mode=edit --bias=sin
echo "hamming sin"
python report.py --outdir=$foo --assembled=$foo/recons_hamming_sin.txt --labels=$foo/test.label --mode=hamming --bias=sin

python ./assemble.py --outdir=$foo --f_inference="$foo/output_test" --fragnum=5 --mode="both" --bias=log
echo "edit log"
python report.py --outdir=$foo --assembled=$foo/recons_edit_log.txt --labels=$foo/test.label --mode=edit --bias=log
echo "hamming log"
python report.py --outdir=$foo --assembled=$foo/recons_hamming_log.txt --labels=$foo/test.label --mode=hamming --bias=log

python ./assemble.py --outdir=$foo --f_inference="$foo/output_test" --fragnum=5 --mode="both" --bias=logsin
echo "edit logsin"
python report.py --outdir=$foo --assembled=$foo/recons_edit_logsin.txt --labels=$foo/test.label --mode=edit --bias=logsin
echo "hamming logsin"
python report.py --outdir=$foo --assembled=$foo/recons_hamming_logsin.txt --labels=$foo/test.label --mode=hamming --bias=logsin

done
#/Users/alex/Desktop