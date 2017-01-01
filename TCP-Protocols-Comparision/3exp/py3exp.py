from subprocess import call
from sets import Set
import pdb

def init():
    global red,droptail
    tcpTypes = ["Reno", "Sack"] # diff tcp variants
    qTypes = ["RED", "DropTail"] # diff queue algorithms
    for tcpType in tcpTypes :
        for qType in qTypes :
            
            call(['/course/cs4700f12/ns-allinone-2.35/bin/ns', 'tcl3exp.tcl', tcpType, qType]) # run tcl script
            calculate(tcpType, qType)
        
            if qType == "RED":
                red.write("\n\n\n")
            elif qType == "DropTail":
                droptail.write("\n\n\n")

# function to calculate droprate, throughput
def calculate(tcpType,qType) :
    global red,droptail
    nextBreak=0 # calculate values at a time interval of 4 seconds
    recvCount=1 # count of tcp packets received
    delaySum=0.0 # sum of RTT
    sizeSum=0 # sum of tcp packets Size
    cbrSize=0.0 # sum of cbr packets size
    sentDict={} # dict of tcp packets time
    packetDict={} # dict of tcp packets size
    traceFile = open("out.tr","r") # open the trace file
    
    for eachline in traceFile :
        words = eachline.split()
        current = words[1].split(".")[0]
        
        try :
            cur1 = int(words[1])
        except :
            cur1 = 0
        
        # if current time = nextBreak write throughput and cbr rate
        if int(current) == nextBreak or cur1 == nextBreak :
            
            throughput = sizeSum * 8.0 / 4000000
            cbrRate = cbrSize * 8.0/4000000
            
            # write to required file
            if qType == "RED":
                red.write(str(nextBreak)+"\t"+str(throughput)+"\t"+str(cbrRate)+"\n")
            elif qType == "DropTail":
                droptail.write(str(nextBreak)+"\t"+str(throughput)+"\t"+str(cbrRate)+"\n")
           
            # reset counts 
            sizeSum = 0
            cbrSize=0.0
            nextBreak +=4
        
        # add every packet sent from n1 to sentDict
        if words[0] == "+" and words[2] == "0" : 
            sentDict[words[10]] = float(words[1])
        
        # for every ack reaching n1 add to RTT
        elif words[0] == "r" and words[3] == "0" :
            if words[10] in sentDict:
                delaySum += float(words[1]) - sentDict[words[10]]
                recvCount +=1
        
        # for every packet reaching n4 add to throughput
        elif words[0] == "r" and words[3] == "3" :
            if words[10] not in packetDict :
                packetDict[words[10]] = float(words[5])
                sizeSum += packetDict[words[10]] 
        
        # for every packet reaching n6 add to cbrSize
        elif words[0] == "r" and words[3] == "5" :
            cbrSize+=float(words[5])
          
    # calculate latency and write to file
    latency = delaySum/recvCount
    latFile.write(tcpType+"-"+qType+":\t"+str(latency)+"\n")
    


if __name__ == '__main__':
    red = open("results/red","w") # file to print throughput values of red queue
    droptail = open("results/droptail","w") # file to print throughput values of droptail queue
    latFile = open("results/latency","w") # file print latency of each tcp variant and queue type
    
    init()

    # close open files
    red.close()
    droptail.close()
    latFile.close()

