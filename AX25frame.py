#!/usr/bin/env python3

class AX25Frame:
    # AX.25 frame structure with response handling
    def __init__(self, dst_addr, src_addr, control, pid, data):
        self.dst_addr = dst_addr
        self.src_addr = src_addr
        self.control = control
        self.pid = pid
        self.data = data
        self.needs_ack = (control & 0x10) == 0x00  # Check P/F bit
        self.frame_type = control & 0x0F
        
    @property
    def is_response(self):
        return (self.control & 0x0F) in [0x01, 0x05, 0x11]  # RR, RNR, REJ responses