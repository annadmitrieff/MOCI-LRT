# Import block at the start of your flowgraph

# Transmit Path:
# [File Source/Vector Source] -> Packed to Unpacked -> Python Block (Packetizer) -> GMSK Mod -> [USRP/SDR Sink]

# Receive Path:
# [USRP/SDR Source] -> AGC -> GMSK Demod -> Packed to Unpacked -> Python Block (Depacketizer) -> [File Sink]

import numpy as np
import gnuradio as gr

from Depacketizer import AX25Depacketizer

# Python block for Depacketizer
class blk(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='AX.25 Depacketizer',
            in_sig=[np.uint8],
            out_sig=[np.uint8]
        )
        self.depacketizer = AX25Depacketizer()

    def work(self, input_items, output_items):
        return self.depacketizer.work(input_items, output_items)