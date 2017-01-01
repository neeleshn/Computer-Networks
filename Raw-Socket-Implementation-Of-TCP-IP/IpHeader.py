#!/usr/bin/python
import socket
from struct import *

#Class for constructing IP Header
class IpHeader:
	
	#Initilazes the variables in IP Header
	def __init__(self):
		
		self.ip_ihl = 5
		self.ip_ver = 4
		self.ip_tos = 0
		self.ip_tot_len = 0  # kernel will fill the correct total length
		self.ip_id = 0   #Id of this packet
		self.ip_frag_off = 0
		self.ip_ttl = 255
		self.ip_proto = socket.IPPROTO_TCP
		self.ip_check = 0    # kernel will fill the correct checksum
		self.ip_saddr = ""
		self.ip_daddr = ""
		self.ip_ihl_ver = (self.ip_ver << 4) + self.ip_ihl
		self.iph_length = 0	
	
	# Method for constructing IP header to send outgoing packets
	def buildIpHeader(self, ip_id, source_ip, dest_ip) :
		
		self.ip_id = ip_id
		self.ip_saddr = socket.inet_aton( source_ip )
		self.ip_daddr = socket.inet_aton(dest_ip)
		
		ip_header = pack('!BBHHHBBH4s4s', self.ip_ihl_ver, self.ip_tos, self.ip_tot_len, self.ip_id, self.ip_frag_off, self.ip_ttl, self.ip_proto, self.ip_check, self.ip_saddr, self.ip_daddr) # Constructs ip header after writing values in respective fields of Ip header 
		
		return ip_header
	
	
	# Method for extracting IP header values for incoming packets
	def extractIpHeader(self, ip_header) :
		
		iph = unpack('!BBHHHBBH4s4s' , ip_header) #Extract the Ip headers from packet
 
		self.ip_ihl_ver = iph[0]
		self.ip_ver = self.ip_ihl >> 4
		self.ip_ihl = self.ip_ihl_ver & 0xF
		self.iph_length = self.ip_ihl * 4
		self.ip_tos = iph[1]
		self.ip_tot_len = iph[2]
		self.ip_id = iph[3]
		self.ip_frag_off = iph[4]
		self.ip_ttl = iph[5]
		self.ip_proto = iph[6]
		self.ip_saddr = socket.inet_ntoa(iph[8]);
		self.ip_daddr = socket.inet_ntoa(iph[9]);
		

