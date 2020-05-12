'''
    Code for calculating various distances and clustering the models

'''
import numpy as np
import scipy.spatial.distance as dist
import math

'''
averaged_feature_vector : 256*2 array representing <mean,variance> pairs for each of the 256 ASCII characters
new_frequency_distribution : 256*1 array representing the frequencies of each of the 256 ASCII characters
smoothing_factor : single scalar value 
'''
def give_mahalanobis_distance(averaged_feature_vector, new_frequency_distribution, smoothing_factor):
	if (smoothing_factor ==0):
        	raise Exception("Smoothing factor cannot be zero")
	distance = 0 
    	for n  in range(0,256) :
        	xi = averaged_feature_vector[n][0]
        	yi = new_frequency_distribution[n]
        	sigi = averaged_feature_vector[n][1]
                if(sigi <0):
                    print sigi
        	distance = distance + (abs(xi-yi)/(sigi+smoothing_factor))

	return distance

#Takes as argument two 1-D list and gives distance as double
'''
model_i : 256*1 array representing the average frequency values of each of the 256 ASCII characters
model_k : 256*1 array representing the average frequency values of each of the 256 ASCII characters
'''
def manhattan_distance(model_i,model_k):
	x = np.array(model_i)
	y = np.array(model_k)
	return dist.cityblock(x,y)
'''
variance1 : single scalar value
variance2 : single scalar value
mean1 : single scalar value
mean2 : single scalar value
size1 : single scalar value
size2 : single scalar value
'''
def weighted_variance(variance1, variance2, mean1,mean2,size1,size2):
	term1 = size1 * (variance1 + (mean1*mean1))
	term2 = size2*(variance2 + (mean2*mean2))
	size = size1 + size2
	weighted_mean = ((size1*mean1)+(size2*mean2))/ float(size)
	#print(weighted_mean)
	return ((term1 + term2)/ float(size)) - (weighted_mean*weighted_mean)

'''
sd1 : single scalar value
sd2 : single scalar value
mean1 : single scalar value
mean2 : single scalar value
size1 : single scalar value
size2 : single scalar value
'''
def weighted_sd(sd1,sd2,mean1,mean2,size1,size2):
	variance1 = sd1 * sd1
	variance2 = sd2 * sd2
	variance = weighted_variance(variance1, variance2, mean1, mean2, size1,size2)
	return math.sqrt(variance)

'''
There can be multiple implementations of this. We merge and update based on weighted average frequency where weight being the number of samples each model has
model_i: 256*2 feature array where each tuple is <freq,stddev> for length i
model_k: 256*2 feature array where each tuple is <freq,stddev> for length k
n_i: single scalar value representing the number of samples for length i
n_k: single scalar value representing the number of samples for length k  
'''
def merge_update(model_i,model_k,ni,nk):
#	print("merge and update")
        
	if (ni == 0 and nk == 0):
		return model_i,model_k
	for j in range(0,255):
		avg_frequency_i = model_i[j][0]
		avg_frequency_k = model_k[j][0]
		n = ni + nk
		avg_cumulative_mean = ((avg_frequency_i * ni) + (avg_frequency_k * nk))/n
		avg_cumulative_stddev = weighted_sd(model_i[j][1], model_k[j][1], model_i[j][0], model_k[j][0], ni, nk)
                model_i[j][0] = avg_cumulative_mean
                model_k[j][0] = avg_cumulative_mean
		model_i[j][1] = avg_cumulative_stddev
		model_k[j][1] = avg_cumulative_stddev
        return model_i,model_k
         
'''
Takes as argument
  models - 2d list with payload length and average frequency for 256 characters [n][256] where n is the number of models. The list is sorted based on payload length
  threshold - when two models should be merged
  lengthwise_sample_numbers - 1-D list number of samples recorded for each length while training 

Uses manhattan distance to decide which models need to be merged  
Model that remains will be a compact model and will not have all the lengths. For the lengths not found, look for the largest predecessor

threshold : single scalar value
models : (range of payload length)*256*2
lengthwise_sample_numbers : (range of payload length)*1 
'''
def cluster(threshold, models, lengthwise_sample_numbers):
        i = 0 
        # iterate over each of the models 
	while (i < len(models)):
        # for each model, search through nearby models and update
		k = i+1
		while(k < len(models) and manhattan_distance(models[i][0],models[k][0]) < threshold):
			ni = lengthwise_sample_numbers[i]
			nk = lengthwise_sample_numbers[k]
			models[i], models[k] = merge_update(models[i],models[k],ni,nk)
                        k = k+1
		i = k+1
        return models


