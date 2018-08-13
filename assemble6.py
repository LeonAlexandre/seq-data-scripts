##The Assembler
##takes in the inference file and reassembles it

"""
TODo: Rework the reconstrutng function

Arguments:
Output directory
Inference file
Fragnum
"""




import argparse
import random
import math
import os
import numpy as np
import Levenshtein as lv
import scipy.special as spc
from scipy.interpolate import interp1d


def parse_arguments():
    """
    arguments: outdir, f_in, fragnum
    


    """
    ##PARSING THROUGH THE ARGUMENTS
    #initialize the parser
    parser = argparse.ArgumentParser()
    #Adding arguments
    #parser.add_argument("name", help="any help", type=str)
    #acces by args.name
    parser.add_argument('--outdir',dest="outdir",help='output directory', type=str,default='newdata')
    parser.add_argument('--f_inference',dest="f_in",help='inference input file location (Full path)',type=str,default='test_output.txt')
    parser.add_argument('--fragnum',dest="fragnum",help='number of fragments as int',type=int,default=1)
    parser.add_argument('--overlap', dest="overlap", help='overlap',type=float,default=0.1)
    parser.add_argument('--delta', dest="delta", help='delta', type=float, default=0.1 )
    parser.add_argument('--assembly',dest="assembly", help='super | inter', type=str, default='super')
    return parser.parse_args()


def generateAddArray(arr1, arr2):
    #generate the addition array
    u = min(len(arr1),len(arr2))
    arr1 = arr1[:u].astype(int)
    arr2 = arr2[:u].astype(int)
    
    fin = arr1 + arr2
    
    return(fin)


def hammingInterpolation(fin,x,y):

    betterList = []
    
    #interpolation method
    for i in range(len(fin)):       
        if fin[i] == 2:
            betterList.append(1)
        if fin[i] == 0:
            betterList.append(0)
    
        
    if len(betterList) < 2:
        inter = x.astype(int)
    else:
        x1 = np.linspace(-1, 1, num=len(betterList), endpoint=True)
        y1 = np.asarray(betterList)
    
    
    
        lin1 = np.linspace(-1,1,len(fin))

        f = interp1d(x1, y1, kind='nearest')
        x2 = np.asarray(lin1).astype(float)
        inter = f(x2)
        inter = inter.astype(int)
    
    
    
    return inter


def hammingSuperposition(fin,x,y):
    #superposition algorithm
    betterList = []
    prev = 0

    for i in range(len(fin)):
        if fin[i] == 1:
            if prev == x[i]:
                betterList.append(x[i])
                betterList.append(y[i])
                prev = y[i]
            elif prev == y[i]:
                betterList.append(y[i])
                betterList.append(x[i])
                prev = x[i]
            
        else:
            
            if fin[i] == 2:
                betterList.append(1)
            if fin[i] == 0:
                betterList.append(0)
            prev = fin[i]
    
    betterList = np.asarray(betterList).astype(int)

    return betterList


def find_overlap(length, delta, overlap):
    fraglen = int(  round(length / (1 + 2 * overlap) ))
    ov = int(fraglen * overlap)
    

    return(ov)


def create_file(outdir,assembly):
    
    #current = os.getcwd()
    #path = current + '/' + outdir
    path = outdir
    if not os.path.isdir(path):
        os.mkdir(path)
        print('Created Directory: ' + outdir)
    else:
        print('Directory ' + outdir + ' already exists!')

    f_out = open(path + '/recons_' + assembly + '.txt', "w+")

    return f_out


def listify(entry):
    return list(''.join(entry.split()))


def formatter(list_in):
    list_in = ' '.join(str(x) for x in list_in)
    return(list_in)


def inference_list(f_in,fragnum):
    #read lines in a lsit
    #split the list according to fragnum (list of list)
    __location__ = os.getcwd()
    inference_file = os.path.join(__location__,f_in)
    inference_file = open(f_in,'r')
    lines = inference_file.readlines()
    
    inf_list = []
    seqnum = int(len(lines) / fragnum)
    #should be a perfect multiple of fragments so no problem here 
    for i in range(seqnum):
        inf_list.append(lines[i * fragnum : (i + 1) * fragnum])
    for i in range(seqnum):
        for j in range(fragnum):
            inf_list[i][j] = listify(inf_list[i][j])



    return inf_list, seqnum


def assembler(fraglist,fragnum,delta,overlap,assembly):

    

    u = np.asarray(fraglist[ 0 ])
    for i in range(fragnum - 1):      
        
        v = np.asarray(fraglist[ i + 1 ])                  
        max_portion = find_overlap(len(v),delta,overlap)
        x = u[-max_portion:]
        y = v[:max_portion]
        fin = generateAddArray(x,y)
        if assembly=='inter':
            middle = hammingInterpolation(fin,x,y)
        elif assembly=='super':
            middle = hammingSuperposition(fin,x,y)
        u2 = u[:-max_portion]

        v2 = v[max_portion + 1 :]
        
        d = np.concatenate((u2,middle,v2),axis=0)
        u = np.copy(d)
    
    return  d


def reconstruct1(inf_list,seqnum,delta,overlap,assembly):
    reconstructed = ''
    for i in range(seqnum):
        reconstructed = reconstructed + "\n" + formatter(assembler(inf_list[i],fragnum,delta,overlap,assembly))
    #delete frist line
    reconstructed = reconstructed.split("\n",1)[1]

    return reconstructed


###MAIN CODE

args = parse_arguments()
outdir = args.outdir
f_in = args.f_in
fragnum = args.fragnum
overlap = args.overlap
delta = args.delta
assembly = args.assembly

#process input
inf_list, seqnum = inference_list(f_in,fragnum)
f_out = create_file(outdir,assembly)
reconstruct = reconstruct1(inf_list,seqnum,delta,overlap,assembly)
f_out.write(reconstruct)
f_out.close()



