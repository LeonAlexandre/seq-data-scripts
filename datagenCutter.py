#Cutter program
#generates a multi trace dataset
#generates files that are cut and the originals with them
#outputs a report on the data set

"""
args: out_dir
args: seqlenght, alphabet, delta, 
    size, train_split, val_split , fragnum, overlap
#arguments for the ranged version
args: range_mode start_len end_len step

"""
#Imports
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
    parser.add_argument('--out_dir',dest="outdir",help='output directory(str)', type=str,default='newdata')
    parser.add_argument('--seqLength',dest="seqLength",help='length of original sequence(int)',type=int,default=100)
    parser.add_argument("--alphabetSize",dest="alphabet_size" ,help="alphabet size (int)",type=int,default=2)
    parser.add_argument('--delta',dest="delta",help='deletion probability (float)',type=float,default=0)
    parser.add_argument('--numSeq',dest="numSeq",help='number of original sequences (int)',type=int,default=100)
    parser.add_argument('--numTraces',dest="num_traces",help='number of traces per sequence (int)',type=int,default=1)
    parser.add_argument('--train_size',dest="train_size",help='percentage of numSeq in the training set as 0.x (float)',type=float,default=0.6)
    parser.add_argument('--val_size',dest="val_size",help='percentage of numSeq in the validation set as 0.x (float)',type=float,default=0.2)
    parser.add_argument('--fragNum',dest="fragnum",help='Number of fragments per sequence (int)',type=int,default=5)
    parser.add_argument('--overlap',dest="overlap",help='overlap rate of the fragments as 0.x (int)',type=float,default=0.1)
    parser.add_argument('--ranged_mode',dest="ranged_mode",help='Enables ranged mode (bool)',type=bool,default=False)
    parser.add_argument('--start_len',dest="start_len",help='starting length (int)',type=int,default=100)
    parser.add_argument('--end_len',dest="end_len",help='ending length(int)',type=int,default=100)
    parser.add_argument('--step',dest="step",help='step size wthin range (int)',type=int,default=1)

    return parser.parse_args()

# create random sequence
def randomSequence(seqLength,alphabet_size):
    '''
    Args:
        seqLength: length of desired randome sequence
        alphabet_size: number of symbols in the alphabet making up the sequence
    Returns:
        outputSeq: a numpy array of random 'int's, each row is a random sequence as a column vector
    '''
    outputSeq = []
    for x in range(seqLength):
        outputSeq.append(random.randint(0,alphabet_size-1))
    return outputSeq

def deletionChannel (inputSeq, delta):
    '''
    Args: 
        inputSeq: sequence to pass into the channel
        delta: a percentage probability with which symbols are randomly deleted
    Returns:
        ouputSeq: the input sequence with symbols deleted according to delta
    '''
    toDelete = []
    for x in range(len(inputSeq)):
        k = random.random()
        toDelete.append(k < delta)
    outputSeq = [i for indx,i in enumerate(inputSeq) if toDelete[indx] == False]
    return outputSeq

#converts to format suiting nmt
def formater(list_in):
    list_in = ' '.join(str(x) for x in list_in)
    return(list_in)

#The Cutter
#fragnum : number of fragments
#overlap : percentage of the fragment that is overlapping as 0.X

#def cut_data(label,trace,fragnum,overlap):

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

#output: -files containing the intact sequences and intact traces
# - lists of files containing fragmented versions that are coded

