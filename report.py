#Report

#Made a change
#    Arguments:
#    out_dir
#    assembled file
#    labels

import argparse
import random
import math
import os
import numpy as np
import Levenshtein as lv

def parse_arguments():
    """
    arguments: outdir, assembled, labels
    


    """
    ##PARSING THROUGH THE ARGUMENTS
    #initialize the parser
    parser = argparse.ArgumentParser()
    #Adding arguments
    #parser.add_argument("name", help="any help", type=str)
    #acces by args.name
    parser.add_argument("--outdir",dest="outdir",help='output directory', type=str,default='newdata')
    parser.add_argument('--assembled',dest="assembled",help='assembled output',type=str,default='please_specify_file.txt')
    parser.add_argument('--labels',dest="labels",help='labels output',type=str,default='please_specify_labels.txt')
    parser.add_argument('--mode',dest='mode',help='hamming | edit',type=str,default='hamming')
    parser.add_argument('--bias',dest='bias',help='log | sin (def) | logsin',type=str,default='sin')

    return parser.parse_args()

def read_list(input_file):
    #read lines in a list
    #split the list according to fragnum (list of list)
    #current = os.getcwd()
    inference_file = open(input_file,'r')
    lines = inference_file.readlines()
    seqnum = len(lines)

    return lines, seqnum

def avg_edit(assembled_f,labels_f,seqnum):
    avg = 0.0
    assembled_f = [x.replace(' ','') for x in assembled_f]
    #removes interstitial spaces
    labels_f = [x.replace(' ','') for x in labels_f]

    
    for i in range(seqnum):
        seqLength = len(labels_f[i]) 
        avg = avg + float(lv.distance(assembled_f[i],labels_f[i]) / seqLength)
    avg = float(avg/seqnum)
    return avg

def diagnose(assembled_f,labels_f,seqnum):
    editAvg = 0.0
    lengthAvg = 0.0

    assembled_f = [x.replace(' ','') for x in assembled_f]
    #removes interstitial spaces
    labels_f = [x.replace(' ','') for x in labels_f]

    
    for i in range(seqnum):
        seqLength = len(labels_f[i])
        traceLength = len(assembled_f[i])
        lengthAvg += abs(seqLength - traceLength) 
        editAvg = editAvg + float(lv.distance(assembled_f[i],labels_f[i]) / seqLength)
    editAvg = float(editAvg/seqnum)
    lengthAvg = float(lengthAvg)/seqnum
    return editAvg, lengthAvg

def create_summary(editAvg,lengthAvg,seqnum,outdir,mode,bias):
    
    summary = 'Dataset Report' 
    summary += '\nNumber of sequences =   ' + str(seqnum)
    summary += '\nAverage edit distance = ' + str(editAvg)
    summary += '\nAverage length mismatch = ' + str(lengthAvg)
    summary += '\nMode = ' + mode
    
    #current = os.getcwd()
    name = outdir + '/' +'Inference_Summary_' + mode + '_' + bias + '.txt'

    summary_file = open(name,"w+")
    summary_file.write(summary)
    summary_file.close()


##MAIN
args = parse_arguments()
outdir = args.outdir
assembled = args.assembled
labels = args.labels
mode = args.mode
bias = args.bias

assembled_f, seqnum1 = read_list(assembled)
labels_f, seqnum2 = read_list(labels)

if not seqnum1==seqnum2:
    print('number of sequences not equal. redo assembly?')
else:
    print("Number of sequences " + str(seqnum1))

editAvg, lengthAvg = diagnose(assembled_f,labels_f,seqnum1)

print('edit:' + str(editAvg))
print('length diff:' + str(lengthAvg))

create_summary(editAvg, lengthAvg, seqnum1, outdir, mode, bias)
