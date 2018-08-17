##The ovelap analyzer
# Takes in inference file
# produces different outputs showcasing the overlap detected by each assembler
# saves and prints them in a human readable format
# compare to label
# give statistics
# 

"""

Arguments:
Output directory
Inference file
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
    parser.add_argument('--fragLabels',dest="fragLabels", help='frag_x.label file',type=str,default='frag_test.label')
    parser.add_argument('--overlap', dest="overlap", help='overlap',type=float,default=0.1)
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

def find_overlap(length,  overlap):
    fraglen = int(  round(length / (1 + (2 * overlap) )))
    
    ov = int(fraglen * overlap ) *2
    

    return(ov)

def find_overlap_last(length,overlap):
    fraglen = int(  round(length / (1 + overlap) ))
    ov = int(fraglen * overlap) * 2
    

    return(ov)


#####ASSEMBLER 1 #################
#hamming score
def assembler_ham_ass7(fraglist,fragnum):
    
    u = np.asarray(fraglist[ 0 ])
    pairs = []
    window = int(len(u))
    for i in range(fragnum - 1):
        sumlist = []
        
        v = np.asarray(fraglist[ i + 1 ])       
        
        for j in range(window)[1:] :
            w = u[-j:].astype(int)
            x = v[:j].astype(int)
            
            
            score_bias = math.sin((j * math.pi)/(window - 1))
            
            
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
def assembler_edit_ass7(fraglist,fragnum):
    
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
            score_bias = math.sin((j * math.pi)/(window - 1))
                       
            score = (1 - float(lv.distance(str1,str2) / j))  * score_bias            
            sumlist.append(score)
        max_portion = sumlist.index(max(sumlist))
        pairs.append( ( formatter(u[-max_portion:]) , formatter(v[:max_portion])) )
        v2 = v[max_portion + 1 :]
        d = np.concatenate((u,v2))
        u = np.copy(d)

    
    return  pairs

#edit score
def reconstruct_edit_assembler7(inf_list,seqnum):
    pairsList = []
    for i in range(seqnum):
        pairs = assembler_edit_ass7(inf_list[i],fragnum)
        pairsList.append(pairs)

    return pairsList

def reconstruct_hamming_assembler7(inf_list,seqnum):
    pairsList = []
    for i in range(seqnum):
        pairs = assembler_ham_ass7(inf_list[i],fragnum)
        pairsList.append(pairs)

    return pairsList



######ASSEMBLER 2 ####################

def assembler_ass5(fraglist,fragnum, overlap):
    pairs = []

    u = np.asarray(fraglist[ 0 ])
    for i in range(fragnum - 1):      
        v = np.asarray(fraglist[ i + 1 ])
        max_portion = find_overlap(len(v), overlap)
        pairs.append( ( formatter(u[-max_portion:]) , formatter(v[:max_portion])) )
        
        u = np.copy(v)
    
    return  pairs

def assembler_ass11(fraglist,fragnum, overlap):
    pairs = []
    

    u = np.asarray(fraglist[ 0 ])
    for i in range(fragnum - 2):      
        v = np.asarray(fraglist[ i + 1 ])                  
        max_portion = find_overlap(len(v), overlap)
        u2 = u[:-max_portion]
        
        d = np.concatenate((u2,v))
        u = np.copy(d)
        pairs.append( ( formatter(u[-max_portion:]) , formatter(v[:max_portion])) )
    v = np.asarray(fraglist[ fragnum -1 ])                  
    max_portion = find_overlap_last(len(v), overlap)
    u2 = u[:-max_portion]
    pairs.append( ( formatter(u[-max_portion:]) , formatter(v[:max_portion])) )
    d = np.concatenate((u2,v))
    u = np.copy(d)

    
    return  pairs

def reconstruct_ass5(inf_list,seqnum, fragnum ,overlap):
    pairsList = []
    for i in range(seqnum):
        pairs = assembler_ass5(inf_list[i],fragnum, overlap)
        pairsList.append(pairs)

    return pairsList

def reconstruct_ass11(inf_list,seqnum, fragnum ,overlap):
    pairsList = []
    for i in range(seqnum):
        pairs = assembler_ass11(inf_list[i],fragnum, overlap)
        pairsList.append(pairs)

    return pairsList
###Find original overlap regions
#use find_overlap
#take from the frag_label
#give score on each string to see if a trend emerges (ie what to take into account)

def find_original(fraglist,fragnum, overlap):
    over = []
    
    for i in range(fragnum - 1):      
        v = np.asarray(fraglist[ i + 1 ])                  
        max_portion = find_overlap(len(v), overlap)
        over.append( formatter( v[:max_portion] ) )
        
    
    return  over


def original_list(in_list,seqnum,overlap):
    overlapList = []
    for i in range(seqnum):
        overlapList.append(find_original(in_list[i],fragnum, overlap) )
    

    return overlapList



####PAIR SCORE

#pair summary
def pair_report(pairs, label_list, seqnum, fragnum):
    #reports on metrics
    MANED = 0.0
    pair_string = ''
    AOLEN = 0.0
    AED1 = 0.0
    AED2 = 0.0
    
    for i in range(seqnum):
        pair_string += 'Sequence:' + str(i) + '\n'
        for j in range(fragnum - 1):
            pair_string += 'Fragment:' + str(j) + '\n'

            lab = label_list[i][j]
            str1 = pairs[i][j][0]
            str2 = pairs[i][j][1]
            labs = lab.replace(' ','')
            str1s = str1.replace(' ','')
            str2s = str2.replace(' ','')
            OLEN = len(str1s)
            MNED = lv.distance(str1s,str2s) / OLEN
            ED1 = lv.distance(labs, str1s) / len(labs)
            ED2 = lv.distance(labs,str2s) / len(labs)

            

            pair_string += 'overlap1: ' + str1 + '\n'
            pair_string += 'overlap2: ' + str2 + '\n'
            pair_string += 'original: ' + lab + '\n'
            pair_string += 'MNED = ' + str(MNED) + '\n'
            pair_string += 'OLEN = ' + str(OLEN) + '\n'
            pair_string += 'ED1 = ' + str(ED1) + '\n'
            pair_string += 'ED2 = ' + str(ED2) + '\n'

            MANED += MNED
            AOLEN += OLEN
            AED1 += ED1
            AED2 += ED2
            

    MANED = (MANED / seqnum) / (fragnum - 1)
    AOLEN = (AOLEN / seqnum) / (fragnum - 1)
    AED1 = (AED1 / seqnum) / (fragnum - 1)
    AED2 = (AED2 / seqnum) / (fragnum - 1)

    header = ''
    header += '**********\nAVERAGE DATA\n********\n'
    header += 'MANED = ' + str(MANED) + '   mutual edit distance (avg)' +'\n'
    header += 'AOLEN = '+ str(AOLEN) +  '   len of overlap (avg)' + '\n'
    header += 'AED1 = ' + str(AED1) + '    avg edit distance between label and frag 1' + '\n'
    header += 'AED2 = ' + str(AED2) + '    avg edit distance between label and frag 2' + '\n'

    header += '***********************************'
    pair_string = header + pair_string

    return pair_string


###MAIN CODE


#parse arguments
args = parse_arguments()
outdir = args.outdir
inference = args.inference
fragnum = args.fragnum

overlap = args.overlap
fragLabels = args.fragLabels


#process input
inf_list, seqnum = create_list(inference, fragnum)
frag_labels, seqnum2 = create_list(fragLabels,fragnum)

#analyze the data

#labels
label_list = original_list(frag_labels, seqnum, overlap)

#differnt assemblers
"""
p_ass7_out1 = create_file(outdir, 'edit_pairs_ass7')
p_ass7_out2 = create_file(outdir, 'ham_pairs_ass7')
p_ass5_out = create_file(outdir,'pairs_ass5')
"""
p_ass11_out = create_file(outdir,'pairs_ass11')
"""
pairs_ham_ass7 = reconstruct_hamming_assembler7(inf_list,seqnum)
pairs_edit_ass7 = reconstruct_edit_assembler7(inf_list,seqnum)
pairs_ass5 = reconstruct_ass5(inf_list, seqnum, fragnum, overlap)
"""
pairs_ass11 = reconstruct_ass11(inf_list, seqnum, fragnum, overlap)

"""
report_edit_ass7 = pair_report(pairs_edit_ass7, label_list, seqnum, fragnum)
report_ham_ass7 = pair_report(pairs_ham_ass7, label_list, seqnum, fragnum)
report_ass5 = pair_report(pairs_ass5, label_list, seqnum, fragnum)
"""
report_ass11 = pair_report(pairs_ass11, label_list, seqnum, fragnum)

"""
p_ass7_out1.write(report_edit_ass7)
p_ass7_out2.write(report_ham_ass7)
p_ass5_out.write(report_ass5)
"""
p_ass11_out.write(report_ass11)

"""
p_ass7_out1.close()
p_ass7_out2.close()
p_ass5_out.close()
"""
p_ass11_out.close()




