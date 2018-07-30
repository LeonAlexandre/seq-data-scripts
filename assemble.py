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
    parser.add_argument("outdir",help='output directory', type=str)
    parser.add_argument("f_in",help='inference input file location',type=str)
    parser.add_argument("fragnum",help='number of fragments as int',type=int)

    return parser.parse_args()

def create_file(outdir):
    
    current = os.getcwd()
    path = current + '/' + outdir
    if not os.path.isdir(path):
        os.mkdir(path)
        print('Created Directory: ' + outdir)
    else:
        print('Directory ' + outdir + ' already exists!')

    f_out = open(path + '/reconstructed.txt', "w+")

    return f_out

def listify(entry):
    return list(''.join(entry.split()))

def formatter(list_in):
    list_in = ' '.join(str(x) for x in list_in)
    return(list_in)


def inference_list(f_in,fragnum):
    #read lines in a lsit
    #split the list according to fragnum (list of list)
    current = os.getcwd()
    inference_file = open(current + f_in,'r')
    lines = inference_file.readlines()

    inf_list = []
    seqnum = int(len(lines) / fragnum)
    #should be a perfect multiple of fragments so no problem here 
    print(lines)
    for i in range(seqnum):
        inf_list.append(lines[i * fragnum : (i + 1) * fragnum])
    print('clic')
    print(inf_list)
    for i in range(seqnum):
        for j in range(fragnum):
            print(i,j)
            inf_list[i][j] = listify(inf_list[i][j])



    return inf_list, seqnum

def assembler(fraglist,fragnum):


    #score_bias = 0.5
    

    u = np.asarray(fraglist[ 0 ])
    window = int(math.ceil(len(u) * 0.5))
    print(window)
    for i in range(fragnum - 1):
        sumlist = []
        
        v = np.asarray(fraglist[ i + 1 ])
        
        
        for j in range(window)[1:] :
            w = u[-j:].astype(int)
            x = v[:j].astype(int)
            #score = (1 - float(sum( (w + x) %2) )/ i) * float(i * score_bias)
            score = (1 - float(sum( (w + x) %2) )/ j)  * math.sin((j * math.pi)/(window - 1))
            #score = (1 - float(sum( (w + x) %2) )/ j)  * math.sin((j * math.pi)/(window ))
            
            sumlist.append(score)

                    
        max_portion = sumlist.index(max(sumlist))
        print(sumlist)
        print(max_portion)
        v2 = v[max_portion + 1 :]
        d = np.concatenate((u,v2))
        u = np.copy(d)
    
    return  d

def reconstruct(inf_list,seqnum):
    reconstructed = ''
    for i in range(seqnum):
        reconstructed = reconstructed + "\n" + formatter(assembler(inf_list[i],fragnum))
    #delete frist line
    reconstructed = reconstructed.split("\n",1)[1]

    return reconstructed


###MAIN CODE


args = parse_arguments()
outdir = args.outdir
f_in = args.f_in
fragnum = args.fragnum

#process input

inf_list, seqnum = inference_list(f_in,fragnum)


reconstructed = reconstruct(inf_list,seqnum)


outdir = 'my_dir'

f_out = create_file(outdir)

f_out.write(reconstructed)

f_out.close()
