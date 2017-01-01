import sys, struct, socket

# dns packet
class Dns_Packet:
    
    # constructor to instantiate dns packet
    def __init__(self):
        self.packet_id = 0
        self.flags = 0
        self.questions = 0
        self.answers = 0
        self.authority = 0
        self.additional = 0
        self.query_name = ''
        self.query_type = 0
        self.query_class = 0
        self.answer_name = 0xC00C
        self.answer_type = 0x0001
        self.answer_class = 0x0001
        self.answer_ttl = 60
        self.answer_len = 4
        self.answer_addr = ''
        
        
    # extract the dig packet 
    def extract(self, packet):
        packet_header = struct.unpack('>HHHHHH', packet[:12])
        self.packet_id = packet_header[0]
        self.flags = packet_header[1]
        self.questions = packet_header[2]
        self.answers = packet_header[3]
        self.authority = packet_header[4]
        self.additional = packet_header[5]
        packet_query = struct.unpack('>HH', packet[-4:])
        self.query_type = packet_query[0]
        self.query_class = packet_query[1]
        queryName = packet[12:-4]
        idx = 0
        temp = []
        
        # extract query name
        try:
            while True:
                count = ord(queryName[idx])
                if count == 0:
                    break
                idx += 1
                temp.append(queryName[idx:idx + count])
                idx += count

            self.query_name = '.'.join(temp)
        except Exception as e:
            # print e
            self.query_name = 'cs5700cdn.example.com'

    # build dns packet by adding answer section
    def build(self, replica_ip):
        queryName = ''.join((chr(len(x)) + x for x in self.query_name.split('.')))
        query_pack = queryName + '\x00' + struct.pack('>HH', self.query_type, self.query_class)
        self.answer_addr = replica_ip
        self.answers=1
        self.flags = 0x8180
        answer_pack = struct.pack('>HHHLH4s', self.answer_name, self.answer_type, self.answer_class, self.answer_ttl, self.answer_len, socket.inet_aton(self.answer_addr))
        packet = struct.pack('>HHHHHH', self.packet_id, self.flags, self.questions, self.answers, self.authority, self.additional)
        
        return packet + query_pack + answer_pack


