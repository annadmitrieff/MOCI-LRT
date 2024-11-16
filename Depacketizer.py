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

class AX25Depacketizer(gr.sync_block):
    # Custom block for AX.25 packet deformation with response handling
    def __init__(self):
        gr.sync_block.__init__(
            self,
            name="AX25 Depacketizer",
            in_sig=[np.uint8],
            out_sig=[np.uint8]
        )
        self.packet_buffer = []
        self.HEADER_LENGTH = 16
        self.MIN_PACKET_LENGTH = self.HEADER_LENGTH + 3
        self.expected_sequence = 0
        self.last_received_sequence = -1
        
    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        
        output_count = 0
        
        for byte in in0:
            self.packet_buffer.append(byte)
            
            while len(self.packet_buffer) >= self.MIN_PACKET_LENGTH:
                frame = self.find_valid_packet()
                
                if frame:
                    if frame.is_response:
                        self.handle_response(frame)
                    else:
                        # Handle information frame
                        received_seq = (frame.control >> 1) & 0x07
                        
                        if received_seq == self.expected_sequence:
                            # Extract and output data
                            data = frame.data
                            if output_count + len(data) <= len(output_items[0]):
                                out[output_count:output_count + len(data)] = data
                                output_count += len(data)
                                
                                # Send RR response
                                self.send_response("RR")
                                self.expected_sequence = (self.expected_sequence + 1) & 0x07
                        else:
                            # Send REJ response for unexpected sequence
                            self.send_response("REJ")
                            
                        self.packet_buffer = self.packet_buffer[len(frame):]
                else:
                    self.packet_buffer.pop(0)
                    
        return output_count
    
    def send_response(self, response_type):
        """Queue a response packet"""
        if hasattr(self, 'packetizer'):
            self.packetizer.response_queue.put(response_type)

