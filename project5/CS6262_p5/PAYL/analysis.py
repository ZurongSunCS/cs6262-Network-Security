'''
    Trains Model and Tests samples.
    Dependency : distance_and_clustering.py

'''
import sys, os, string
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import distance_and_clustering as dc
import read_pcap as dpr

def is_ascii(string1):
    for c in string1:
        if ord(c) >= 256:
            print '"'+c+'" '+str(ord(c))
            return 0
    return 1

def get_freq_from_ascii_string(ascii_string):
    freq_array1 = [0]*256
    for c in ascii_string:
        freq_array1[ord(c)] = freq_array1[ord(c)]+1
    return freq_array1

def get_mahabs_distance(pool, training_length_dict, averaged_feature_vector, new_frequency_distribution, smoothing_factor):
    for str2 in pool:
        mahabs_distance = sys.maxint

        if is_ascii(str2) == 0 :
            sys.exit('Error: File contains non-ascii characters! Exiting')
        new_frequency_distribution = get_freq_from_ascii_string(str2)

        # now, check if the length has been encountered is or not !
        if(len(str2) in training_length_dict.keys()):
            averaged_feature_vector = (feature_vector[min_length-len(str2)])
            mahabs_distance = dc.give_mahalanobis_distance(averaged_feature_vector, new_frequency_distribution, smoothing_factor)
        else:
            mahabs_distance = sys.maxint

    return mahabs_distance


# if verbose is set to True, the graphs are generated
def train_and_test(training, test, attack_file, smoothing_factor, threshold_for_classification, verbose = "False"):

    all_ascii = [str(i) for i in xrange(256)]
    all_ascii_int = [ j for j in xrange(256)]

    matplotlib.rcParams.update({'font.size': 10})

    # sort the files by length 
    training_length_dict = {}
    min_length = len(training[0])
    max_length = len(training[0])

    for payload in training:
        if is_ascii(payload) == 0 :
            sys.exit('Error: File contains non-ascii characters! Exiting')
        payload_length = len(payload)
        if payload_length in training_length_dict.keys():
            training_length_dict[payload_length].append(payload)
        else:
            training_length_dict[payload_length] =[payload]
        if min_length > payload_length:
            min_length = payload_length
        if max_length < payload_length:
            max_length = payload_length

    feature_vector = []
    for i in range(1, max_length-min_length+2):
        mean = [0]*256
        stddev = [0]*256
        feature_vector.append(np.vstack((mean,stddev)).T)
    
    print 'Training the Model'
    # process the sorted files and store the models by the length of the files
    for key in sorted(training_length_dict.iterkeys()):
        i = 0
        # frequency array for each length group
        freq_array_per_length= [[0]*256]*(len(training_length_dict[key]))
        for argu in training_length_dict[key]:
            if is_ascii(argu) == 0 :
                sys.exit('Error: File contains non-ascii characters! Exiting')
            freq_array_per_length[i] = get_freq_from_ascii_string(argu)
            i = i+1
            
        stddev_array_per_length = np.std(freq_array_per_length,axis=0) 
        mean_array_per_length = np.mean(freq_array_per_length, axis=0)
        feature_vector[min_length-key] = np.vstack((mean_array_per_length,stddev_array_per_length)).T
        #print str(min_length-key)
        #print feature_vector[min_length-key]
        #print "NEW"
        
        # plotting the mean array        
        if verbose == "True":
            plt.xticks(all_ascii_int, all_ascii)
            plt.bar(all_ascii_int, mean_array_per_length)
            plt.title('Mean frequency of each of the acsii characters for length '+str(key))
            plt.show()

        # plotting the std dev array
        if verbose == "True":
            plt.xticks(all_ascii_int, all_ascii)
            plt.xticks(all_ascii_int, all_ascii)
            plt.bar(all_ascii_int, stddev_array_per_length)
            plt.title('Std Dev of freq of each of the ascii characters for Length '+str(key))
            plt.show()


    #print 'Training lengths:'
    #for key in sorted(training_length_dict.iterkeys()): 
    #        print "Training key: " + str(key) + ":" + str(len(training_length_dict[key]))
            
    print 'Testing the Model'
   
    true_positive = 0
    false_negative = 0

    for str2 in test:
        mahabs_distance = sys.maxint

        if is_ascii(str2) == 0 :
            sys.exit('Error: File contains non-ascii characters! Exiting')
        new_frequency_distribution = get_freq_from_ascii_string(str2)
        # now, check if the length has been encountered is or not !
        if(len(str2) in training_length_dict.keys()):
            averaged_feature_vector = (feature_vector[min_length-len(str2)])
            #print averaged_feature_vector
            mahabs_distance = dc.give_mahalanobis_distance(averaged_feature_vector, new_frequency_distribution, smoothing_factor)
        else:
            mahabs_distance = sys.maxint

        if mahabs_distance <= threshold_for_classification:            
            true_positive = true_positive + 1
            if verbose == "True":
                print str(mahabs_distance)

        else:
            false_negative = false_negative + 1 
            if verbose == "True":
                print str(mahabs_distance)

    print 'Total Number of testing samples: '+str(len(test))
    print 'Percentage of True positives: '+str((true_positive/float(len(test)))*100.0)


    
    #Attack data loading
    
    false_positive = 0
    true_negative = 0
    if attack_file is not None:
        if attack_file.lower().endswith('.pcap'):
            attack = dpr.readPcap(attack_file, "True")
        else:
            attack = dpr.read_attack_data(attack_file)
    else:
        print '\nExiting now'
        return

    print '--------------------------------------'
    print 'Analysing attack data, of length '+str(len(attack[0]))
    for str2 in attack:
        mahabs_distance = sys.maxint

        if is_ascii(str2) == 0 :
            sys.exit('Error: File contains non-ascii characters! Exiting')
        new_frequency_distribution = get_freq_from_ascii_string(str2)
        
        # now, check if the length has been encountered is or not !
        if(len(str2) in training_length_dict.keys()):
            #print "No of samples in length:" + str(len(training_length_dict[len(str2)]))
            #print str(min_length-len(str2))
            #print feature_vector[min_length-len(str2)]
            #averaged_feature_vector = (feature_vector[-2503])
            averaged_feature_vector = (feature_vector[min_length-len(str2)])
            mahabs_distance = dc.give_mahalanobis_distance(averaged_feature_vector, new_frequency_distribution, smoothing_factor)
        else:
            mahabs_distance = sys.maxint

        if mahabs_distance <= threshold_for_classification:            
            false_positive = false_positive + 1
            print 'Calculated distance of '+ str(mahabs_distance)+' is lesser than the threshold of '+\
                    str(threshold_for_classification)+'. It fits the model. '

        else:
            true_negative = true_negative + 1            
            print 'Calculated distance of '+ str(mahabs_distance)+' is greater than the threshold of '+\
            str(threshold_for_classification) +'. It doesn\'t fit the model. '

    print 'Total number of True Negatives: '+str((true_negative/float(len(attack)))*100.0)
    print 'Total number of False Positives: '+str((false_positive/float(len(attack)))*100.0)+'\n'
