import dpkt

def readPcap(fileName, port_neutral = "False"):
	payload_list = []
	f = open(fileName,"rb")
	pcap = dpkt.pcap.Reader(f)
	total = 0
	for ts,buf in pcap:
		try:
			eth = dpkt.ethernet.Ethernet(buf)
			ip = eth.data
			tcp = ip.data
			#Read http payload
			if(tcp.sport==80 or tcp.dport==80):
				payload = tcp.data
				payload_list.append(str(payload))
				total = total + 1
                        elif (port_neutral == "True"):
                                payload = tcp.data
                                payload_list.append(str(payload))
                                total = total + 1
		except :
			continue

	#print "Total payloads read:" + str(fileName) + ":" + str(total) + "\n"
	return payload_list


def getPayloadStrings():
    payload_list = []
    list1 = readPcap('data/HTTPtext_V1.pcap')
    list2 = readPcap('data/HTTPtext_V2.pcap')    
    list3 = readPcap('data/modified_new3_simple_http.pcap')
    list4 = readPcap('data/modified_new4_simple_http.pcap')
    list5 = readPcap('data/modified_new5_simple_http.pcap')
    list6 = readPcap('data/modified_new6_simple_http.pcap')
    list7 = readPcap('data/modified_new_simple_http.pcap')

    payload_list.extend(list1)
    payload_list.extend(list2)
    payload_list.extend(list3)
    payload_list.extend(list4)
    payload_list.extend(list5)
    payload_list.extend(list6)
    payload_list.extend(list7)
    return payload_list

def read_attack_data(filename):
    listl = open(filename)
    listl1 = listl.read()
    #print listl1
    return [listl1]
