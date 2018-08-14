##The ovelap analyzer
# Takes in inference file
# produces different outputs showcasing the overlap detected by each assembler
# saves and prints them in a human readable format
# compare to label
# give statistics
# 

"""
TODo: Rework the reconstrutng function

Arguments:
Output directory
Inference file
Labels
Frag labels
Fragnum

"""
##Add functions from report.py

import argparse
import random
import math
import os
import numpy as np
import Levenshtein as lv

def parse_arguments():
    """
    arguments: outdir, inference, fragnum, fragLabels, labels
    
    """
    ##PARSING THROUGH THE ARGUMENTS
    #initialize the parser
    parser = argparse.ArgumentParser()
    #Adding arguments
    #parser.add_argument("name", help="any help", type=str)
    #acces by args.name
    parser.add_argument('--outdir',dest="outdir",help='output directory', type=str,default='newdata')
    parser.add_argument('--inference',dest="inference",help='inference input file location (Full path)',type=str,default='test_output.txt')
    parser.add_argument('--fragnum',dest="fragnum",help='number of fragments as int',type=int,default=1)
    parser.add_argument('--mode',dest="mode",help='hamming | edit | both (default)', type=str, default='both' )
    parser.add_argument('--bias',dest="bias",help='sin (def) | log | logsin | sigmoid',type=str,default='sin')
    parser.add_argument('--fragLabels',dest="fragLabels", help='frag_x.label file',type=str,default='frag_test.label')
    parser.add_argument('--labels', dest='labels', help='x.label', type=str, default='test.label')
    parser.add_argument('--overlap', dest="overlap", help='overlap',type=float,default=0.1)
    parser.add_argument('--delta', dest="delta", help='delta', type=float, default=0.1 )
    return parser.parse_args()

def create_file(outdir,name):
    
    #current = os.getcwd()
    #path = current + '/' + outdir
    path = outdir
    if not os.path.isdir(path):
        os.mkdir(path)
        print('Created Directory: ' + outdir)
    else:
        print('Directory ' + outdir + ' already exists!')

    f_out = open(path + '/' + name + '.txt', "w+")

    return f_out

def listify(entry):
    return list(''.join(entry.split()))

def formatter(list_in):
    list_in = ' '.join(str(x) for x in list_in)
    return(list_in)

def create_list(f_in,fragnum):
    #read lines in a lsit
    #split the list according to fragnum (list of list)
    #current = os.getcwd()
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

def stringify(list_in):
  #Input:list
  #ouput: string
  return(''.join(str(x) for x in list_in))

def find_overlap(length, delta, overlap):
    fraglen = int(  round(length / (1 + 2 * overlap) ))
    ov = int(fraglen * overlap)
    

    return(ov)

#####ASSEMBLER 1 #################
#hamming score
def assembler_ham_ass1(fraglist,fragnum,bias):
    u = np.asarray(fraglist[ 0 ])
    pairs = []
    window = int(len(u))
    for i in range(fragnum - 1):
        sumlist = []
        
        v = np.asarray(fraglist[ i + 1 ])       
        
        for j in range(window)[1:] :
            w = u[-j:].astype(int)
            x = v[:j].astype(int)
            
            if bias=='sin':
                score_bias = math.sin((j * math.pi)/(window - 1))
            elif bias=='log': #log-bias
                score_bias = math.log(j + 1)/(math.log(window))
            elif bias=='logsin':
                score_bias = (math.sin((j * math.pi)/(window - 1)) + math.log(j + 1)/(math.log(window))) / 1.75
            elif bias=='sigmoid':
                score_bias=(1/(1 + math.exp(-j / (window/4.0))) - 0.55) * 2.0   
            elif bias=='tanh':
                score_bias= math.tanh(j/ (window *0.5))
            
            if w.size == x.size:
                score = ((1 - float(sum( (w + x) %2) )/ j)  * score_bias )
            else:
                score = 0

            
            sumlist.append(score)
        max_portion = sumlist.index(max(sumlist))
        pairs.append( ( formatter(u[-max_portion:]) , formatter(v[:max_portion])) )
        v2 = v[max_portion + 1 :]
        d = np.concatenate((u,v2))
        u = np.copy(d)
    return  pairs

