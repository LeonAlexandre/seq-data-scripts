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
    parser.add_argument("--trace",dest="trace",help="trace file to calculate delta",type=str,default=None)
    parser.add_argument('--mode',dest='mode',help='hamming | edit | none | super | inter',type=str,default='hamming')
    parser.add_argument('--bias',dest='bias',help='log | sin (def) | logsin | none',type=str,default='sin')

    return parser.parse_args()

def read_list(input_file):
    #read lines in a list
    #split the list according to fragnum (list of list)
    __location__ = os.getcwd()
    inference_file = os.path.join(__location__,input_file)
    inference_file = open(input_file,'r')
    lines = inference_file.readlines()
    seqnum = len(lines)

    return lines, seqnum

def avg_edit(assembled_f,labels_f,seqnum):
    avg = 0.0
    for (ass,lab) in zip(assembled_f,labels_f):
        avg += lv.distance(ass,lab) / len(lab)
    avg = float(avg/seqnum)
    return avg

def avg_delta(assembled_f,trace_f,seqnum):
    avg = 0.0
    for (ass,tra) in zip(assembled_f,trace_f):
        avg += float(len(ass) - len(tra)) / len(ass)
    avg = avg / seqnum
    return avg

def avg_len_diff(assembled_f,labels_f,seqnum):
    avg = 0.0
    for (ass,lab) in zip(assembled_f,labels_f):
        avg += abs(len(ass)-len(lab)) / len(lab)
    avg = avg / seqnum
    return avg

def avg_hamming(assembled_f,labels_f,seqnum):
    avg = 0.0
    for (ass,lab) in zip(assembled_f,labels_f):
        ass_len = len(ass)
        lab_len = len(lab)
        if ass_len > lab_len:
            ass = ass[:lab_len]
        if ass_len < lab_len:
            ass = ass + "1" * (lab_len - ass_len)

        avg += sum(ass_sym != lab_sym for (ass_sym, lab_sym) in zip(ass,lab)) / lab_len

    avg = avg / seqnum
    return avg

def diagnose(assembled_f,labels_f,trace_f,seqnum):
    assembled_f = [x.replace(' ','') for x in assembled_f]
    labels_f = [x.replace(' ','') for x in labels_f]
    trace_f = [x.replace(' ','') for x in trace_f]

    ed = avg_edit(assembled_f,labels_f,seqnum)
    hd = avg_hamming(assembled_f,labels_f,seqnum)
    delta = avg_delta(assembled_f,trace_f,seqnum)
    len_diff = avg_len_diff(assembled_f,labels_f,seqnum)

    return ed, hd, delta, len_diff

def create_summary(editAvg,hammingAvg,deltaAvg,len_diff,seqnum,outdir,mode,bias):
    
    summary = 'Dataset Report' 
    summary += '\nNumber of sequences =   ' + str(seqnum)
    summary += '\nAverage normalized edit distance = ' + str(editAvg)
    summary += '\nAverage normalized hamming distance = ' + str(hammingAvg)
    summary += '\nAverage delta = ' + str(deltaAvg)
    summary += '\nAverage normalized len diff = ' + str(len_diff)
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
trace = args.trace
mode = args.mode
bias = args.bias

assembled_f, seqnum1 = read_list(assembled)
labels_f, seqnum2 = read_list(labels)
trace_f, _ = read_list(trace)

if not seqnum1==seqnum2:
    print('number of sequences not equal. redo assembly?')
else:
    print("Number of sequences " + str(seqnum1))

editAvg, hammingAvg, deltaAvg, len_diff = diagnose(assembled_f,labels_f,trace_f,seqnum1)

print('ANED: ' + str(editAvg))
print('ANHD: ' + str(hammingAvg))
print('delta: ' + str(deltaAvg))
print("ANLD: " + str(len_diff))

create_summary(editAvg, hammingAvg, deltaAvg, len_diff, seqnum1, outdir, mode, bias)
