#!/usr/bin/env python3
from gnuradio import gr
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
import struct
import numpy as np
import threading
import queue
import time

class AX25Packetizer(gr.sync_block):
    # Custom block for AX.25 packet formation + response handling
    def __init__(self):
        gr.sync_block.__init__(
            self,
            name="AX25 Packetizer",
            in_sig=[np.uint8],
            out_sig=[np.uint8]
        )
        self.packet_buffer = []
        self.sequence_number = 0
        self.response_queue = queue.Queue()
        self.waiting_for_ack = False
        
    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        
        # Check for pending responses first
        try:
            response = self.response_queue.get_nowait()
            response_packet = self.create_response_packet(response)
            out[:len(response_packet)] = response_packet
            return len(response_packet)
        except queue.Empty:
            pass
        
        # If waiting for acknowledgment, don't send new data
        if self.waiting_for_ack:
            return 0
            
        for byte in in0:
            self.packet_buffer.append(byte)
            
            if len(self.packet_buffer) >= 256:
                packet = self.create_information_packet()
                out[:len(packet)] = packet
                self.packet_buffer = []
                self.waiting_for_ack = True
                return len(packet)
                
        return 0
    
    def create_information_packet(self):
        # Create an information packet with sequence numbers
        packet = []
        
        # Add header fields
        packet.extend([0xFF] * 6)  # DST address
        packet.append(0x00)        # SSID
        packet.extend([0xFF] * 6)  # SRC address
        packet.append(0x00)        # SSID
        
        # Control field with sequence numbers
        control = 0x00 | ((self.sequence_number & 0x07) << 1)  # I-frame
        packet.append(control)
        
        packet.append(0xF0)        # PID field
        packet.extend(self.packet_buffer[:256])
        
        # Calculate and add FCS
        crc = self.calculate_crc(packet)
        packet.extend([crc >> 8, crc & 0xFF])
        
        return packet
    
    def create_response_packet(self, response_type):
        # Create a response packet (RR, RNR, or REJ)
        packet = []
        
        # Swap addresses for response
        packet.extend(self.last_src_addr)  # Original source becomes destination
        packet.append(self.last_src_ssid)
        packet.extend(self.last_dst_addr)  # Original destination becomes source
        packet.append(self.last_dst_ssid)
        
        # Control field for response
        if response_type == "RR":
            control = 0x01 | ((self.sequence_number & 0x07) << 5)  # RR (Receive Ready)
        elif response_type == "RNR":
            control = 0x05 | ((self.sequence_number & 0x07) << 5)  # RNR (Receive Not Ready)
        else:  # REJ
            control = 0x09 | ((self.sequence_number & 0x07) << 5)  # REJ (Reject)
            
        packet.append(control)
        packet.append(0xF0)  # PID
        
        # Calculate and add FCS
        crc = self.calculate_crc(packet)
        packet.extend([crc >> 8, crc & 0xFF])
        
        return packet