"""
Returns:
(train_label, train_trace, val_label, val_trace, test_label, test_trace, frag_train_label ,
 frag_train_trace, frag_val_label ,frag_val_trace ,frag_test_label, frag_test_trace )

"""
def generate_cut_strings(args):
    
    #previous args
    seqLength = args.seqLength
    alphabet_size = args.alphabet_size
    delta = args.delta
    numSeq = args.numSeq
    num_traces = args.num_traces
    train_size = args.train_size
    val_size = args.val_size
    fragnum =args.fragnum
    overlap = args.overlap
    
    
    #time to generalize this baby
    train_label = ''
    train_trace = [''] * num_traces
    val_label = ''
    val_trace = [''] * num_traces
    test_label = ''
    test_trace = [''] * num_traces
    
    frag_train_label = ''
    frag_train_trace = [''] * num_traces
 

    frag_val_label = ''
    frag_val_trace = [''] * num_traces
    
    frag_test_label = ''
    frag_test_trace = [''] * num_traces
    #frag_test_trace = [''] * fragnum
    
    ####TRAIN        
    for i in range(int(numSeq*train_size)):
        #intact
        label = randomSequence(seqLength,alphabet_size)
        #generate a list of traces
        trace = [''] * num_traces
        for i in range(num_traces):
            trace[i] = deletionChannel(label,delta)
        
        #fragmented
        fragtrace = [''] * num_traces
        
        fraglabel = cut_data(label,fragnum,overlap)
        for i in range(num_traces):
            fragtrace[i] = cut_data(trace[i],fragnum,overlap)
        
        #generate intact 'file' (really just a string)
        
        if not '' in trace:
            label = formater(label)
            train_label = train_label + '\n' + label
            for i in range(num_traces):
                trace[i] = formater(trace[i])                
                train_trace[i] = train_trace[i] + '\n' + trace[i]
        
        
        keep = True
        #generate a list with all the fragments
        if not '' in trace:
            #keep = False
            for x in range(len(fragtrace)):
                if  '' in fragtrace[x] :
                    keep = False
        
        if keep:
            
            for i in range(fragnum):
                    frag_train_label = frag_train_label + '\n' + formater(fraglabel[i])
                    for j in range(num_traces):
                        frag_train_trace[j] = frag_train_trace[j] + '\n' + formater(fragtrace[j][i])
          

    #####EVAL   
    for i in range(int(numSeq*val_size)):
        #intact
        label = randomSequence(seqLength,alphabet_size)
        #generate a list of traces
        trace = [''] * num_traces
        for i in range(num_traces):
            trace[i] = deletionChannel(label,delta)
        
        #fragmented
        fragtrace = [''] * num_traces
        
        fraglabel = cut_data(label,fragnum,overlap)
        for i in range(num_traces):
            fragtrace[i] = cut_data(trace[i],fragnum,overlap)
        

        #generate intact 'file' (really just a string)
        
        if not '' in trace:
            label = formater(label)
            val_label = val_label + '\n' + label
            for i in range(num_traces):
                trace[i] = formater(trace[i])                
                val_trace[i] = val_trace[i] + '\n' + trace[i]
        
        keep = True
        #generate a list with all the fragments
        if not '' in trace:
            #keep = False
            for x in range(len(fragtrace)):
                if  '' in fragtrace[x] :
                    keep = False
                
        
        if keep:
            
            for i in range(fragnum):
                    frag_val_label = frag_val_label + '\n' + formater(fraglabel[i])
                    for j in range(num_traces):
                        frag_val_trace[j] = frag_val_trace[j] + '\n' + formater(fragtrace[j][i])


    ####TEST   
    for i in range(int(numSeq*(1 - val_size - train_size))):
        #intact
        label = randomSequence(seqLength,alphabet_size)
        #generate a list of traces
        trace = [''] * num_traces
        for i in range(num_traces):
            trace[i] = deletionChannel(label,delta)
        
        #fragmented
        fragtrace = [''] * num_traces
        
        fraglabel = cut_data(label,fragnum,overlap)
        for i in range(num_traces):
            fragtrace[i] = cut_data(trace[i],fragnum,overlap)

        
        #generate intact 'file' (really just a string)
        
        if not '' in trace:
            label = formater(label)
            test_label = test_label + '\n' + label
            for i in range(num_traces):
                trace[i] = formater(trace[i])                
                test_trace[i] = test_trace[i] + '\n' + trace[i]
        
        
        keep = True
        #generate a list with all the fragments
        if not '' in trace:
            #keep = False
            for x in range(len(fragtrace)):
                if  '' in fragtrace[x] :
                    keep = False
        
        if keep:
            
            for i in range(fragnum):
                    frag_test_label = frag_test_label + '\n' + formater(fraglabel[i])
                    for j in range(num_traces):
                        frag_test_trace[j] = frag_test_trace[j] + '\n' + formater(fragtrace[j][i])
            
            
            
    #delete first line
    
    for i in range(num_traces):
        train_trace[i] = train_trace[i].split("\n",1)[1] + '\n'
        frag_train_trace[i] = frag_train_trace[i].split("\n",1)[1] + '\n'
        frag_val_trace[i] = frag_val_trace[i].split("\n",1)[1] + '\n'
        val_trace[i] = val_trace[i].split("\n",1)[1] + '\n'
        frag_test_trace[i] = frag_test_trace[i].split("\n",1)[1] + '\n'
        test_trace[i] = test_trace[i].split("\n",1)[1] + '\n'
    
    train_label = train_label.split("\n",1)[1] + '\n'
    val_label = val_label.split("\n",1)[1] + '\n'
    test_label = test_label.split("\n",1)[1] + '\n'
    
    frag_train_label = frag_train_label.split("\n",1)[1] + '\n'
    frag_val_label = frag_val_label.split("\n",1)[1] + '\n'
    frag_test_label = frag_test_label.split("\n",1)[1] + '\n'
    
    
        
    return (train_label, train_trace, val_label, val_trace, test_label, test_trace, frag_train_label ,frag_train_trace,
        frag_val_label ,frag_val_trace ,frag_test_label, frag_test_trace  )

