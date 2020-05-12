#!/usr/bin/env python2
import struct
import math
import dpkt
import socket
from collections import Counter
from frequency import *

def substitute(attack_payload, subsitution_table):
    # Use the substitution table you generated to encrypt attack payload
    # Note that you also need to generate a xor_table which will be used to decrypt the attack_payload
    # i.e. (encrypted attack payload) XOR (xor_table) = (original attack payload)

    b_attack_payload = bytearray(attack_payload)

    # Based on your implementattion of substitution table, please prepare result and xor_table as output.pcap

    result = []
    xor_table = []

    for value in b_attack_payload:
        a=chr(value)
        b=subsitution_table[a]
        xor_val=ord(a)^ord(b)
        result.append(b)
        xor_table.append(chr(xor_val))

    return (xor_table, result)

def getSubstitutionTable(artificial_payload, attack_payload):
    # You will need to generate a substitution table which can be used to encrypt the attack body by replacing the most frequent byte in attack body by the most frequent byte in artificial profile one by one

    # Note that the frequency for each byte is provided below in dictionay format. Please check frequency.py for more details
    artificial_frequency = frequency(artificial_payload)
    attack_frequency = frequency(attack_payload)

    sorted_artificial_frequency = sorting(artificial_frequency)
    sorted_attack_frequency = sorting(attack_frequency)

    # Your code here ...
    # You may implement substitution table in your way. Just make sure it can be used in substitute(attack_payload, subsitution_table)
    substitution_table = {}
    for idx, val in enumerate(sorted_attack_frequency):
        old_char = val[0]
        new_char = sorted_artificial_frequency[idx][0]
        substitution_table[old_char] = new_char

    return substitution_table


def getAttackBodyPayload(path):
    f = open(path,"rb")
    pcap = dpkt.pcap.Reader(f)
    for ts, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        ip = eth.data
        if socket.inet_ntoa(ip.dst) == "192.150.11.111": # verify the dst IP from your attack payload
            tcp = ip.data
            if tcp.data == "":
                continue
            return tcp.data.rstrip()

def getArtificialPayload(path):
    f = open(path,"rb")
    pcap = dpkt.pcap.Reader(f)
    for ts, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        ip = eth.data
        tcp = ip.data
        if tcp.sport == 80 and len(tcp.data) > 0:
            return tcp.data
