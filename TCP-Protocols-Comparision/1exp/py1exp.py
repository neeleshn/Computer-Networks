from subprocess import call
from sets import Set

def init():
    
    global latFile, dropFile, tptFile
    tcpTypes = ["Tahoe","Reno","Newreno","Vegas"] # types of tcp variants
    for tcpType in tcpTypes :
        for rate in range(1,11) :
            #run tcl script and calculate throughput, latency and droprate
            call(['/course/cs4700f12/ns-allinone-2.35/bin/ns', 'tcl1exp.tcl', tcpType, str(rate)+'mb'])
            calculate(tcpType, rate)
        
        latFile.write("\n")
        tptFile.write("\n")
        dropFile.write("\n")

def calculate(tcpType,rate) :
    global latFile, dropFile, tptFile

    # reset variables
    dropCount=0
    sentCount=0
    recvCount=0
    delaySum=0.0
    sizeSum=0.0
    
    sentDict={} # dict to map seqid to time
    packetDict = {} # dict to map seqid to packet size

    traceFile = open("out.tr","r") # read trace file

    for eachline in traceFile :
        words = eachline.split()
        
        # increase drop count for every packet dropped
        if words[0] == "d" :
            dropCount +=1
        
        # for every packet leaving n1, increase sent count
        elif words[0] == "+" and words[2] == "0" :
            sentCount +=1
            sentDict[words[10]] = words[1]
        
        # for every ack reaching n1, add RTT
        elif words[3] == "0" and words[0] == "r" :
            if words[10] in sentDict:
                delaySum += float(words[1]) - float(sentDict[words[10]])
                recvCount +=1
        
        # for every packet reaching n4, add to throughput
        elif words[3] == "3" and words[0] == "r" :
            if words[10] in packetDict :
                sizeSum -= packetDict[words[10]]
                
            packetDict[words[10]] = float(words[5])
            sizeSum += packetDict[words[10]] 
         
    # calculate latency, throughput and droprate
    latency = delaySum/recvCount
    throughput = (sizeSum * 1.0 * 8) / (10*1000000)
    droprate = dropCount*1.0/sentCount
    
    # write latency, throughput and droprate to respective files
    latFile.write(str(latency)+"\t")
    tptFile.write(str(throughput)+"\t")
    dropFile.write(str(droprate)+"\t")
    
            
if __name__ == '__main__':
    latFile = open("results/latency","w") # open a file to write each tcp variant's latency
    dropFile = open("results/droprate","w") # open a file to write each tcp variant's droprate
    tptFile = open("results/throughput","w") # open a file to write each tcp variant's throughput
    init()
    # close all opened files
    latFile.close()
    dropFile.close()
    tptFile.close()


