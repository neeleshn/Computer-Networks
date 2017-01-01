from subprocess import call
from sets import Set

def init():
    global Reno_Reno, Newreno_Reno, Vegas_Vegas, Newreno_Vegas
    tcpTypes = ["Reno-Reno", "Newreno-Reno", "Vegas-Vegas","Newreno-Vegas"] # different tcps for comparision
    for tcpType in tcpTypes :
        for rate in range(1,11) : # for 1-10 cbr rate
            tcpSplit = tcpType.split("-")
            # run the tcl script
            call(['/course/cs4700f12/ns-allinone-2.35/bin/ns', 'tcl2exp.tcl', tcpSplit[0], tcpSplit[1], str(rate)+'mb'])
            calculate(tcpType, rate)
        
            if tcpType == "Reno-Reno" :
                Reno_Reno.write("\n")
        
            if tcpType == "Newreno-Reno" :
                Newreno_Reno.write("\n")

            if tcpType == "Vegas-Vegas" :
                Vegas_Vegas.write("\n")

            if tcpType == "Newreno-Vegas" :
                Newreno_Vegas.write("\n")


def calculate(tcpType,rate) :
    global Reno_Reno, Newreno_Reno, Vegas_Vegas, Newreno_Vegas
    
    # reset all variables to 0
    sent1Count=0
    sent2Count=0
    recv1Count=0
    recv2Count=0
    delay1Sum=0.0
    delay2Sum=0.0
    size1Sum=0
    size2Sum=0

    # dict to map seqid to time
    sent1Dict={}
    sent2Dict={}

    # dict to map seqid to packet size
    packet1Dict={}
    packet2Dict={}
    
    # read trace file to calculate throughput latency and droprate
    traceFile = open("out.tr","r")

    for eachline in traceFile :
        words = eachline.split()
        
        # count every packet sent from n1 and n5
        if words[0] == "+" and words[2] == "0" :
            sent1Count+=1
            sent1Dict[words[10]] = float(words[1])
        
        elif words[0] == "+" and words[2] == "4" :
            sent2Count+=1
            sent2Dict[words[10]] = float(words[1])

        # for every packet reach n1 and n5, calculate droprate and latency
        elif words[0] == "r" and words[3] == "0" :
            sent1Count-=1
            if words[10] in sent1Dict:
                delay1Sum += float(words[1]) - sent1Dict[words[10]]
                recv1Count +=1
                
        elif words[0] == "r" and words[3] == "4" :
            sent2Count-=1
            if words[10] in sent2Dict:
                delay2Sum += float(words[1]) - sent2Dict[words[10]]
                recv2Count +=1
        
        # for every packet reach n4 and n6, calculate throughput
        elif words[0] == "r" and words[3] == "3" :
            if words[10] in packet1Dict :
                size1Sum -= packet1Dict[words[10]]
                
            packet1Dict[words[10]] = float(words[5])
            size1Sum += packet1Dict[words[10]] 
             
        elif words[0] == "r" and words[3] == "5" :
            if words[10] in packet2Dict :
                size2Sum -= packet2Dict[words[10]]
                
            packet2Dict[words[10]] = float(words[5])
            size2Sum += packet2Dict[words[10]] 
         
    # calculate throughput, latency and droprate to files for each tcp
    latency1 = delay1Sum/recv1Count
    throughput1 = (size1Sum * 1.0 * 8) / (9000000)
    droprate1 = sent1Count * 1.0/len(sent1Dict)

    latency2 = delay2Sum/recv2Count
    throughput2 = (size2Sum * 1.0 * 8) / (9000000)
    droprate2 = sent2Count * 1.0/len(sent1Dict)

    # write throughput to files to plot graph
    if tcpType == "Reno-Reno" :
        Reno_Reno.write(str(throughput1)+"\t"+str(throughput2))
        
    if tcpType == "Newreno-Reno" :
        Newreno_Reno.write(str(throughput1)+"\t"+str(throughput2))

    if tcpType == "Vegas-Vegas" :
        Vegas_Vegas.write(str(throughput1)+"\t"+str(throughput2))

    if tcpType == "Newreno-Vegas" :
        Newreno_Vegas.write(str(throughput1)+"\t"+str(throughput2))


if __name__ == '__main__':

    #open files for all tcp variants
    Reno_Reno = open("results/Reno-Reno-tpt","w")
    Newreno_Reno = open("results/Newreno-Reno-tpt","w")
    Vegas_Vegas = open("results/Vegas-Vegas-tpt","w")
    Newreno_Vegas = open("results/Newreno-Vegas-tpt","w")
    
    init()
    
    # close all opened files
    Reno_Reno.close()
    Newreno_Reno.close()
    Vegas_Vegas.close()
    Newreno_Vegas.close()

