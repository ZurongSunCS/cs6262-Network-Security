#!/usr/bin/env python2
import struct
import math
import random
from frequency import *
from collections import Counter

def padding(artificial_payload, raw_payload):

	padding = ""

	# Get frequency of raw_payload and artificial profile payload
	artificial_frequency = frequency(artificial_payload)
	raw_payload_frequency = frequency(raw_payload)

	# To simplify padding, you only need to find the maximum frequency difference for each byte in raw_payload
	# and artificial_payload, and pad that byte to the end of the raw_payload.
	# Note: only consider the difference when artificial profile has higher frequency.


    # Your code here ...
	max_freq = 0
	max_freq_char = chr(0) #default
	for i in artificial_frequency:
		if i in raw_payload_frequency:
			a_freq = artificial_frequency[i]
			if max_freq == 0:
				max_freq = a_freq
				max_freq_char = i
			r_freq = raw_payload_frequency[i]

			if a_freq > r_freq:
				diff = a_freq - r_freq
				diff_char = i

				if diff > max_freq:
					max_freq = diff
					max_freq_char = diff_char

	# Depending on the difference, call raw_payload.append
	raw_payload.append(max_freq_char)