def generate_cut_strings_ranged(args):
    #unpack arguments
    #previous args
    alphabet_size = args.alphabet_size
    delta = args.delta
    numSeq = args.numSeq
    num_traces = args.num_traces
    train_size = args.train_size
    val_size = args.val_size
    fragnum =args.fragnum
    overlap = args.overlap

    start_len = args.start_len
    end_len = args.end_len
    step = args.step
    
    #time to generalize this baby
    train_label = ''
    train_trace = [''] * num_traces
    val_label = ''
    val_trace = [''] * num_traces
    test_label = ''
    test_trace = [''] * num_traces
    
    frag_train_label = ''
    frag_train_trace = [''] * num_traces
 

    frag_val_label = ''
    frag_val_trace = [''] * num_traces
    
    frag_test_label = ''
    frag_test_trace = [''] * num_traces

    #make a progressions cheme
    pieceNum = int((end_len - start_len) / step) + 1
    train_numSeq = int(numSeq * train_size / pieceNum)
    val_numSeq = int(numSeq * val_size / pieceNum)
    test_numSeq = int(numSeq * (1 - train_size - val_size) / pieceNum)
    
    ####TRAIN
    for pieceCount in range(pieceNum):
        seqLength = start_len + (pieceCount * step)   
        for i in range(train_numSeq):
            #intact
            label = randomSequence(seqLength,alphabet_size)
            #generate a list of traces
            trace = [''] * num_traces
            for i in range(num_traces):
                trace[i] = deletionChannel(label,delta)
            
            #fragmented
            fragtrace = [''] * num_traces
            
            fraglabel = cut_data(label,fragnum,overlap)
            for i in range(num_traces):
                fragtrace[i] = cut_data(trace[i],fragnum,overlap)
            
            #generate intact 'file' (really just a string)
            
            if not '' in trace:
                label = formater(label)
                train_label = train_label + '\n' + label
                for i in range(num_traces):
                    trace[i] = formater(trace[i])                
                    train_trace[i] = train_trace[i] + '\n' + trace[i]
            
            
            keep = True
            #generate a list with all the fragments
            if not '' in trace:
                #keep = False
                for x in range(len(fragtrace)):
                    if  '' in fragtrace[x] :
                        keep = False
            
            if keep:
                
                for i in range(fragnum):
                        frag_train_label = frag_train_label + '\n' + formater(fraglabel[i])
                        for j in range(num_traces):
                            frag_train_trace[j] = frag_train_trace[j] + '\n' + formater(fragtrace[j][i])
          

    #####EVAL   
    for pieceCount in range(pieceNum):
        seqLength = start_len + (pieceCount * step)
        for i in range(val_numSeq):
            #intact
            label = randomSequence(seqLength,alphabet_size)
            #generate a list of traces
            trace = [''] * num_traces
            for i in range(num_traces):
                trace[i] = deletionChannel(label,delta)
            
            #fragmented
            fragtrace = [''] * num_traces
            
            fraglabel = cut_data(label,fragnum,overlap)
            for i in range(num_traces):
                fragtrace[i] = cut_data(trace[i],fragnum,overlap)
            

            #generate intact 'file' (really just a string)
            
            if not '' in trace:
                label = formater(label)
                val_label = val_label + '\n' + label
                for i in range(num_traces):
                    trace[i] = formater(trace[i])                
                    val_trace[i] = val_trace[i] + '\n' + trace[i]
            
            keep = True
            #generate a list with all the fragments
            if not '' in trace:
                #keep = False
                for x in range(len(fragtrace)):
                    if  '' in fragtrace[x] :
                        keep = False
                    
            
            if keep:
                
                for i in range(fragnum):
                        frag_val_label = frag_val_label + '\n' + formater(fraglabel[i])
                        for j in range(num_traces):
                            frag_val_trace[j] = frag_val_trace[j] + '\n' + formater(fragtrace[j][i])


    ####TEST
    for pieceCount in range(pieceNum):
        seqLength = start_len + (pieceCount * step)
        for i in range(test_numSeq):
            #intact
            label = randomSequence(seqLength,alphabet_size)
            #generate a list of traces
            trace = [''] * num_traces
            for i in range(num_traces):
                trace[i] = deletionChannel(label,delta)
            
            #fragmented
            fragtrace = [''] * num_traces
            
            fraglabel = cut_data(label,fragnum,overlap)
            for i in range(num_traces):
                fragtrace[i] = cut_data(trace[i],fragnum,overlap)

            
            #generate intact 'file' (really just a string)
            
            if not '' in trace:
                label = formater(label)
                test_label = test_label + '\n' + label
                for i in range(num_traces):
                    trace[i] = formater(trace[i])                
                    test_trace[i] = test_trace[i] + '\n' + trace[i]
            
            
            keep = True
            #generate a list with all the fragments
            if not '' in trace:
                #keep = False
                for x in range(len(fragtrace)):
                    if  '' in fragtrace[x] :
                        keep = False
            
            if keep:
                
                for i in range(fragnum):
                        frag_test_label = frag_test_label + '\n' + formater(fraglabel[i])
                        for j in range(num_traces):
                            frag_test_trace[j] = frag_test_trace[j] + '\n' + formater(fragtrace[j][i])
            
            
            
    #delete first line
    
    for i in range(num_traces):
        train_trace[i] = train_trace[i].split("\n",1)[1] + '\n'
        frag_train_trace[i] = frag_train_trace[i].split("\n",1)[1] + '\n'
        frag_val_trace[i] = frag_val_trace[i].split("\n",1)[1] + '\n'
        val_trace[i] = val_trace[i].split("\n",1)[1] + '\n'
        frag_test_trace[i] = frag_test_trace[i].split("\n",1)[1] + '\n'
        test_trace[i] = test_trace[i].split("\n",1)[1] + '\n'
    
    train_label = train_label.split("\n",1)[1] + '\n'
    val_label = val_label.split("\n",1)[1] + '\n'
    test_label = test_label.split("\n",1)[1] + '\n'
    
    frag_train_label = frag_train_label.split("\n",1)[1] + '\n'
    frag_val_label = frag_val_label.split("\n",1)[1] + '\n'
    frag_test_label = frag_test_label.split("\n",1)[1] + '\n'
    
    
        
    return (train_label, train_trace, val_label, val_trace, test_label, test_trace, frag_train_label ,frag_train_trace,
        frag_val_label ,frag_val_trace ,frag_test_label, frag_test_trace  )