#edit score
def assembler_edit_ass1(fraglist,fragnum,bias):
    pairs = [] 
    u = np.asarray(fraglist[ 0 ])
    window = int(len(u))
    for i in range(fragnum - 1):
        sumlist = []
           
        v = np.asarray(fraglist[ i + 1 ])                
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
            elif bias=='sigmoid':
                score_bias=(1/(1 + math.exp(-j / (window/4.0))) - 0.55) * 2.0
            elif bias=='tanh':
                score_bias= math.tanh(j/ (window *0.5))            
            score = (1 - float(lv.distance(str1,str2) / j))  * score_bias            
            sumlist.append(score)
        max_portion = sumlist.index(max(sumlist))
        pairs.append( ( formatter(u[-max_portion:]) , formatter(v[:max_portion])) )
        v2 = v[max_portion + 1 :]
        d = np.concatenate((u,v2))
        u = np.copy(d)

    
    return  pairs

#edit score
def reconstruct_edit_assembler1(inf_list,seqnum,bias):
    pairsList = []
    for i in range(seqnum):
        pairs = assembler_edit_ass1(inf_list[i],fragnum,bias)
        pairsList.append(pairs)
    #delete frist line

    return pairsList

def reconstruct_hamming_assembler1(inf_list,seqnum,bias):
    pairsList = []
    for i in range(seqnum):
        pairs = assembler_ham_ass1(inf_list[i],fragnum,bias)
        pairsList.append(pairs)
    #delete frist line

    return pairsList



######ASSEMBLER 2 ####################

def assembler_ass5(fraglist,fragnum,delta,overlap):
    pairs = []
    u = np.asarray(fraglist[ 0 ])
    for i in range(fragnum - 1):      
        v = np.asarray(fraglist[ i + 1 ])                  
        max_portion = find_overlap(len(v),delta,overlap)
        pairs.append( ( formatter(u[-max_portion:]) , formatter(v[:max_portion])) )
        v2 = v[max_portion + 1 :]
        d = np.concatenate((u,v2))
        u = np.copy(d)
    
    return  pairs


def reconstruct_ass5(inf_list,seqnum,delta,overlap):
    reconstructed = ''
    for i in range(seqnum):
        reconstructed = reconstructed + "\n" + formatter(assembler_ass5(inf_list[i],fragnum,delta,overlap))
    #delete frist line
    reconstructed = reconstructed.split("\n",1)[1]

    return reconstructed


####PAIR SCORE

#pair summary
def pair_report(pairs, seqnum, fragnum):
    #reports on metrics
    ANED = 0.0
    pair_string = ''
    ALEN = 0.0
    
    for i in range(seqnum):
        pair_string += 'Sequence:' + str(i) + '\n'
        for j in range(fragnum - 1):
            pair_string += 'Fragment:' + str(j) + '\n'

            str1 = pairs[i][j][0]
            str2 = pairs[i][j][1]
            str1.replace(' ','')
            str2.replace(' ','')
            LEN = len(str1)
            NED = lv.distance(str1,str2) / LEN
            

            pair_string += 'overlap1: ' + str1 + '\n'
            pair_string += 'overlap2: ' + str2 + '\n'
            pair_string += 'NED = ' + str(NED) + '\n'
            pair_string += 'LEN = ' + str(LEN) + '\n'

            ANED += NED
            ALEN += LEN
            

    ANED = (ANED / seqnum) / (fragnum - 1)
    ALEN = (ALEN / seqnum) / (fragnum - 1)
    header = ''
    header += '**********\nAVERAGE DATA\n********\n'
    header += 'ANED' + str(ANED) + '\n'
    header += 'ALEN'+ str(ALEN) + '\n'
    header += '***********************************'
    pair_string = header + pair_string

    return pair_string


###MAIN CODE


#parse arguments
args = parse_arguments()
outdir = args.outdir
inference = args.inference
fragnum = args.fragnum
mode = args.mode
bias = args.bias
overlap = args.overlap
delta = args.delta


#process input
inf_list, seqnum = create_list(inference, fragnum)

#analyze the data



p_ass1_out1 = create_file(outdir, 'edit_pairs_ass1')
p_ass1_out2 = create_file(outdir, 'ham_pairs_ass1')
p_ass5_out = create_file(outdir,'pairs_ass5')
pairs_ham_ass1 = reconstruct_hamming_assembler1(inf_list,seqnum,bias)
pairs_edit_ass1 = reconstruct_edit_assembler1(inf_list,seqnum,bias)

report_edit_ass1 = pair_report(pairs_edit_ass1, seqnum, fragnum)
report_ham_ass1 = pair_report(pairs_ham_ass1, seqnum, fragnum)
report_ass5 = pair_report()
p_ass1_out1.write(report_edit_ass1)
p_ass1_out2.write(report_ham_ass1)


p_ass1_out1.close()
p_ass1_out2.close()






