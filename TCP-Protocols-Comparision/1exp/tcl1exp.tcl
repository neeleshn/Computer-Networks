
# Read command line args
set tcpType [lindex $argv 0]
set cbrRate [lindex $argv 1]

# Make a NS simulator 
set ns [new Simulator]        
set tf [open out.tr  w]
$ns trace-all $tf

# Define a 'finish' procedure
proc finish {} {
   global ns tf
   $ns flush-trace ;# flush trace files
   close $tf
   exit 0
}

# Create the nodes:
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]

# Create the links 
$ns duplex-link $n1 $n2 10Mb 2ms DropTail
$ns duplex-link $n5 $n2 10Mb 2ms DropTail
$ns duplex-link $n2 $n3 10Mb 2ms DropTail
$ns duplex-link $n3 $n4 10Mb 2ms DropTail
$ns duplex-link $n3 $n6 10Mb 2ms DropTail

#Set Queue Size of link (n2-n3) to 5
$ns queue-limit $n2 $n3 5

# ################################################
# Make this configuration:                       NEW
# ################################################
#
#            1                 4
#   10Mb/10ms \   10Mb/10ms   / 10Mb/10ms
#              2 ----------- 3
#   10Mb/10ms /               \ 10Mb/10ms
#            5                 6
#
# ################################################

# Add a UDP connection
set udp1 [new Agent/UDP]
$ns attach-agent $n2 $udp1
set null1 [new Agent/Null]
$ns attach-agent $n3 $null1
$ns connect $udp1 $null1 
$udp1 set fid_ 2

# Set CBR Traffic on udp1
set cbr1 [new Application/Traffic/CBR]
$cbr1 attach-agent $udp1
$cbr1 set type_ CBR
$cbr1 set packet_size_ 1000
$cbr1 set rate_ $cbrRate
$cbr1 set random_ false

# Create required tcp connection
if {$tcpType eq "Tahoe"} {
	set tcp1 [new Agent/TCP]
} elseif {$tcpType eq "Reno"} {
	set tcp1 [new Agent/TCP/Reno]
} elseif {$tcpType eq "Newreno"} {
	set tcp1 [new Agent/TCP/Newreno]
} elseif {$tcpType eq "Vegas"} {
	set tcp1 [new Agent/TCP/Vegas]
}

# Add a TCP connection
$tcp1 set class_ 2
$ns attach-agent $n1 $tcp1
set sink1 [new Agent/TCPSink]
$ns attach-agent $n4 $sink1
$ns connect $tcp1 $sink1
$tcp1 set fid_ 2

# Setup a FTP traffic generator on tcp1
set ftp1 [new Application/FTP]
$ftp1 attach-agent $tcp1
$ftp1 set type_ FTP               

# Schedule start/stop times
$ns at 0.0 "$cbr1 start"
$ns at 0.0 "$ftp1 start"
$ns at 10.0 "$ftp1 stop"
$ns at 10.0 "$cbr1 stop"

# Set simulation end time
$ns at 10.0 "finish"            

# Run simulation !!!!
$ns run


