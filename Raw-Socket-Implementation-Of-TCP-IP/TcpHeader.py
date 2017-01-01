#!/usr/bin/python
import socket
from struct import *

# Class for constructing TCP Header
class TcpHeader:
	
	# Initilazes the variables in TCP Header
	def __init__(self):
		
		self.tcp_source = 0
		self.tcp_dest = 0
		
		self.tcp_seq = 0
		self.tcp_ack_seq = 0
		
		self.tcp_fin = 0
		self.tcp_syn = 1
		self.tcp_ack = 0
		self.tcp_rst = 0
		self.tcp_psh = 0
		self.tcp_urg = 0
		
		self.placeholder = 0
		self.tcp_window = socket.htons (5840)    #   maximum allowed window size
		self.tcp_doff = 5
		self.tcp_check = 0
		self.tcp_urg_ptr = 0
		self.tcp_offset_res = (self.tcp_doff << 4) + 0
		self.tcp_flags = self.tcp_fin + (self.tcp_syn << 1) + (self.tcp_rst << 2) + (self.tcp_psh <<3) + (self.tcp_ack << 4) + (self.tcp_urg << 5)
		self.tcp_mss = 1460
		self.data = ""
		self.tcp_length = 0
	
	# Method for writing values to respective fields in TCP header
	def setTcpHeader(self, sourcePort, destPort, sequenceNo, ackNo, fin_flag, syn_flag, ack_flag, rst_flag, psh_flag, urg_flag, data):
		
		self.tcp_source = sourcePort
		self.tcp_dest = destPort
		
		self.tcp_seq = sequenceNo
		self.tcp_ack_seq = ackNo
		
		self.tcp_fin = fin_flag
		self.tcp_syn = syn_flag
		self.tcp_ack = ack_flag
		self.tcp_rst = rst_flag
		self.tcp_psh = psh_flag
		self.tcp_urg = urg_flag
		
		self.tcp_window = socket.htons (5840)    # Maximum allowed advertised window size
		self.tcp_offset_res = (self.tcp_doff << 4) + 0
		self.tcp_flags = self.tcp_fin + (self.tcp_syn << 1) + (self.tcp_rst << 2) + (self.tcp_psh <<3) + (self.tcp_ack << 4) + (self.tcp_urg << 5)
		
		self.data = data
		
		
	# Method for calculation of checksum from packet
	def checksum(self,msg):
		s = 0

		if ((len(msg) % 2) != 0):
			for i in range(0, len(msg) - 1, 2):
				w = ord(msg[i]) + (ord(msg[i + 1]) << 8)
				s += w
			s += socket.ntohs(0xFF00) & (ord(msg[(len(msg)-1)]))
		else:
			for i in range(0, len(msg), 2):
				w = ord(msg[i]) + (ord(msg[i + 1]) << 8)
				s += w
											
		s = (s >> 16) + (s & 0xffff)
		s += (s >> 16)
		s = ~s & 0xffff
		return s
	
	
	# Construction of tcp header for sending packets
	def buildTcpHeader(self, source_ip, dest_ip) :
		
		source_address = socket.inet_aton( source_ip )
		dest_address = socket.inet_aton(dest_ip)
		
		protocol = socket.IPPROTO_TCP
		tcp_header = pack('!HHLLBBHHH', self.tcp_source, self.tcp_dest, self.tcp_seq, self.tcp_ack_seq, self.tcp_offset_res, self.tcp_flags, self.tcp_window, self.tcp_check, self.tcp_urg_ptr) #Packages TCP header fields to build TCP packet
		
		self.tcp_length = len(tcp_header) + len(self.data)
		
		psh = pack('!4s4sBBH' , source_address , dest_address , self.placeholder , protocol , self.tcp_length);
		psh = psh + tcp_header + self.data; # generates psuedo header for checksum calculation
		self.tcp_check = self.checksum(psh)
		
		# Constructs the tcp header again and fill the correct checksum
		tcp_header = pack('!HHLLBBH', self.tcp_source, self.tcp_dest, self.tcp_seq, self.tcp_ack_seq, self.tcp_offset_res, self.tcp_flags, self.tcp_window) + pack('H' , self.tcp_check) + pack('!H' , self.tcp_urg_ptr)
		
		#print "seq no: "+str(self.tcp_seq)+"\nack no: "+str(self.tcp_ack_seq)+"\ndata: "+self.data
		return tcp_header
	
	
	# Method for extracting tcp header values for incoming packets
	def extractTcpHeader(self, tcp_header) :
		
		tcph = unpack('!HHLLBBHHH' , tcp_header)
		self.tcp_source = tcph[0]
		self.tcp_dest = tcph[1]
		self.tcp_seq = tcph[2]
		self.tcp_ack_seq = tcph[3]
		self.tcp_doff = tcph[4]
		self.tcp_offset_res = self.tcp_doff >> 4
		self.tcp_flags = tcph[5] & 0x3F
		self.tcp_urg = (self.tcp_flags & 0x20) >> 5
		self.tcp_ack = (self.tcp_flags & 0x10) >> 4
		self.tcp_psh = (self.tcp_flags & 0x08) >> 3
		self.tcp_rst = (self.tcp_flags & 0x04) >> 2
		self.tcp_syn = (self.tcp_flags & 0x02) >> 1
		self.tcp_fin = self.tcp_flags & 0x01
		self.tcp_window = tcph[6]
		self.tcp_check = tcph[7]
		self.tcp_urg_ptr = tcph[8]

