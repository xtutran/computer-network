import random
import socket, struct, sys, os.path, logging
from socket import AF_INET, SOCK_DGRAM
from array import array
import re


def toip(ip):
    # "convert decimal dotted quad string to long integer"
    return struct.unpack('L', socket.inet_aton(ip))[0]


def todottedip(n):
    # "convert long int to dotted quad string"
    return socket.inet_ntoa(struct.pack('L',n))


def ip_in_net(dest, mask, subnet):
    return toip(dest) & toip(mask) == toip(subnet)


def read_route_table(route_table_file):
    res = []
    i = 0
    with open(route_table_file, 'rb') as f:
        try:
            content = f.readlines()
            for line in content:
                tokens = re.split(r'[ ]+', line.rstrip('\n').rstrip('\r'))
                if len(tokens) != 3:
                    continue

                res.append(tokens)

            f.close()
        except IOError as err:
            print 'Error: reading route table file: ' + route_table_file
            sys.exit(1)
    return res


def check_destination(route_table, dest_ip):
    for route_record in route_table:
        if ip_in_net(dest_ip, route_record[1], route_record[0]):
            return route_record[2]
    return None


# main method to launch the server
def main():
    argv = sys.argv
    if len(argv) != 4:
        print 'Usage: python router.py <port> <route_table_file> <statistic_file>'
        sys.exit(1)

    if not argv[1].isdigit():
        print 'Port must be a number'
        sys.exit(1)

    port = int(argv[1])
    route_table_file = argv[2]
    stats_file = argv[3]

    if not os.path.isfile(route_table_file) or not os.access(route_table_file, os.R_OK):
        print 'Error: route table file: ' + route_table_file + ' doesnt exist';
        sys.exit(1)
    route_table = read_route_table(route_table_file)
    logging.basicConfig(filename=stats_file, format='%(message)s', filemode='w', level=logging.INFO)
    try:
        serversocket = socket.socket(AF_INET, SOCK_DGRAM)  # Create a socket object
        serversocket.bind(('127.0.0.1', port))  # Bind to the port
        serversocket.setblocking(True)

        # Now wait for client connection.
        print 'Server listening....'
        expired_packets = 0
        unroutable_packets = 0
        delivered_direct = 0
        packets_forwarded = 0
        while True:
            packet_bytes, recv_addr = serversocket.recvfrom(1024)
            if packet_bytes:
                if str.encode(packet_bytes) == '$':
                    logging.info("expired_packets = %d" % expired_packets)
                    logging.info("unroutable_packets = %d" % unroutable_packets)
                    logging.info("delivered_direct = %d" % delivered_direct)
                    logging.info("packets_forwarded = %d" % packets_forwarded)

                packet_info = re.split(r', ', str.encode(packet_bytes))
                packet_id = packet_info[0]
                # source = packet_info[1]
                dest = packet_info[2]
                ttl = int(packet_info[3])
                # payload = packet_info[4]
                if ttl - 1 == 0:
                    expired_packets += 1
                    continue
                route_host = check_destination(route_table, dest)
                if not route_host:
                    unroutable_packets += 1
                    continue
                elif route_host == '0':
                    delivered_direct += 1
                    print 'Delivering direct: packet ID=%s, dest=%s' % (packet_id, dest)
                    # continue
                else:
                    packets_forwarded += 1

    except socket.error as err:
        print 'Error: unable to listen to or connect to the specified UDP port: ' + str(port)
        sys.exit(1)

if __name__ == "__main__":
    # try:
    main()
    # except KeyboardInterrupt as err:
    #     print 'Warning: terminated by user'

    # tables = read_route_table('route_table.txt')
