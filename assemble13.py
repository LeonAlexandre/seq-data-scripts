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
    parser.add_argument('--mode',dest="mode",help='hamming | edit | both (default)', type=str, default='both' )
    parser.add_argument('--bias',dest="bias",help='sin (def) | log | logsin | prob',type=str,default='sin')
    parser.add_argument('--delta', dest="delta", help='deletion probabilty', type=float, default=0.1)
    parser.add_argument('--overlap', dest="overlap", help='overlap',type=float,default=0.1)
    return parser.parse_args()

def create_file(outdir,mode,bias):
    
    #current = os.getcwd()
    #path = current + '/' + outdir
    path = outdir
    if not os.path.isdir(path):
        os.mkdir(path)
        print('Created Directory: ' + outdir)
    else:
        print('Directory ' + outdir + ' already exists!')

    f_out = open(path + '/recons_' + mode + '_' +bias + '.txt', "w+")

    return f_out

def listify(entry):
    return list(''.join(entry.split()))

def formatter(list_in):
    list_in = ' '.join(str(x) for x in list_in)
    return(list_in)

def generate_prob(window, overlap, delta):
    x = range( window + 1 )
    temp=[]
    for i in x:       
        temp.append(  spc.comb(i,overlap) 
                    * math.pow(delta ,(i-overlap)) 
                    * math.pow((1-delta) ,overlap)  )
    return temp


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


def find_overlap(length, overlap, delta):

    fraglen = int(round((length / (1 - delta))  / (1 + 2 * overlap))  )
    ov = int(fraglen * overlap) * 2
    return(ov)


#hamming score
def assembler_ham(fraglist,fragnum,bias ,delta,overlap):

    u = np.asarray(fraglist[ 0 ])
    
    window = int(len(u) )
    for i in range(fragnum - 1):
        sumlist = []
        
        v = np.asarray(fraglist[ i + 1 ])

        ov = find_overlap(len(v), overlap, delta)
        prob = generate_prob(window , ov , delta)
        
        for j in range(window)[1:] :
            w = u[-j:].astype(int)
            x = v[:j].astype(int)
            
            if bias=='sin':
                score_bias = math.sin((j * math.pi)/(window - 1))
            elif bias=='log': #log-bias
                score_bias = math.log(j + 1)/(math.log(window))
            elif bias=='logsin':
                score_bias = (math.sin((j * math.pi)/(window - 1)) + math.log(j + 1)/(math.log(window))) / 1.75
            elif bias=='prob':
                score_bias=prob[j] * j
                
            
            if w.size == x.size:
                score = ((1 - float(sum( (w + x) %2) )/ j)  * score_bias )
            else:
                score = 0

            sumlist.append(score)
                    
        max_portion = sumlist.index(max(sumlist))
        #if bias=='prob':
        #    max_portion += 1
            #print(max_portion)
       
        u2 = u[:-max_portion]
        d = np.concatenate((u2,v))
        u = np.copy(d)
    
    return  d

#hamming score
def reconstruct1(inf_list,seqnum,bias, delta,overlap):
    reconstructed = ''
    for i in range(seqnum):
        reconstructed = reconstructed + "\n" + formatter(assembler_ham(inf_list[i],fragnum,bias, delta, overlap))
    #delete frist line
    reconstructed = reconstructed.split("\n",1)[1]

    return reconstructed


#edit score
def assembler_edit(fraglist,fragnum,bias, delta,overlap):


    u = np.asarray(fraglist[ 0 ])
    window = int(math.ceil(len(u) ))
    
    for i in range(fragnum - 1):
        sumlist = []
        
            
        v = np.asarray(fraglist[ i + 1 ])
        ov = find_overlap(len(v), overlap, delta)
        
        prob = generate_prob(window , ov , delta)
        
        
        for j in range(window)[1:] :
            #isolate section
            array1 = u[-j:].astype(str)
            array2 = v[:j].astype(str)
            #convert to list then string
            str1 = ''.join(array1.tolist())
            str2 = ''.join(array2.tolist())

            if bias=='sin':
                score_bias = math.sin((j * math.pi)/(window - 1))
            elif bias=='log': #log-bias
                score_bias = math.log(j + 1)/(math.log(window))
            elif bias=='logsin':
                score_bias = (math.sin((j * math.pi)/(window - 1)) + math.log(j + 1)/(math.log(window))) / 1.75
            elif bias=='prob':
                score_bias = prob[j] * j
                

            score = (1 - float(lv.distance(str1,str2) / j))  * score_bias
            
            sumlist.append(score)

        max_portion = sumlist.index(max(sumlist)) 
        print(max_portion)
        #if bias=='prob':
        #    max_portion +=1
            #print(max_portion)
        
        u2 = u[:-max_portion]
        d = np.concatenate((u2,v))
        u = np.copy(d)
    
    return  d

#edit score
def reconstruct2(inf_list,seqnum,bias,delta,overlap):
    reconstructed = ''
    for i in range(seqnum):
        reconstructed = reconstructed + "\n" + formatter(assembler_edit(inf_list[i],fragnum,bias, delta, overlap))
    #delete frist line
    reconstructed = reconstructed.split("\n",1)[1]

    return reconstructed

###MAIN CODE

if __name__ == '__main__':
    args = parse_arguments()
    outdir = args.outdir
    f_in = args.f_in
    fragnum = args.fragnum
    mode = args.mode
    bias = args.bias
    delta = args.delta
    overlap = args.overlap

    #process input
    inf_list, seqnum = inference_list(f_in,fragnum)
    if mode=='both':
        f_out1 = create_file(outdir,'hamming',bias)
        reconstructed1 = reconstruct1(inf_list,seqnum,bias,delta,overlap)
        reconstructed2 = reconstruct2(inf_list,seqnum,bias, delta,overlap)
        f_out2 = create_file(outdir,'edit',bias)
        f_out1.write(reconstructed1)
        f_out2.write(reconstructed2)
        f_out1.close()
        f_out2.close()

    else:
        f_out = create_file(outdir,mode,bias)
        if mode=='hamming':
            reconstruct = reconstruct1(inf_list,seqnum,bias,delta,overlap)
        elif mode=='edit':
            reconstruct = reconstruct2(inf_list,seqnum,bias,delta,overlap)
        f_out.write(reconstruct)
        f_out.close()
