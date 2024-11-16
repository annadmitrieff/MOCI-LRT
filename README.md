
### Files and Descriptions
#### `AX25frame.py`:
Interpreter for the AX.25 protocol framework.

- **Attributes**:
  - `dst_addr`: Destination address of the frame.
  - `src_addr`: Source address of the frame.
  - `control`: Control field determining the frame's type and associated features.
  - `pid`: Protocol identifier.
  - `data`: Payload of the frame.

- **Methods and Properties**:
  - `needs_ack`: Determines if the frame requires acknowledgment (`ACK`) based on the Poll/Final (`P/F`) bit in the control field. `control & 0x10 == 0x00` indicates a frame that requests acknowledgment.
  - `frame_type`: Extracts the frame type from the lower 4 bits of the `control` field (`control & 0x0F`).
  - `is_response`: Read-only property that checks if the frame is a response frame. Matches lower 4 bits of `control` to response types:
    - `RR` (Receive Ready): `0x01`
    - `RNR` (Receive Not Ready): `0x05`
    - `REJ` (Reject): `0x11`

#### `Depacketizer.py`:
Processes incoming frames and extracts the payload by reversing the packetization process.

- **Purpose**:
  - Extracts useful data from incoming packets by verifying and interpreting the encapsulated AX.25 frame.
  - Strips framing overhead while maintaining data integrity.

#### `Packetizer.py`:
Encodes data into packets suitable for transmission.

- **Purpose**:
  - Adds framing and checksum information.
  - Structures data into a format adhering to AX.25 protocol standards.

#### `GRCDepacketizerBlock.py`:
Custom GNU Radio Companion (GRC) block for depacketization.

- **Purpose**:
  - Integrates with GNU Radio to enable real-time depacketization within a flowgraph.

#### `GRCPacketizerBlock.py`:
Custom GRC block for packetization.

- **Purpose**:
  - Integrates with GNU Radio for real-time packetization of outgoing data streams.

#### `GRCflowgraph.grc`:
GNU Radio flowgraph in `.grc` format.

- **Purpose**:
  - Defines the structure and connections of blocks for real-time signal processing.
