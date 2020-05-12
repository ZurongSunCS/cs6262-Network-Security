'''
    Wrapper script for OMSCS CS 6262 Project 5    
    run as : python wrapper.py

'''
import read_pcap as dpr
import random as rn
import sys
import analysis

attack_file = None

# check which mode the program is being run in 
len_of_args = len(sys.argv)
if(len_of_args == 1):
    print '\n\tAttack data not provided, training and testing model based on pcap files in \'data/\' folder alone.' 
    print '\tTo provide attack data, run the code as: python wrapper.py <attack-data-file-name>'
else:
    print '\n\tAttack data provided, as command line argument \''+sys.argv[1]+'\''
    attack_file = sys.argv[1]
print '---------------------------------------------'

payloads = dpr.getPayloadStrings()

# shuffle the data to randomly pick samples
rn.shuffle(payloads)

min_length = 0 
max_length = 0

while min_length ==0 and max_length ==0:    
    min_length = 0 
    max_length = 0
    # This is where we decide what the split ratio is
    split_ratio = 0.75
    split_index = int(len(payloads)*split_ratio)
    training = payloads[0:split_index+1]
    test = payloads[split_index+1:len(payloads)]

    # we need at least one min and max length samples in the training data set
    for x in training:
        if len(x) == 0:
            min_length = 1
        if len(x) == 1460:
            max_length =1
    for j in range(0,len(test)):        
        if len(test[j]) == 705:
            for i in range(0, len(training)):
                if len(training[i]) !=0 and len(training[i]) != 1460 and len(training[i]) !=705:
                    t = training[i]
                    training[i] = test[j]
                    test[j] = t
                    i = len(training)+1                   

# Simple sanity check
if len(payloads) != len(test)+len(training) or split_ratio >= 1.0:
        sys.exit()
else:
        '''
        To better understand the behaviour of the model with different parameters, we typically 
        let the parameters iterate over a range.

        Here, range(threshold_for_mahalanobis_lower, threshold_for_mahalanobis_upper+1) is the 
        range over which the mahalanobis threshold iterates. 
        Similarly, range(smoothing_factor_lower, smoothing_factor_upper+0.1) is the range over
        which the smoothing factor iterates.
        
        For each such combination of mahalanobis threshold and smoothing factor, the model is 
        generated with these parameters.
        '''
        #smoothing_factor_lower = 10
        #smoothing_factor_upper = 50
        #threshold_for_mahalanobis_lower = 50
        #threshold_for_mahalanobis_upper = 200000
        # this loops from smoothing_factor_lower to smoothing_factor_upper in steps of 0.1
        #for smoothing_factor in range(smoothing_factor_lower, smoothing_factor_upper+1):
        #    for mahabs in range(threshold_for_mahalanobis_lower, threshold_for_mahalanobis_upper+1, 50):
        #        print 'Smoothing Factor: '+str(smoothing_factor/10.0)
        #        print 'Threshold for Mahalanobis Distance: '+str(mahabs)
        #        analysis.train_and_test(training, test, attack_file, smoothing_factor/10.0, mahabs, verbose = "False")
        #        print '---------------------------------------------'

        smoothing_factor = 12.3
        mahabs = 4567.89
        print 'Smoothing Factor: '+str(smoothing_factor/10.0)
        print 'Threshold for Mahalanobis Distance: '+str(mahabs)
        analysis.train_and_test(training, test, attack_file, smoothing_factor/10.0, mahabs, verbose = "False")
        print '---------------------------------------------'
