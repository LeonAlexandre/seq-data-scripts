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
    return parser.parse_args()


def find_overlap(length, overlap):

    fraglen = int(  round(length / (1 + 2 * overlap) ))
    ov = int(fraglen * overlap) * 2
    

    return(ov)


def find_overlap_last(length,overlap):
    fraglen = int(  round(length / (1 + overlap) ))
    ov = int(fraglen * overlap) * 2
    

    return(ov)


def create_file(outdir):
    
    #current = os.getcwd()
    #path = current + '/' + outdir
    path = outdir
    if not os.path.isdir(path):
        os.mkdir(path)
        print('Created Directory: ' + outdir)
    else:
        print('Directory ' + outdir + ' already exists!')

    f_out = open(path + '/recons' + '.txt', "w+")

    return f_out


def listify(entry):
    #from string to list
    return list(''.join(entry.split()))


def formatter(list_in):
    #formats the string to the network format
    list_in = ' '.join(str(x) for x in list_in)
    return(list_in)


def inference_list(f_in,fragnum):
    #read lines in a list
    #split the list according to fragnum (list of list)
    #results ina  three dimensional list. First level is by sequence number. Second level by fragment number. third level is the bit itself.
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


def assembler(fraglist,fragnum, overlap):

    

    u = np.asarray(fraglist[ 0 ])
    for i in range(fragnum - 2):      
        v = np.asarray(fraglist[ i + 1 ])                  
        max_portion = find_overlap(len(v), overlap)
        u2 = u[:-max_portion]
        
        d = np.concatenate((u2,v))
        u = np.copy(d)
    v = np.asarray(fraglist[ fragnum -1 ])                  
    max_portion = find_overlap_last(len(v), overlap)
    u2 = u[:-max_portion]
        
    d = np.concatenate((u2,v))
    u = np.copy(d)

    
    return  d


def assembler_no_overlap(fraglist,fragnum):

    u = np.asarray(fraglist[ 0 ])
    for i in range(fragnum - 2):      
        v = np.asarray(fraglist[ i + 1 ])                  
        d = np.concatenate((u,v))
        u = np.copy(d)
    v = np.asarray(fraglist[ fragnum -1 ])  
    d = np.concatenate((u,v))
    
    return  d


def reconstruct1(inf_list,seqnum,overlap):
    #reconstructs each sequence and adds it to an output string.
    #output is the formatted string or assembled sequences
    reconstructed = ''
    for i in range(seqnum):
        reconstructed = reconstructed + "\n" + formatter(assembler(inf_list[i],fragnum, overlap))
    #delete frist line
    reconstructed = reconstructed.split("\n",1)[1]

    return reconstructed

def reconstruct_no_overlap(inf_list,seqnum):
    #reconstructs each sequence and adds it to an output string.
    #output is the formatted string or assembled sequences
    reconstructed = ''
    for i in range(seqnum):
        reconstructed = reconstructed + "\n" + formatter(assembler_no_overlap(inf_list[i],fragnum))
    #delete frist line
    reconstructed = reconstructed.split("\n",1)[1]

    return reconstructed

###MAIN CODE

args = parse_arguments()
outdir = args.outdir
f_in = args.f_in
fragnum = args.fragnum
overlap = args.overlap


#process input
inf_list, seqnum = inference_list(f_in,fragnum)
f_out = create_file(outdir)
if overlap == 0.0:
    reconstruct_no_overlap(inf_list,seqnum)
else:
    reconstruct = reconstruct1(inf_list,seqnum, overlap)
f_out.write(reconstruct)
f_out.close()



