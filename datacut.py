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
    parser.add_argument('--indir',dest="indir",help='input directory(str)', type=str,default='newdata')
    parser.add_argument('--outdir',dest="outdir",help='output directory(str)', type=str,default='newdata')
    parser.add_argument('--num_traces',dest="num_traces",help='number of traces per sequence (int)',type=int,default=1)
    parser.add_argument('--fragnum',dest="fragnum",help='Number of fragments per sequence (int)',type=int,default=5)
    parser.add_argument('--overlap',dest="overlap",help='overlap rate of the fragments as 0.x (float)',type=float,default=0.1)

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

   
    


    return  f_frag_train_label , f_frag_train_trace, f_frag_val_label ,f_frag_val_trace ,f_frag_test_label, f_frag_test_trace


def listify(entry):
    return list(''.join(entry.split()))


def inference_list(prefix, suffix,indir):
    #read lines in a lsit
    #split the list according to fragnum (list of list)
    #current = os.getcwd()
    
    filename = indir + '/' + prefix+'.'+suffix
    inference_file = open(filename,'r')
    print('found file: ',filename)
    lines = inference_file.readlines()
    
    inf_list = []
    seqnum = len(lines)
    #should be a perfect multiple of fragments so no problem here 
    for i in range(seqnum):
        inf_list.append(listify(lines[i]))



    return inf_list


def cut_list(in_list,fragnum,overlap):
    #in_list: input list
    #fragnum
    #overlap

    #output in a nice format
        
    out_str = ''
    
    
    ####cutting      
    for i in range(len(in_list)):
        print(i)
        fragment_list = cut_data(in_list[i],fragnum,overlap)
        
        if not '' in fragment_list: #guards against empty fragments
            for j in range(fragnum):
                fragment = formater(fragment_list[j])
                out_str += '\n' + fragment
                
                          
    #delete first line
        
    out_str = out_str.split("\n",1)[1] + '\n'
    
    
    
        
    return out_str

#MAIN

#parse arguments
"""Args
indir
outdir
fragnum
num_traces
overlap
"""



args = parse_arguments()
outdir = args.outdir
fragnum = args.fragnum
indir = args.indir
num_traces = args.num_traces
overlap = args.overlap


#read data & listify
suffix= 'label'
in_train_label = inference_list('train', suffix, indir)
in_val_label = inference_list('val', suffix, indir)
in_test_label = inference_list('test', suffix, indir)

suffix = 'trace'
in_train_trace = inference_list('train', suffix, indir)
in_val_trace = inference_list('val', suffix, indir)
in_test_trace = inference_list('test', suffix, indir)


print('cutting data')

#cut data
frag_train_label = cut_list(in_train_label, fragnum, overlap)
frag_train_trace = cut_list(in_train_trace, fragnum, overlap)
frag_val_label = cut_list(in_val_label, fragnum, overlap)
frag_val_trace = cut_list(in_val_trace , fragnum, overlap)
frag_test_label = cut_list(in_test_label, fragnum, overlap)
frag_test_trace = cut_list(in_test_trace, fragnum, overlap)

print('creating files')
#create files
(f_frag_train_label , f_frag_train_trace, f_frag_val_label ,
f_frag_val_trace ,f_frag_test_label, f_frag_test_trace ) = create_files(outdir,num_traces,fragnum)


#write to file

print('writing to file')
f_frag_train_label.write(frag_train_label)
f_frag_val_label.write(frag_val_label)
f_frag_test_label.write(frag_test_label)

print(frag_val_trace)

if num_traces == 1:
    f_frag_train_trace[0].write(frag_train_trace)
    f_frag_val_trace[0].write(frag_val_trace)
    f_frag_test_trace[0].write(frag_test_trace)
else:
    print('not supported yet ;(')