def create_files(out_dir,num_traces,fragnum):
    """
    Creates files for each string returned by the generator
    (f_train_label, f_train_trace, f_val_label, f_val_trace, f_test_label, f_test_trace, f_frag_train_label ,
    f_frag_train_trace, f_frag_val_label ,f_frag_val_trace ,f_frag_test_label, f_frag_test_trace )

    """
    #find dir
    current = os.getcwd()
    path = current + '/' +out_dir
    try:  
        os.mkdir(path)
    except OSError:  
        print("Creation of the directory %s failed" % path)
    else:  
        print("Successfully created the directory %s " % path)
    dirpath = path + '/'


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


def create_summary(args):
    outdir = args.outdir
    seqLength = args.seqLength
    alphabet_size = args.alphabet_size
    delta = args.delta
    numSeq = args.numSeq
    num_traces = args.num_traces
    train_size = args.train_size
    val_size = args.val_size
    fragnum =args.fragnum
    overlap = args.overlap

    summary = 'Dataset Report' 
    summary = summary + '\nOutput directory = ' + outdir 
    summary = summary + '\nSequence Length = ' + str(seqLength)
    summary = summary + '\nAlphabet Size = ' + str(alphabet_size)
    summary = summary + '\nDeletion probability = ' + str(delta)
    summary = summary + '\nNumber of sequences = ' + str(numSeq)
    summary = summary + '\nNumber of traces = ' + str(num_traces)
    summary = summary + '\nTrain size = ' +str(train_size*100) +'%'
    summary = summary + '\nValidation size = ' +str(val_size*100) +'%'
    summary = summary + '\nNumber of fragments = '+str(fragnum)
    summary = summary + '\nOverlap rate = ' +str(overlap * 100) + '%'

    current = os.getcwd()
    name = current + '/' +outdir + '/' +'summary.txt'

    summary_file = open(name,"w+")
    summary_file.write(summary)
    summary_file.close()

