# Note - 2 Code citations are included in this file where the code is used.

from segment import Segment


# #################################################################################################################### #
# RDTLayer                                                                                                             #
#                                                                                                                      #
# Description:                                                                                                         #
# The reliable data transfer (RDT) layer is used as a communication layer to resolve issues over an unreliable         #
# channel.                                                                                                             #
#                                                                                                                      #
#                                                                                                                      #
# Notes:                                                                                                               #
# This file is meant to be changed.                                                                                    #
#                                                                                                                      #
#                                                                                                                      #
# #################################################################################################################### #


class RDTLayer(object):
    # ################################################################################################################ #
    # Class Scope Variables                                                                                            #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    DATA_LENGTH = 4  # in characters                       # The length of the string data that will be sent per packet...
    FLOW_CONTROL_WIN_SIZE = 15  # in characters             # Receive window size for flow-control
    sendChannel = None
    receiveChannel = None
    dataToSend = ''
    currentIteration = 0  # Use this for segment 'timeouts'

    # Add items as needed

    # ################################################################################################################ #
    # __init__()                                                                                                       #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def __init__(self):
        self.sendChannel = None
        self.receiveChannel = None
        self.dataToSend = ''
        self.currentIteration = 0
        # Add items as needed
        self.current_window_size = RDTLayer.FLOW_CONTROL_WIN_SIZE
        self.seqnum = 1
        self.acknum = 1
        self.sorted_ack_segments = []
        self.sorted_payload_segments = []
        self.received_data = ""
        self.sent_packets = {}
        self.pending_packets = []
        self.countSegmentTimeouts = 0  # Implement this?
        self.sent_data_length = 0
        self.acked_data_length = 0
        self.hostname = ""

    # ################################################################################################################ #
    # setSendChannel()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable sending lower-layer channel                                                 #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setSendChannel(self, channel):
        self.sendChannel = channel

    # ################################################################################################################ #
    # setReceiveChannel()                                                                                              #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable receiving lower-layer channel                                               #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setReceiveChannel(self, channel):
        self.receiveChannel = channel

    # ################################################################################################################ #
    # setDataToSend()                                                                                                  #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the string data to send                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setDataToSend(self, data):
        self.dataToSend = data

    # ################################################################################################################ #
    # getDataReceived()                                                                                                #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to get the currently received and buffered string data, in order                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def getDataReceived(self):
        # ############################################################################################################ #
        # Identify the data that has been received...

        # print('getDataReceived(): Complete this...')

        # ############################################################################################################ #
        return self.received_data

    # ################################################################################################################ #
    # processData()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # "timeslice". Called by main once per iteration                                                                   #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processData(self):
        self.currentIteration += 1
        self.process_receive()
        self.process_send()

    # ################################################################################################################ #
    # processSend()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment sending tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #

    def process_receive(self):
        """
        Sorts and processes incoming segments for both the client and server.
        """

        # Determine host
        if len(self.dataToSend) != 0:
            self.hostname = "Client"
        else:
            self.hostname = "Server"

        # Client
        if len(self.dataToSend) != 0:

            # Process acks
            self.sort_segments()
            self.process_acks()

        # Server
        else:

            # Process payload segments
            self.sort_segments()
            self.reassemble_segments()

    def process_send(self):
        """
        Determines which segments the client and server should send each iteration. The client pipelines outgoing
        segments to fit within a flow-control window. Any segments not acked by the server are resent by the client
        after a timeout interval. The server acks all incoming segments.
        """

        # Client
        if len(self.dataToSend) != 0:
            segment_send = Segment()

            # Track indices of sent and missing packets
            index = self.seqnum - 1
            count = 0

            print("Current window size:", self.current_window_size)

            # While there is data left to send.
            if index < len(self.dataToSend):

                # Send as many segments as possible.
                while self.current_window_size >= RDTLayer.DATA_LENGTH and self.acked_data_length < len(
                        self.dataToSend):

                    # First, resend any missing packets.
                    for segment in self.sent_packets:

                        # If segment has timeout > 1
                        if self.sent_packets[segment] > 1:
                            # Update timeout value to 0.
                            self.sent_packets[segment] = 0

                            # Send segment and create new segment object
                            self.send_segment(segment, segment_send)
                            segment_send = Segment()
                            count += 1

                    if self.current_window_size > RDTLayer.DATA_LENGTH:
                        # Otherwise, send segment and create new segment object
                        self.send_segment(self.seqnum, segment_send)
                        self.sent_packets[self.seqnum] = 0  # Key = data index // value = timeouts
                        segment_send = Segment()
                        self.sent_data_length += self.DATA_LENGTH
                        self.seqnum += RDTLayer.DATA_LENGTH
                        index += self.DATA_LENGTH
                        count += 1

            # If all data has been sent, but not received
            else:

                if len(self.sent_packets) > 0:

                    # First, resend any missing packets.
                    for segment in self.sent_packets:

                        # If segment has timeout > 1
                        if self.sent_packets[segment] > 1:
                            # Update timeout value to 0.
                            self.sent_packets[segment] = 0

                            # Send segment and create new segment object
                            self.send_segment(segment, segment_send)
                            segment_send = Segment()
                            count += 1

            if len(self.dataToSend) != 0:
                print("Updated window size:", self.current_window_size)
                print("New packets sent:", count)
                print("Outstanding packets:", len(self.sent_packets))
                print()

        # Server
        else:

            # Reply with ack for every received segment
            segmentAck = Segment()  # Segment acknowledging packet(s) received
            for segment in self.sorted_payload_segments:
                acknum = segment.seqnum + self.DATA_LENGTH
                segmentAck.setAck(acknum)

                print("Sending ack: ", segmentAck.to_string())

                # Use the unreliable sendChannel to send the ack packet
                self.sendChannel.send(segmentAck)

                segmentAck = Segment()
            print()

    def send_segment(self, seq, segment):
        """
        Prepares a data segment to be sent. The sequence number determines the index of the string, which is then
        embedded the segment's payload.
        """

        index = seq - 1

        # Citation for the following code
        # Date: 02/20/25
        # Based on: String Slicing in Python
        # Source URL: https://www.geeksforgeeks.org/string-slicing-in-python/

        data = self.dataToSend[index: index + self.DATA_LENGTH]

        # Display sending segment
        segment.setData(index + 1, data)
        print("Sending segment: ", segment.to_string())

        # Use the unreliable sendChannel to send the segment
        self.sendChannel.send(segment)

        # Update variables based on segment
        self.current_window_size -= self.DATA_LENGTH

    def sort_segments(self):
        """
        Parses incoming segments and sorts them into two lists: payload segments and acks. Segments containing errors
        are not added, which negates an errors from being processed.
        """

        payload_segments = []
        ack_segments = []

        # Categorize segments
        for segment in self.receiveChannel.receive():
            if segment.seqnum == -1:

                # Only add error-free ack segments to list.
                if segment.checkChecksum() is True:
                    ack_segments.append(segment)

            else:
                # Only add error-free payload segments to list.
                if segment.checkChecksum() is True:
                    payload_segments.append(segment)

        # Update variables
        # Citation for the following code
        # Date: 02/19/25
        # Based on: Lambda functions - what are they?
        # https://blogboard.io/blog/knowledge/python-sorted-lambda/
        self.sorted_ack_segments = sorted(ack_segments, key=lambda packet: packet.acknum)
        self.sorted_payload_segments = sorted(payload_segments, key=lambda packet: packet.seqnum)

        if len(self.dataToSend) > 0:
            print("Acks received:", len(self.sorted_ack_segments))
        else:
            print("Segments received:", len(self.sorted_payload_segments))

    def reassemble_segments(self):
        """
        Reassembles incoming segments and updates the ack number as data is successfully received.
        """

        current_ack = self.acknum

        # Add zero-error segments to pending packets list
        for segment in self.sorted_payload_segments:
            self.pending_packets.append(segment)

        # Sort pending packets
        self.pending_packets = sorted(self.pending_packets, key=lambda packet: packet.seqnum)

        # Loop over list to see if it contains the segment
        while True:

            segment_found = False
            for i in range(len(self.pending_packets)):
                segment = self.pending_packets[i]
                seg_seqnum = segment.seqnum

                # Segment already received
                if seg_seqnum < current_ack:

                    # Delete from pending packets list:
                    del self.pending_packets[i]
                    break

                # If segment is found.
                elif seg_seqnum == current_ack:

                    # Add segment to received data and remove from list
                    self.received_data += segment.payload
                    del self.pending_packets[i]

                    # Update ack to look at next seq#
                    current_ack += self.DATA_LENGTH
                    self.acknum = current_ack
                    segment_found = True
                    break

                # Segment sequence > desired packed.
                else:
                    segment_found = False

            if segment_found is False:
                break

    def process_acks(self):
        """
        Reviews sorted and error-free acks sent to the client. Any received segments are removed from the
        client's sent packets list and the window size is updated.
        """

        # Remove received packets from sent packets list
        for ack in self.sorted_ack_segments:
            for segment in self.sent_packets:

                # If packet was received
                if ack.acknum - self.DATA_LENGTH == segment:
                    # Remove from list and update window size
                    del self.sent_packets[segment]
                    self.current_window_size += self.DATA_LENGTH
                    self.acked_data_length += self.DATA_LENGTH
                    print("Received ack:", ack.acknum)
                    break

        # Increment timeout values for any existing packets
        for segment in self.sent_packets:
            self.sent_packets[segment] += 1
            self.countSegmentTimeouts += 1
            print("*** Missing *** seq:", segment)

            # Increase window size if timeout > 1
            if self.sent_packets[segment] > 1:
                self.current_window_size += self.DATA_LENGTH
                print("Seq:", segment, "has timed-out")
