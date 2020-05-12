#!/usr/bin/env python

#Usage: python2.7 view_pcaps.py

import SocketServer
import dpkt, pcap, socket
from sys import argv
from ipaddr import IPv4Address, IPv6Address
import syslog
import time
import os

def read_pcap(pcap_file):

    print ('Reading:' + str(pcap_file) + '\n')
    f = open(str(pcap_file), "rb")
    pcap = dpkt.pcap.Reader(f)

    for ts, pkt in pcap:

        try:

            eth=dpkt.ethernet.Ethernet(pkt) 
            if eth.type!=dpkt.ethernet.ETH_TYPE_IP:
                continue

            #Parsing IP data
            ip=eth.data
            if type(ip) == dpkt.ip.IP:
                ipaddr = IPv4Address(socket.inet_ntop(socket.AF_INET, ip.dst)) 
            else:
                IPv6Address(socket.inet_ntop(socket.AF_INET6, ip.dst))
            
            #Parsing TCP data
            if ip.p==dpkt.ip.IP_PROTO_TCP: 
                tcp = ip.data

                src = socket.inet_ntoa(ip.src)
                dst = socket.inet_ntoa(ip.dst)
                tcp_sport = tcp.sport
                tcp_dport = tcp.dport
                
                if "192.168" in str(src): 
                    total_ips[str(src)] = 1
                if "192.168" in str(dst): 
                    total_ips[str(dst)] = 1
                     
                #Parsing HTTP data Responses:
                if (tcp.sport == 80) and len(tcp.data) > 0: 

                    http = dpkt.http.Response(tcp.data)
                    #print(http.body)
                    #print(http.status)
                    
                #Parsing HTTP data Requests:
                elif tcp.dport == 80 and len(tcp.data) > 0:

                    http = dpkt.http.Request(tcp.data)
                    #print(http.headers)
                    #print(http.uri)
                                        
            if ip.p==dpkt.ip.IP_PROTO_UDP:
                pass

        except dpkt.UnpackError as e:
            pass
            #fout.write('\n *Unpack ERROR HERE: %s * \n' % (e))
            
        except Exception as e:
            pass
            #fout.write('\n *ERROR HERE: %s * \n' % (e))

            
    f.close()


    
if __name__ == "__main__":

    total_ips = {}
    
    read_pcap(str("evaluation.pcap"))

    print("Total IPs:" + str(len(total_ips)))
    for ip in total_ips:
        print (str(ip)+'\n')
    