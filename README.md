# Reliable Data Transmission (RDT)

## Overview

This project simulates **reliable data transmission** over an unreliable underlying system. The `RDTLayer` class was fully implemented to enable the transfer of string data over a simulated send-receive network using TCP-inspired reliability principles. The final solution successfully handles data integrity, ordering, retransmission, timeouts, and flow control under conditions with dropped, delayed, out-of-order, or corrupted packets.

---

## Components

### Provided Classes

- **UnreliableChannel**
  - Simulates unreliable packet delivery (e.g., loss, delay, errors, out-of-order delivery
- **Segment**
  - Represents a data or acknowledgment (ACK) packet
  - Includes methods for:
    - Calculating and verifying checksums
    - Storing timestamps (based on iteration count)

- **rdt_main.py**
  - Main file to simulate the system.
  - Uses the `RDTLayer` class for both client and server functionality

---

## RDTLayer Functionality

The `RDTLayer` class was developed to handle:

- Sending and receiving string data via segments
- Sending and processing ACKs
- Detecting and recovering from dropped, delayed, corrupted, or out-of-order segments
- Ensuring reliable transmission in a simulated unreliable environment

---

## Key Methods

- **`processSend()`**
  - Handles sending segments
  - Called by both client and server
  - Checks internal state and sends data appropriately within window constraints

- **`processReceiveAndSendRespond()`**
  - Handles receiving segments and sending ACKs
  - Validates and delivers correct segments to the application layer
  - Detects corrupted or out-of-order packets and responds accordingly

---

## Requirements Fulfilled

- Delivered all data correctly with **no errors**
- Successfully ran with the original `UnreliableChannel` and `Segment` classes
- Functioned even when **all unreliable features were enabled**
- Used a **flow-control window**
- Supported **pipelined transmission** (multiple segments per iteration)
- Implemented **Go-Back-N** for retransmission
- Handled **timeouts using iteration count**
- Used defined constants:
  - `PAYLOAD_SIZE`
  - `WINDOW_SIZE`
- Operated efficiently with minimal unnecessary retransmissions

---

## UnreliableChannel Features Simulated

The following types of unreliability were successfully handled:

- Dropped packets (data or ACK)
- Delayed packets by multiple iterations
- Out-of-order delivery
- Corrupted data packets (checksum failures)
- Combinations of the above

Each feature was tested incrementally using the UnreliableChannel's configuration flags.

---

## Implementation Strategy

1. **Phase 1 – Reliable Channel**  
   Verified basic sending/receiving functionality with all unreliable features disabled.

2. **Phase 2 – Introduced Packet Loss and Delay**  
   Added timeout logic and retransmission using Go-Back-N protocol.

3. **Phase 3 – Out-of-Order and Corruption Handling**  
   Added logic for sequence number validation and checksum verification.

4. **Phase 4 – Full Unreliable Environment**  
   Tested with all unreliability features enabled and confirmed correctness of data transmission and acknowledgment.

---

## Output Behavior

With full functionality implemented, the program transmits multiple strings correctly and acknowledges them efficiently. Even under extreme unreliability, all data is eventually delivered in the correct order and without corruption.

---

## Personal Contribution

All functionality of the `RDTLayer` class was implemented from scratch, including:

- Development of a **Go-Back-N** retransmission protocol
- Integration of **timeout-based retransmission** using iteration count
- Design and implementation of a **pipelined send window**
- Logic to validate checksums, detect corrupt/out-of-order segments, and manage retransmissions
- Extensive testing under progressively more unreliable conditions using the provided simulation framework

This project provided hands-on experience with transport-layer protocols and deepened understanding of reliability mechanisms used in real-world TCP communication.

---

## License

This project is part of an academic course assignment and is intended for educational use only.


## Acknowledgments

Portions of this README were developed with the assistance of ChatGPT by OpenAI.

