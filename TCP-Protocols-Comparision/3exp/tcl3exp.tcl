
# Make a NS simulator 
set ns [new Simulator]        
set tf [open out.tr w]
$ns trace-all $tf

# Read command line args
set tcpType1 [lindex $argv 0]
set qType [lindex $argv 1]

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
$ns duplex-link $n1 $n2 10Mb 10ms $qType
$ns duplex-link $n5 $n2 10Mb 10ms $qType
$ns duplex-link $n2 $n3 10Mb 10ms $qType
$ns duplex-link $n3 $n4 10Mb 10ms $qType
$ns duplex-link $n3 $n6 10Mb 10ms $qType

#set Queue Size of all links to 5
$ns queue-limit $n1 $n2 5
$ns queue-limit $n2 $n3 5
$ns queue-limit $n3 $n4 5
$ns queue-limit $n5 $n2 5
$ns queue-limit $n3 $n6 5

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
$ns attach-agent $n5 $udp1
set null1 [new Agent/Null]
$ns attach-agent $n6 $null1
$ns connect $udp1 $null1
$udp1 set fid_ 2

# Set CBR Traffic on udp1
set cbr1 [new Application/Traffic/CBR]
$cbr1 attach-agent $udp1
$cbr1 set type_ CBR
$cbr1 set packet_size_ 1000
$cbr1 set rate_ 7mb
$cbr1 set random_ false

# Create required tcp1 connection
if {$tcpType1 eq "Reno"} {
	set tcp1 [new Agent/TCP]
	set sink1 [new Agent/TCPSink]
} elseif {$tcpType1 eq "Sack"} {
	set tcp1 [new Agent/TCP/Sack1]
	set sink1 [new Agent/TCPSink/Sack1]
}

# Add a TCP1 connection
$tcp1 set class_ 1
$ns attach-agent $n1 $tcp1
$ns attach-agent $n4 $sink1
$ns connect $tcp1 $sink1
$ns set fid_ 1

# Setup a FTP traffic generator on tcp1
set ftp1 [new Application/FTP]
$ftp1 attach-agent $tcp1
$ftp1 set type_ FTP               

# Schedule start/stop times
$ns at 0.0 "$ftp1 start"
$ns at 12.0 "$cbr1 start"
$ns at 40.0 "$cbr1 stop"
$ns at 50.0 "$ftp1 stop"

# Set simulation end time
$ns at 50.0 "finish"

# Run simulation !!!!
$ns run

