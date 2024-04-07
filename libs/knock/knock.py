import base64
import pickle
import socket
import pickle

from scapy.all import IP, ICMP, send, Raw


event_types = {
    0: 'access_port',
    1: 'send_ping_packet',
    2: 'send_udp_data'
}


event_fields = {
    'access_port': [('port', int, 65535), ('host', str, 'localhost')],
    'send_ping_packet': [
        ('host', str, 'localhost'),
        ('port', int, 65535),
        ('packet_length', int, 1000)],
    'send_udp_data': [('host', str, 'localhost'), ('port', int, 65535), ('data', str, 'Hello, UDP!')]
}


rule_templates = {
    'access_port': (
        "/ip firewall filter add action=add-src-to-address-list address-list={target_address_list} " +
        "address-list-timeout=30s chain=input dst-port={port} protocol=tcp comment=\"Pre-Knock " +
        "to tcp:{port} add to address list {target_address_list}\"",
        "/ip firewall filter add action=add-src-to-address-list address-list={target_address_list} " +
        "address-list-timeout=30s chain=input dst-port={port} protocol=tcp comment=\"Middle-Knock " +
        "to tcp:{port} add to address list {target_address_list} from {src_address_list}\" " +
        "src-address-list={src_address_list}",
        "/ip firewall filter add action=add-src-to-address-list address-list={target_address_list} " +
        "address-list-timeout=1h chain=input dst-port={port} protocol=tcp comment=\"Final-Knock " +
        "to tcp:{port} add to address list {target_address_list} from {src_address_list}\" " +
        "src-address-list={src_address_list}"
    ),
    'send_ping_packet': (
        "/ip firewall filter add action=add-src-to-address-list address-list={target_address_list} " +
        "address-list-timeout=30s chain=input dst-port={port} packet-size={packet_length} " +
        "protocol=icmp comment=\"Pre-Knock to icmp:{port} with packet length {packet_length} " +
        "add to address list {target_address_list}\"",
        "/ip firewall filter add action=add-src-to-address-list address-list={target_address_list} " +
        "address-list-timeout=30s chain=input dst-port={port} packet-size={packet_length} " +
        "protocol=icmp comment=\"Middle-Knock to icmp:{port} with packet length {packet_length} " +
        "add to address list {target_address_list} from {src_address_list}\" " +
        "src-address-list={src_address_list}",
        "/ip firewall filter add action=add-src-to-address-list address-list={target_address_list} " +
        "address-list-timeout=1h chain=input dst-port={port} packet-size={packet_length} " +
        "protocol=icmp comment=\"Final-Knock to icmp:{port} with packet length {packet_length} " +
        "add to address list {target_address_list} from {src_address_list}\" " +
        "src-address-list={src_address_list}"
    ),
    'send_udp_data': (
        "/ip firewall filter add action=add-src-to-address-list address-list={target_address_list} " +
        "address-list-timeout=30s chain=input dst-port={port} protocol=udp comment=\"Pre-Knock " +
        "to udp:{port} add to address list {target_address_list}\"",
        "/ip firewall filter add action=add-src-to-address-list address-list={target_address_list} " +
        "address-list-timeout=30s chain=input dst-port={port} protocol=udp comment=\"Middle-Knock " +
        "to udp:{port} add to address list {target_address_list} from {src_address_list}\" " +
        "src-address-list={src_address_list}",
        "/ip firewall filter add action=add-src-to-address-list address-list={target_address_list} " +
        "address-list-timeout=1h chain=input dst-port={port} protocol=udp comment=\"Final-Knock " +
        "to udp:{port} add to address list {target_address_list} from {src_address_list}\" " +
        "src-address-list={src_address_list}"
    ),
    'accept_knock': (
        "/ip firewall filter add action=accept chain=input dst-port={port} protocol=tcp " +
        "src-address-list={src_address_list}"
    )
}


def read_chain(input_file) -> list:
    with open(input_file, 'rb') as f:
        encoded_chain = f.read()
    decoded_chain = base64.b64decode(encoded_chain)
    chain = pickle.loads(decoded_chain)
    return chain


def write_chain(chain, output_file):
    encoded_chain = base64.b64encode(pickle.dumps(chain))
    with open(output_file, 'wb') as f:
        f.write(encoded_chain)


def access_port(host, port):
    """
    Simulates accessing a port.
    """
    print(f"Accessing port {host}:{port}")


def send_ping_packet(host, port, packet_length):
    """
    Crafts a custom ICMP echo request packet with specified packet length
    and sends it to the specified port using scapy.
    """
    print(f"Sending custom ICMP packet to {host}:{port} with length {packet_length} bytes")
    # Craft the ICMP echo request packet
    packet = IP(dst=host)/ICMP()/Raw(load=b'\x41'*packet_length)
    # Send the packet
    send(packet, verbose=False)


def send_udp_data(host, port, data):
    """
    Simulates sending data to a UDP port.
    """
    print(f"Sending data to UDP port {port}")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(data.encode(), (host, port))


executors = {
    'access_port': access_port,
    'send_ping_packet': send_ping_packet,
    'send_udp_data': send_udp_data
}