def create_vocab(args):
    alphabet_size = args.alphabet_size
    outdir = args.outdir
    
    base = '<unk>\n<s>\n<\s>'
    for i in range(alphabet_size):
        base = base + '\n' + str(i)
    
    current = os.getcwd()
    
    label = current + '/' + outdir + '/' + 'vocab.label'
    trace = current + '/' +outdir + '/' +'vocab.trace'
    label_file = open(label,"w+")
    trace_file = open(trace,"w+") 
    label_file.write(base)
    label_file.close()
    trace_file.write(base)

    trace_file.close()


######MAIN#####
#at the end
args = parse_arguments()

#previous args
outdir = args.outdir
#seqLength = args.seqLength
#alphabet_size = args.alphabet_size
#delta = args.delta
#numSeq = args.numSeq
num_traces = args.num_traces
#train_size = args.train_size
#val_size = args.val_size
fragnum =args.fragnum
#overlap = args.overlap

#ranged args

ranged_mode = args.ranged_mode
#start_len = args.start_len
#end_len = args.end_len
#step = args.step


#cuts
if not ranged_mode:
    (train_label, train_trace, val_label, val_trace, test_label, test_trace, frag_train_label ,
    frag_train_trace, frag_val_label ,frag_val_trace ,
    frag_test_label, frag_test_trace ) = generate_cut_strings(args)
else:
    (train_label, train_trace, val_label, val_trace, test_label, test_trace, frag_train_label ,
    frag_train_trace, frag_val_label ,frag_val_trace ,
    frag_test_label, frag_test_trace ) = generate_cut_strings_ranged(args)




#create files
(f_train_label, f_train_trace, f_val_label, f_val_trace, f_test_label, f_test_trace, 
 f_frag_train_label , f_frag_train_trace, f_frag_val_label ,f_frag_val_trace, 
 f_frag_test_label, f_frag_test_trace) = create_files(outdir,num_traces,fragnum)

#create summary
create_summary(args)

create_vocab(args)

##Basic Files
#labels
f_train_label.write(train_label)
f_val_label.write(val_label)
f_test_label.write(test_label)


for i in range(num_traces):
    f_train_trace[i].write(train_trace[i])
    f_val_trace[i].write(val_trace[i])
    f_test_trace[i].write(test_trace[i])


###FRAG###


f_frag_train_label.write(frag_train_label)
f_frag_val_label.write(frag_val_label)
f_frag_test_label.write(frag_test_label)


for i in range(num_traces):
    f_frag_train_trace[i].write(frag_train_trace[i])
    f_frag_val_trace[i].write(frag_val_trace[i])
    f_frag_test_trace[i].write(frag_test_trace[i])




print('Done ;)')
