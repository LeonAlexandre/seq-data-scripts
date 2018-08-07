#Cut pregenerated data


import argparse
import random
import math
import os


#Parser 
def parse_arguments():
    """
    arguments: outdir, seqLength,alphabet_size,delta,numSeq,num_traces,train_size,val_size,fragnum,overlap
    args: range_mode start_len end_len step 


    """
    ##PARSING THROUGH THE ARGUMENTS
    #initialize the parser
    parser = argparse.ArgumentParser()
    #acces by args.name
    parser.add_argument('--outdir',dest="outdir",help='output directory(str)', type=str,default='newdata')
    parser.add_argument('--seqLength',dest="seqLength",help='length of original sequence(int)',type=int,default=100)
    parser.add_argument("--alphabetSize",dest="alphabet_size" ,help="alphabet size (int)",type=int,default=2)
    parser.add_argument('--delta',dest="delta",help='deletion probability (float)',type=float,default=0)
    parser.add_argument('--numSeq',dest="numSeq",help='number of original sequences (int)',type=int,default=100)
    parser.add_argument('--num_traces',dest="num_traces",help='number of traces per sequence (int)',type=int,default=1)
    parser.add_argument('--train_size',dest="train_size",help='percentage of numSeq in the training set as 0.x (float)',type=float,default=0.6)
    parser.add_argument('--val_size',dest="val_size",help='percentage of numSeq in the validation set as 0.x (float)',type=float,default=0.2)
    parser.add_argument('--fragnum',dest="fragnum",help='Number of fragments per sequence (int)',type=int,default=5)
    parser.add_argument('--overlap',dest="overlap",help='overlap rate of the fragments as 0.x (int)',type=float,default=0.1)
    parser.add_argument('--ranged_mode',dest="ranged_mode",help='Enables ranged mode (bool)',type=bool,default=False)
    parser.add_argument('--start_len',dest="start_len",help='starting length (int)',type=int,default=100)
    parser.add_argument('--end_len',dest="end_len",help='ending length(int)',type=int,default=100)
    parser.add_argument('--step',dest="step",help='step size wthin range (int)',type=int,default=1)

    return parser.parse_args()

def formater(list_in):
    list_in = ' '.join(str(x) for x in list_in)
    return(list_in)


def cut_data(label,fragnum,overlap):
    portion = int(math.floor(len(label) / fragnum))
    ov = int(math.ceil(portion * overlap))
    
    fraglabel = []
    fraglabel.append(label[0:portion + ov])
    
    for i in range(fragnum)[1: fragnum - 1]:
        fraglabel.append(label[(i * portion) - ov: ((i+1) * portion) + ov])
    fraglabel.append(label[(fragnum -1) * portion :])
    #alt
    #fraglabel.append(label[(fragnum -1) * portion - ov:])
        
    #portion = int(math.ceil(len(trace) / fragnum))
    #ov = int(math.ceil(portion * overlap))
    
    #fragtrace = []
    #fragtrace.append(trace[0:portion + ov])
    
    #for i in range(fragnum)[1: fragnum -1]:
    #    fragtrace.append(trace[(i * portion) - ov : ((i+1) * portion) + ov])
    #fragtrace.append(trace[(fragnum -1) * portion :])
    
    return fraglabel #, fragtrace

def create_files(out_dir,num_traces,fragnum):
    """
    Creates files for each string returned by the generator
    (f_train_label, f_train_trace, f_val_label, f_val_trace, f_test_label, f_test_trace, f_frag_train_label ,
    f_frag_train_trace, f_frag_val_label ,f_frag_val_trace ,f_frag_test_label, f_frag_test_trace )

    """
    #find dir
    #current = os.getcwd()
    #path = current + '/' +out_dir
    path=out_dir
    try:  
        os.mkdir(path)
    except OSError:  
        print("Creation of the directory %s failed" % path)
    else:  
        print("Successfully created the directory %s " % path)
    #dirpath = path + '/'
    dirpath= out_dir + '/'

    #Basic files
    #LABELS
    f_train_label = open(dirpath + "train.label","w+")
    f_val_label = open(dirpath +"val.label","w+")
    f_test_label = open(dirpath +"test.label","w+")

    #TRACES
    f_train_trace = [''] * num_traces
    f_val_trace = [''] * num_traces
    f_test_trace = [''] * num_traces
    if num_traces == 1:
        name = dirpath + "train.trace" 
        f_train_trace[0] = open(name ,"w+")
        name = dirpath + "val.trace"
        f_val_trace[0] = open(name ,"w+")
        name = dirpath + "test.trace"
        f_test_trace[0] = open(name ,"w+")
    else:
        for i in range(num_traces):
            name = dirpath + "train.trace" + str(i)
            f_train_trace[i] = open(name ,"w+")
            name = dirpath + "val.trace" + str(i)
            f_val_trace[i] = open(name ,"w+")
            name = dirpath + "test.trace" + str(i)
            f_test_trace[i] = open(name ,"w+")
    
    #Fragmented
    #LABELS
    f_frag_train_label = open(dirpath + 'frag_train.label', "w+")
    f_frag_val_label = open(dirpath + 'frag_val.label', "w+")
    f_frag_test_label = open(dirpath + 'frag_test.label', "w+")
    #TRACES
    f_frag_train_trace = [''] * num_traces
    f_frag_val_trace = [''] * num_traces
    f_frag_test_trace = [''] * num_traces

    if num_traces == 1:
        name = dirpath + 'frag_train.trace' 
        f_frag_train_trace[0] = open(name,"w+")
        name = dirpath + 'frag_val.trace' 
        f_frag_val_trace[0] = open(name, "w+")
        name = dirpath + 'frag_test.trace'
        f_frag_test_trace[0] = open(name, "w+")
    else:
        for i in range(num_traces):
            name = dirpath + 'frag_train.trace' + str(i)
            f_frag_train_trace[i] = open(name,"w+")
            name = dirpath + 'frag_val.trace' + str(i)
            f_frag_val_trace[i] = open(name, "w+")
            name = dirpath + 'frag_test.trace' + str(i)
            f_frag_test_trace[i] = open(name, "w+")

   
    


    return f_train_label, f_train_trace, f_val_label, f_val_trace, f_test_label, f_test_trace, f_frag_train_label , f_frag_train_trace, f_frag_val_label ,f_frag_val_trace ,f_frag_test_label, f_frag_test_trace




def inference_list(prefix, suffix,fragnum):
    #read lines in a lsit
    #split the list according to fragnum (list of list)
    #current = os.getcwd()
    filename = prefix+'.'+suffix
    inference_file = open(filename,'r')
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

#MAIN

#parse arguments
"""Args
outdir
input file (each tagged)
fragnum


"""



args = parse_arguments()
outdir = args.outdir
f_in = args.f_in
fragnum = args.fragnum


#read data
with suffix as 'label':
    in_train_label = inference_list('train', suffix,fragnum)
    in_val_label = inference_list('val', suffix, fragnum)
    in_test_label = inference_list('test', suffix, fragnum)

with suffix as 'trace':
    in_train_trace = inference_list('train', suffix,fragnum)
    in_val_trace = inference_list('val', suffix, fragnum)
    in_test_trace = inference_list('test', suffix, fragnum)

fragnum = args.fragnum

#process input
#listify the lines
inf_list, seqnum = inference_list(f_in,fragnum)



#cut data

#create files

#write to file