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

'''
def edit2(string1, string2):
    len1 = len(string1)
    len2 = len(string2)
    v = np.zeros([len1+1,len2+1])
    for i in range(1,len1):
        v[i,0] = i
    for j in range(1,len2):
        v[0,j] = j
    for i in range(0,len1):
        for j in range(0,len2):
            if string1[i] == string2[j]:
                #v[i+1,j+1] = v[i,j]
                substitutionCost = 0
            else:
                #v[i+1,j+1] = 1 + min(min(v[i+1,j],v[i,j+1]),v[i,j])
                substitutionCost = 1
            deletion = v[i,j+1] + 2
            insertion = v[i+1,j] + 2
            substitution = v[i,j] + substitutionCost
            v[i+1,j+1] = min(min(deletion,insertion),substitution)
    return v[len1,len2]
'''
def edit2(s1, s2):
    if len(s1) < len(s2):
        return edit2(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 2 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 2       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def avg_edit2(assembled_f,labels_f,seqnum):
    avg = 0
    for (ass,lab) in zip(assembled_f,labels_f):
        avg += edit2(ass,lab) / len(lab)
    avg = avg / seqnum
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
    ed2 = avg_edit2(assembled_f,labels_f,seqnum)
    hd = avg_hamming(assembled_f,labels_f,seqnum)
    delta = avg_delta(assembled_f,trace_f,seqnum)
    len_diff = avg_len_diff(assembled_f,labels_f,seqnum)

    return ed, ed2, hd, delta, len_diff

def create_summary(editAvg,editAvg2,hammingAvg,deltaAvg,len_diff,seqnum,outdir,mode,bias):
    
    summary = 'Dataset Report' 
    summary += '\nNumber of sequences =   ' + str(seqnum)
    summary += '\nAverage normalized edit distance = ' + str(editAvg)
    summary += '\nAverage normalized editdistance 2 = ' + str(editAvg2)
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

editAvg, editAvg2, hammingAvg, deltaAvg, len_diff = diagnose(assembled_f,labels_f,trace_f,seqnum1)

print('ANED: ' + str(editAvg))
print('ANED2: ' + str(editAvg2))
print('ANHD: ' + str(hammingAvg))
print("ANLD: " + str(len_diff))
print('delta: ' + str(deltaAvg))

create_summary(editAvg, editAvg2, hammingAvg, deltaAvg, len_diff, seqnum1, outdir, mode, bias)
