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
from weighted_levenshtein import lev
import time

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

def avg_edit2(assembled_f,labels_f,seqnum):
    avg = 0
    # Make array of costs, can control the edit cost for each opeartion and their application to each character
    # Example: insert_costs[ord('D')] = 1.5, make inserting the character 'D' have cost 1.5 (instead of 1)
    insert_costs = np.ones(128, dtype=np.float64) * 2
    delete_costs = np.ones(128, dtype=np.float64) * 2
    # Substitution costs can be specified independently in both directions, i.e. a->b can have different cost from b->a
    # Example: substitute_costs[ord('H'), ord('B')] = 1.25, make substituting 'H' for 'B' cost 1.25
    subs_costs = np.ones((128,128), dtype=np.float64) * 1
    for (ass,lab) in zip(assembled_f,labels_f):
        avg += lev(ass,lab,insert_costs=insert_costs,delete_costs=delete_costs,substitute_costs=subs_costs) / len(lab)
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

def reg_edit(assembled_f,labels_f,seqnum):
    avg0 = 0.0
    avg1 = 0.0
    avg2 = 0.0
    avg3 = 0.0

    for (ass,lab) in zip(assembled_f,labels_f):
        cut = int(len(ass) / 4 )
        print(cut)
        ass0 = ass[:cut]
        ass1 = ass[cut: 2*cut]
        ass2 = ass[2 * cut: 3* cut]
        ass3 = ass[-cut:]
        lab0 = lab[:cut]
        lab1 = lab[cut: 2*cut]
        lab2 = lab[2 * cut: 3* cut]
        lab3 = lab[-cut:]
        avg0 += lv.distance(ass0,lab0) / len(lab0)
        avg1 += lv.distance(ass1,lab1) / len(lab1)
        avg2 += lv.distance(ass2,lab2) / len(lab2)
        avg3 += lv.distance(ass3,lab3) / len(lab3)
    avg0 = float(avg0/seqnum)
    avg1 = float(avg1/seqnum)
    avg2 = float(avg2/seqnum)
    avg3 = float(avg3/seqnum)

    return avg0, avg1, avg2, avg3


def diagnose(assembled_f,labels_f,trace_f,seqnum):
    assembled_f = [x.replace(' ','') for x in assembled_f]
    labels_f = [x.replace(' ','') for x in labels_f]
    trace_f = [x.replace(' ','') for x in trace_f]

    start_time = time.time()
    ed = avg_edit(assembled_f,labels_f,seqnum)
    print("avg_edit took %s seconds" % (time.time()-start_time))
    start_time = time.time()
    ed2 = avg_edit2(assembled_f,labels_f,seqnum)
    print("avg_edit2 took %s seconds" % (time.time()-start_time))
    hd = avg_hamming(assembled_f,labels_f,seqnum)
    delta = avg_delta(assembled_f,trace_f,seqnum)
    len_diff = avg_len_diff(assembled_f,labels_f,seqnum)
    avg0, avg1, avg2, avg3 = reg_edit(assembled_f, labels_f, seqnum)

    return ed, ed2, hd, delta, len_diff, avg0, avg1, avg2, avg3

def create_summary(editAvg,editAvg2,hammingAvg,deltaAvg,len_diff,avg0, avg1, avg2, avg3,seqnum,outdir,mode,bias):
    
    summary = 'Dataset Report' 
    summary += '\nNumber of sequences =   ' + str(seqnum)
    summary += '\nAverage normalized edit distance = ' + str(editAvg)
    summary += '\nAverage normalized editdistance 2 = ' + str(editAvg2)
    summary += '\nAverage normalized hamming distance = ' + str(hammingAvg)
    summary += '\nAverage delta = ' + str(deltaAvg)
    summary += '\nAverage normalized len diff = ' + str(len_diff)
    summary += '\nRegion0' + str(avg0)
    summary += '\nRegion1' + str(avg1)
    summary += '\nRegion2' + str(avg2)
    summary += '\nRegion3' + str(avg3)
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

editAvg, editAvg2, hammingAvg, deltaAvg, len_diff, avg0, avg1, avg2, avg3 = diagnose(assembled_f,labels_f,trace_f,seqnum1)

print('ANED: ' + str(editAvg))
print('ANED2: ' + str(editAvg2))
print('ANHD: ' + str(hammingAvg))
print("ANLD: " + str(len_diff))
print('delta: ' + str(deltaAvg))
print( 'Region0: ' + str(avg0) )
print( 'Region1: ' + str(avg1) )
print( 'Region2: ' + str(avg2) )
print('Region3: ' + str(avg3) )

create_summary(editAvg, editAvg2, hammingAvg, deltaAvg, len_diff,avg0, avg1, avg2, avg3, seqnum1, outdir, mode, bias)
