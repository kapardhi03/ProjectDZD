import argparse
from scapy.sendrecv import AsyncSniffer
import csv
from collections import defaultdict
from scapy.sessions import DefaultSession
from enum import Enum
from typing import Any
import uuid
from itertools import islice, zip_longest
import numpy
import multiprocessing
import time
import warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("default")


### sniffer.py calling generate_session_class from flow_session.py

# from .flow_session import generate_session_class

def create_sniffer(
    input_file, input_interface, output_mode, output_file, url_model=None
):
    assert (input_file is None) ^ (input_interface is None)

    NewFlowSession = generate_session_class(output_mode, output_file, url_model)

    if input_file is not None:
        return AsyncSniffer(
            offline=input_file,
            filter="ip and (tcp or udp)",
            prn=None,
            session=NewFlowSession,
            store=False,
        )
    else:
        return AsyncSniffer(
            iface=input_interface,
            filter="ip and (tcp or udp)",
            prn=None,
            session=NewFlowSession,
            store=False,
        )

def main():
    args = argparse.Namespace()
    args.input_interface = "Wi-Fi"
    args.output_mode = "flow"
    args.output = "flows.csv"
    args.url_model = None  # Assuming it's not required

    sniffer = create_sniffer(
        None,
        args.input_interface,
        args.output_mode,
        args.output,
        None,
    )
    sniffer.start()
    
    try:
        sniffer.join()
    except KeyboardInterrupt:
        sniffer.stop()
    finally:
        sniffer.join()


###flow_session.py calling Flow from flow

# from ciccontext import PacketDirection
# from ciccontext import get_packet_flow_key
# from .flow import Flow

EXPIRED_UPDATE = 40
MACHINE_LEARNING_API = "http://localhost:8000/predict"
GARBAGE_COLLECT_PACKETS = 100


class FlowSession(DefaultSession):
    """Creates a list of network flows."""

    def __init__(self, *args, **kwargs):
        self.flows = {}
        self.csv_line = 0

        if self.output_mode == "flow":
            output = open(self.output_file, "w")
            self.csv_writer = csv.writer(output)

        self.packets_count = 0

        self.clumped_flows_per_label = defaultdict(list)

        super(FlowSession, self).__init__(*args, **kwargs)

    def toPacketList(self):
        # Sniffer finished all the packets it needed to sniff.
        # It is not a good place for this, we need to somehow define a finish signal for AsyncSniffer
        self.garbage_collect(None)
        return super(FlowSession, self).toPacketList()

    def on_packet_received(self, packet):
        count = 0
        direction = PacketDirection.FORWARD

        if self.output_mode != "flow":
            if "TCP" not in packet:
                return
            elif "UDP" not in packet:
                return

        try:
            # Creates a key variable to check
            packet_flow_key = get_packet_flow_key(packet, direction)
            flow = self.flows.get((packet_flow_key, count))
        except Exception:
            return

        self.packets_count += 1

        # If there is no forward flow with a count of 0
        if flow is None:
            # There might be one of it in reverse
            direction = PacketDirection.REVERSE
            packet_flow_key = get_packet_flow_key(packet, direction)
            flow = self.flows.get((packet_flow_key, count))

        if flow is None:
            # If no flow exists create a new flow
            direction = PacketDirection.FORWARD
            flow = Flow(packet, direction)
            packet_flow_key = get_packet_flow_key(packet, direction)
            self.flows[(packet_flow_key, count)] = flow

        elif (packet.time - flow.latest_timestamp) > EXPIRED_UPDATE:
            # If the packet exists in the flow but the packet is sent
            # after too much of a delay than it is a part of a new flow.
            expired = EXPIRED_UPDATE
            while (packet.time - flow.latest_timestamp) > expired:
                count += 1
                expired += EXPIRED_UPDATE
                flow = self.flows.get((packet_flow_key, count))

                if flow is None:
                    flow = Flow(packet, direction)
                    self.flows[(packet_flow_key, count)] = flow
                    break
        elif "F" in str(packet.flags):
            # If it has FIN flag then early collect flow and continue
            flow.add_packet(packet, direction)
            self.garbage_collect(packet.time)
            return

        flow.add_packet(packet, direction)

        if not self.url_model:
            GARBAGE_COLLECT_PACKETS = 10000

        if self.packets_count % GARBAGE_COLLECT_PACKETS == 0 or (
            flow.duration > 120 and self.output_mode == "flow"
        ):
            self.garbage_collect(packet.time)

    def get_flows(self) -> list:
        return self.flows.values()

    def garbage_collect(self, latest_time) -> None:
        # TODO: Garbage Collection / Feature Extraction should have a separate thread
        if not self.url_model:
            print("Garbage Collection Began. Flows = {}".format(len(self.flows)))
        keys = list(self.flows.keys())
        for k in keys:
            flow = self.flows.get(k)

            if (
                latest_time is None
                or latest_time - flow.latest_timestamp > EXPIRED_UPDATE
                or flow.duration > 90
            ):
                data = flow.get_data()

                if self.csv_line == 0:
                    self.csv_writer.writerow(data.keys())

                self.csv_writer.writerow(data.values())
                self.csv_line += 1

                del self.flows[k]
        if not self.url_model:
            print("Garbage Collection Finished. Flows = {}".format(len(self.flows)))


def generate_session_class(output_mode, output_file, url_model):
    return type(
        "NewFlowSession",
        (FlowSession,),
        {
            "output_mode": output_mode,
            "output_file": output_file,
            "url_model": url_model,
        },
    )


## flow.py calling get_statistics from utils.py

# from . import constants
class const():
    def __init__(self):
        self.EXPIRED_UPDATE = 240
        self.CLUMP_TIMEOUT = 1
        self.ACTIVE_TIMEOUT = 0.005
        self.BULK_BOUND = 4
constants = const()

# from ciccontext import get_packet_flow_key
# from ciccontext import PacketDirection
# from ciccontext import FlagCount
# from ciccontext import FlowBytes
# from ciccontext import PacketCount
# from ciccontext import PacketLength
# from ciccontext import PacketTime
# from .utils import get_statistics


class Flow:
    """This class summarizes the values of the features of the network flows"""

    def __init__(self, packet: Any, direction: Enum):
        """This method initializes an object from the Flow class.

        Args:
            packet (Any): A packet from the network.
            direction (Enum): The direction the packet is going ove the wire.
        """

        (
            self.dest_ip,
            self.src_ip,
            self.src_port,
            self.dest_port,
        ) = get_packet_flow_key(packet, direction)

        self.packets = []
        self.flow_interarrival_time = []
        self.latest_timestamp = 0
        self.start_timestamp = 0
        self.init_window_size = {
            PacketDirection.FORWARD: 0,
            PacketDirection.REVERSE: 0,
        }

        self.start_active = 0
        self.last_active = 0
        self.active = []
        self.idle = []

        self.forward_bulk_last_timestamp = 0
        self.forward_bulk_start_tmp = 0
        self.forward_bulk_count = 0
        self.forward_bulk_count_tmp = 0
        self.forward_bulk_duration = 0
        self.forward_bulk_packet_count = 0
        self.forward_bulk_size = 0
        self.forward_bulk_size_tmp = 0
        self.backward_bulk_last_timestamp = 0
        self.backward_bulk_start_tmp = 0
        self.backward_bulk_count = 0
        self.backward_bulk_count_tmp = 0
        self.backward_bulk_duration = 0
        self.backward_bulk_packet_count = 0
        self.backward_bulk_size = 0
        self.backward_bulk_size_tmp = 0

    def get_data(self) -> dict:
        """This method obtains the values of the features extracted from each flow.

        Note:
            Only some of the network data plays well together in this list.
            Time-to-live values, window values, and flags cause the data to
            separate out too much.

        Returns:
           list: returns a List of values to be outputted into a csv file.

        """

        flow_bytes = FlowBytes(self)
        flag_count = FlagCount(self)
        packet_count = PacketCount(self)
        packet_length = PacketLength(self)
        packet_time = PacketTime(self)
        flow_iat = get_statistics(self.flow_interarrival_time)
        forward_iat = get_statistics(
            packet_time.get_packet_iat(PacketDirection.FORWARD)
        )
        backward_iat = get_statistics(
            packet_time.get_packet_iat(PacketDirection.REVERSE)
        )
        active_stat = get_statistics(self.active)
        idle_stat = get_statistics(self.idle)

        data = {
            # Basic IP information
            "src_ip": self.src_ip,
            "dst_ip": self.dest_ip,
            "src_port": self.src_port,
            "dst_port": self.dest_port,
            "protocol": self.protocol,
            # Basic information from packet times
            "timestamp": packet_time.get_time_stamp(),
            "flow_duration": 1e6 * packet_time.get_duration(),
            "flow_byts_s": flow_bytes.get_rate(),
            "flow_pkts_s": packet_count.get_rate(),
            "fwd_pkts_s": packet_count.get_rate(PacketDirection.FORWARD),
            "bwd_pkts_s": packet_count.get_rate(PacketDirection.REVERSE),
            # Count total packets by direction
            "tot_fwd_pkts": packet_count.get_total(PacketDirection.FORWARD),
            "tot_bwd_pkts": packet_count.get_total(PacketDirection.REVERSE),
            # Statistical info obtained from Packet lengths
            "totlen_fwd_pkts": packet_length.get_total(PacketDirection.FORWARD),
            "totlen_bwd_pkts": packet_length.get_total(PacketDirection.REVERSE),
            "fwd_pkt_len_max": float(packet_length.get_max(PacketDirection.FORWARD)),
            "fwd_pkt_len_min": float(packet_length.get_min(PacketDirection.FORWARD)),
            "fwd_pkt_len_mean": float(packet_length.get_mean(PacketDirection.FORWARD)),
            "fwd_pkt_len_std": float(packet_length.get_std(PacketDirection.FORWARD)),
            "bwd_pkt_len_max": float(packet_length.get_max(PacketDirection.REVERSE)),
            "bwd_pkt_len_min": float(packet_length.get_min(PacketDirection.REVERSE)),
            "bwd_pkt_len_mean": float(packet_length.get_mean(PacketDirection.REVERSE)),
            "bwd_pkt_len_std": float(packet_length.get_std(PacketDirection.REVERSE)),
            "pkt_len_max": packet_length.get_max(),
            "pkt_len_min": packet_length.get_min(),
            "pkt_len_mean": float(packet_length.get_mean()),
            "pkt_len_std": float(packet_length.get_std()),
            "pkt_len_var": float(packet_length.get_var()),
            "fwd_header_len": flow_bytes.get_forward_header_bytes(),
            "bwd_header_len": flow_bytes.get_reverse_header_bytes(),
            "fwd_seg_size_min": flow_bytes.get_min_forward_header_bytes(),
            "fwd_act_data_pkts": packet_count.has_payload(PacketDirection.FORWARD),
            # Flows Interarrival Time
            "flow_iat_mean": float(flow_iat["mean"]),
            "flow_iat_max": float(flow_iat["max"]),
            "flow_iat_min": float(flow_iat["min"]),
            "flow_iat_std": float(flow_iat["std"]),
            "fwd_iat_tot": forward_iat["total"],
            "fwd_iat_max": float(forward_iat["max"]),
            "fwd_iat_min": float(forward_iat["min"]),
            "fwd_iat_mean": float(forward_iat["mean"]),
            "fwd_iat_std": float(forward_iat["std"]),
            "bwd_iat_tot": float(backward_iat["total"]),
            "bwd_iat_max": float(backward_iat["max"]),
            "bwd_iat_min": float(backward_iat["min"]),
            "bwd_iat_mean": float(backward_iat["mean"]),
            "bwd_iat_std": float(backward_iat["std"]),
            # Flags statistics
            "fwd_psh_flags": flag_count.has_flag("PSH", PacketDirection.FORWARD),
            "bwd_psh_flags": flag_count.has_flag("PSH", PacketDirection.REVERSE),
            "fwd_urg_flags": flag_count.has_flag("URG", PacketDirection.FORWARD),
            "bwd_urg_flags": flag_count.has_flag("URG", PacketDirection.REVERSE),
            "fin_flag_cnt": flag_count.has_flag("FIN"),
            "syn_flag_cnt": flag_count.has_flag("SYN"),
            "rst_flag_cnt": flag_count.has_flag("RST"),
            "psh_flag_cnt": flag_count.has_flag("PSH"),
            "ack_flag_cnt": flag_count.has_flag("ACK"),
            "urg_flag_cnt": flag_count.has_flag("URG"),
            "ece_flag_cnt": flag_count.has_flag("ECE"),
            # Response Time
            "down_up_ratio": packet_count.get_down_up_ratio(),
            "pkt_size_avg": packet_length.get_avg(),
            "init_fwd_win_byts": self.init_window_size[PacketDirection.FORWARD],
            "init_bwd_win_byts": self.init_window_size[PacketDirection.REVERSE],
            "active_max": float(active_stat["max"]),
            "active_min": float(active_stat["min"]),
            "active_mean": float(active_stat["mean"]),
            "active_std": float(active_stat["std"]),
            "idle_max": float(idle_stat["max"]),
            "idle_min": float(idle_stat["min"]),
            "idle_mean": float(idle_stat["mean"]),
            "idle_std": float(idle_stat["std"]),
            "fwd_byts_b_avg": float(
                flow_bytes.get_bytes_per_bulk(PacketDirection.FORWARD)
            ),
            "fwd_pkts_b_avg": float(
                flow_bytes.get_packets_per_bulk(PacketDirection.FORWARD)
            ),
            "bwd_byts_b_avg": float(
                flow_bytes.get_bytes_per_bulk(PacketDirection.REVERSE)
            ),
            "bwd_pkts_b_avg": float(
                flow_bytes.get_packets_per_bulk(PacketDirection.REVERSE)
            ),
            "fwd_blk_rate_avg": float(
                flow_bytes.get_bulk_rate(PacketDirection.FORWARD)
            ),
            "bwd_blk_rate_avg": float(
                flow_bytes.get_bulk_rate(PacketDirection.REVERSE)
            ),
        }

        # Duplicated features
        data["fwd_seg_size_avg"] = data["fwd_pkt_len_mean"]
        data["bwd_seg_size_avg"] = data["bwd_pkt_len_mean"]
        data["cwe_flag_count"] = data["fwd_urg_flags"]
        data["subflow_fwd_pkts"] = data["tot_fwd_pkts"]
        data["subflow_bwd_pkts"] = data["tot_bwd_pkts"]
        data["subflow_fwd_byts"] = data["totlen_fwd_pkts"]
        data["subflow_bwd_byts"] = data["totlen_bwd_pkts"]

        return data

    def add_packet(self, packet: Any, direction: Enum) -> None:
        """Adds a packet to the current list of packets.

        Args:
            packet: Packet to be added to a flow
            direction: The direction the packet is going in that flow

        """
        self.packets.append((packet, direction))

        self.update_flow_bulk(packet, direction)
        self.update_subflow(packet)

        if self.start_timestamp != 0:
            self.flow_interarrival_time.append(
                1e6 * (packet.time - self.latest_timestamp)
            )

        self.latest_timestamp = max([packet.time, self.latest_timestamp])

        if "TCP" in packet:
            if (
                direction == PacketDirection.FORWARD
                and self.init_window_size[direction] == 0
            ):
                self.init_window_size[direction] = packet["TCP"].window
            elif direction == PacketDirection.REVERSE:
                self.init_window_size[direction] = packet["TCP"].window

        # First packet of the flow
        if self.start_timestamp == 0:
            self.start_timestamp = packet.time
            self.protocol = packet.proto

    def update_subflow(self, packet):
        """Update subflow

        Args:
            packet: Packet to be parse as subflow

        """
        last_timestamp = (
            self.latest_timestamp if self.latest_timestamp != 0 else packet.time
        )
        if (packet.time - last_timestamp) > constants.CLUMP_TIMEOUT:
            self.update_active_idle(packet.time - last_timestamp)

    def update_active_idle(self, current_time):
        """Adds a packet to the current list of packets.

        Args:
            packet: Packet to be update active time

        """
        if (current_time - self.last_active) > constants.ACTIVE_TIMEOUT:
            duration = abs(float(self.last_active - self.start_active))
            if duration > 0:
                self.active.append(1e6 * duration)
            self.idle.append(1e6 * (current_time - self.last_active))
            self.start_active = current_time
            self.last_active = current_time
        else:
            self.last_active = current_time

    def update_flow_bulk(self, packet, direction):
        """Update bulk flow

        Args:
            packet: Packet to be parse as bulk

        """
        payload_size = len(PacketCount.get_payload(packet))
        if payload_size == 0:
            return
        if direction == PacketDirection.FORWARD:
            if self.backward_bulk_last_timestamp > self.forward_bulk_start_tmp:
                self.forward_bulk_start_tmp = 0
            if self.forward_bulk_start_tmp == 0:
                self.forward_bulk_start_tmp = packet.time
                self.forward_bulk_last_timestamp = packet.time
                self.forward_bulk_count_tmp = 1
                self.forward_bulk_size_tmp = payload_size
            else:
                if (
                    packet.time - self.forward_bulk_last_timestamp
                ) > constants.CLUMP_TIMEOUT:
                    self.forward_bulk_start_tmp = packet.time
                    self.forward_bulk_last_timestamp = packet.time
                    self.forward_bulk_count_tmp = 1
                    self.forward_bulk_size_tmp = payload_size
                else:  # Add to bulk
                    self.forward_bulk_count_tmp += 1
                    self.forward_bulk_size_tmp += payload_size
                    if self.forward_bulk_count_tmp == constants.BULK_BOUND:
                        self.forward_bulk_count += 1
                        self.forward_bulk_packet_count += self.forward_bulk_count_tmp
                        self.forward_bulk_size += self.forward_bulk_size_tmp
                        self.forward_bulk_duration += (
                            packet.time - self.forward_bulk_start_tmp
                        )
                    elif self.forward_bulk_count_tmp > constants.BULK_BOUND:
                        self.forward_bulk_packet_count += 1
                        self.forward_bulk_size += payload_size
                        self.forward_bulk_duration += (
                            packet.time - self.forward_bulk_last_timestamp
                        )
                    self.forward_bulk_last_timestamp = packet.time
        else:
            if self.forward_bulk_last_timestamp > self.backward_bulk_start_tmp:
                self.backward_bulk_start_tmp = 0
            if self.backward_bulk_start_tmp == 0:
                self.backward_bulk_start_tmp = packet.time
                self.backward_bulk_last_timestamp = packet.time
                self.backward_bulk_count_tmp = 1
                self.backward_bulk_size_tmp = payload_size
            else:
                if (
                    packet.time - self.backward_bulk_last_timestamp
                ) > constants.CLUMP_TIMEOUT:
                    self.backward_bulk_start_tmp = packet.time
                    self.backward_bulk_last_timestamp = packet.time
                    self.backward_bulk_count_tmp = 1
                    self.backward_bulk_size_tmp = payload_size
                else:  # Add to bulk
                    self.backward_bulk_count_tmp += 1
                    self.backward_bulk_size_tmp += payload_size
                    if self.backward_bulk_count_tmp == constants.BULK_BOUND:
                        self.backward_bulk_count += 1
                        self.backward_bulk_packet_count += self.backward_bulk_count_tmp
                        self.backward_bulk_size += self.backward_bulk_size_tmp
                        self.backward_bulk_duration += (
                            packet.time - self.backward_bulk_start_tmp
                        )
                    elif self.backward_bulk_count_tmp > constants.BULK_BOUND:
                        self.backward_bulk_packet_count += 1
                        self.backward_bulk_size += payload_size
                        self.backward_bulk_duration += (
                            packet.time - self.backward_bulk_last_timestamp
                        )
                    self.backward_bulk_last_timestamp = packet.time

    @property
    def duration(self):
        return self.latest_timestamp - self.start_timestamp

###utils.py

def grouper(iterable, n, max_groups=0, fillvalue=None):
    """Collect data into fixed-length chunks or blocks"""

    if max_groups > 0:
        iterable = islice(iterable, max_groups * n)

    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def random_string():
    return uuid.uuid4().hex[:6].upper().replace("0", "X").replace("O", "Y")


def get_statistics(alist: list):
    """Get summary statistics of a list"""
    iat = dict()

    if len(alist) > 1:
        iat["total"] = sum(alist)
        iat["max"] = max(alist)
        iat["min"] = min(alist)
        iat["mean"] = numpy.mean(alist)
        iat["std"] = numpy.sqrt(numpy.var(alist))
    else:
        iat["total"] = 0
        iat["max"] = 0
        iat["min"] = 0
        iat["mean"] = 0
        iat["std"] = 0

    return iat

#!/usr/bin/env python
from enum import Enum, auto
from scapy.layers.inet import IP, TCP
from datetime import datetime
import numpy
from scipy import stats as stat
import numpy
from scipy import stats as stat


#packetdirection.py ----------------------------------------------------

class PacketDirection(Enum):
    """Packet Direction creates constants for the direction of the packets.

    There are two given directions that the packets can Feature along
    the line. PacketDirection is an enumeration with the values
    forward (1) and reverse (2).
    """

    FORWARD = auto()
    REVERSE = auto()

#######packet_flow_key.py calling Packetdirection from packetdirection.py

#!/usr/bin/env python
# from .packet_direction import PacketDirection


def get_packet_flow_key(packet, direction) -> tuple:
    """Creates a key signature for a packet.

    Summary:
        Creates a key signature for a packet so it can be
        assigned to a flow.

    Args:
        packet: A network packet
        direction: The direction of a packet

    Returns:
        A tuple of the String IPv4 addresses of the destination,
        the source port as an int,
        the time to live value,
        the window size, and
        TCP flags.

    """

    if "TCP" in packet:
        protocol = "TCP"
    elif "UDP" in packet:
        protocol = "UDP"
    else:
        raise Exception("Only TCP protocols are supported.")

    if direction == PacketDirection.FORWARD:
        dest_ip = packet["IP"].dst
        src_ip = packet["IP"].src
        src_port = packet[protocol].sport
        dest_port = packet[protocol].dport
    else:
        dest_ip = packet["IP"].src
        src_ip = packet["IP"].dst
        src_port = packet[protocol].dport
        dest_port = packet[protocol].sport

    return dest_ip, src_ip, src_port, dest_port

#flagcount.py----------------------------------------------------------------

class FlagCount:
    """This class extracts features related to the Flags Count."""

    def __init__(self, feature):
        self.feature = feature
        self.flags = {
            "F": "FIN",
            "S": "SYN",
            "R": "RST",
            "P": "PSH",
            "A": "ACK",
            "U": "URG",
            "E": "ECE",
            "C": "CWR",
        }

    def has_flag(self, flag, packet_direction=None) -> bool:
        """Count packets by direction.

        Returns:
            packets_count (int):

        """
        packets = (
            (
                packet
                for packet, direction in self.feature.packets
                if direction == packet_direction
            )
            if packet_direction is not None
            else (packet for packet, _ in self.feature.packets)
        )

        for packet in packets:
            if flag[0] in str(packet.flags):
                return 1
        return 0

#flow_bytes.py calling ----------------------------------------------------

# from .context.packet_direction import PacketDirection
# from .packet_time import PacketTime


class FlowBytes:
    """Extracts features from the traffic related to the bytes in a flow"""

    def __init__(self, feature):
        self.feature = feature

    def direction_list(self) -> list:
        """Returns a list of the directions of the first 50 packets in a flow.

        Return:
            list with packet directions.

        """
        feat = self.feature
        direction_list = [
            (i, direction.name)[1]
            for (i, (packet, direction)) in enumerate(feat.packets)
            if i < 50
        ]
        return direction_list

    def get_bytes(self) -> int:
        """Calculates the amount bytes being transfered.

        Returns:
            int: The amount of bytes.

        """
        feat = self.feature

        return sum(len(packet) for packet, _ in feat.packets)

    def get_rate(self) -> float:
        """Calculates the rate of the bytes being transfered in the current flow.

        Returns:
            float: The bytes/sec sent.

        """
        duration = PacketTime(self.feature).get_duration()

        if duration == 0:
            rate = 0
        else:
            rate = self.get_bytes() / duration

        return rate

    def get_bytes_sent(self) -> int:
        """Calculates the amount bytes sent from the machine being used to run DoHlyzer.

        Returns:
            int: The amount of bytes.

        """
        feat = self.feature

        return sum(
            len(packet)
            for packet, direction in feat.packets
            if direction == PacketDirection.FORWARD
        )

    def get_sent_rate(self) -> float:
        """Calculates the rate of the bytes being sent in the current flow.

        Returns:
            float: The bytes/sec sent.

        """
        sent = self.get_bytes_sent()
        duration = PacketTime(self.feature).get_duration()

        if duration == 0:
            rate = -1
        else:
            rate = sent / duration

        return rate

    def get_bytes_received(self) -> int:
        """Calculates the amount bytes received.

        Returns:
            int: The amount of bytes.

        """
        packets = self.feature.packets

        return sum(
            len(packet)
            for packet, direction in packets
            if direction == PacketDirection.REVERSE
        )

    def get_received_rate(self) -> float:
        """Calculates the rate of the bytes being received in the current flow.

        Returns:
            float: The bytes/sec received.

        """
        received = self.get_bytes_received()
        duration = PacketTime(self.feature).get_duration()

        if duration == 0:
            rate = -1
        else:
            rate = received / duration

        return rate

    def get_forward_header_bytes(self) -> int:
        """Calculates the amount of header bytes in the header sent in the same direction as the flow.

        Returns:
            int: The amount of bytes.

        """

        packets = self.feature.packets

        return sum(
            self._header_size(packet)
            for packet, direction in packets
            if direction == PacketDirection.FORWARD
        )

    def get_forward_rate(self) -> int:
        """Calculates the rate of the bytes being going forward
        in the current flow.

        Returns:
            float: The bytes/sec forward.

        """
        forward = self.get_forward_header_bytes()
        duration = PacketTime(self.feature).get_duration()

        if duration > 0:
            rate = forward / duration
        else:
            rate = -1

        return rate

    def _header_size(self, packet):
        return packet[IP].ihl * 4 if TCP in packet else 8

    def get_reverse_header_bytes(self) -> int:
        """Calculates the amount of header bytes in the header sent in the opposite direction as the flow.

        Returns:
            int: The amount of bytes.

        """

        packets = self.feature.packets

        if not packets:
            return 0

        return sum(
            self._header_size(packet)
            for packet, direction in packets
            if direction == PacketDirection.REVERSE
        )

    def get_min_forward_header_bytes(self) -> int:
        """Calculates the amount of header bytes in the header sent in the opposite direction as the flow.

        Returns:
            int: The amount of bytes.

        """

        packets = self.feature.packets

        if not packets:
            return 0

        return min(
            self._header_size(packet)
            for packet, direction in packets
            if direction == PacketDirection.FORWARD
        )

    def get_reverse_rate(self) -> int:
        """Calculates the rate of the bytes being going reverse
        in the current flow.

        Returns:
            float: The bytes/sec reverse.

        """
        reverse = self.get_reverse_header_bytes()
        duration = PacketTime(self.feature).get_duration()

        if duration == 0:
            rate = -1
        else:
            rate = reverse / duration

        return rate

    def get_header_in_out_ratio(self) -> float:
        """Calculates the ratio of foward traffic over reverse traffic.

        Returns:
            float: The ratio over reverse traffic.
            If the reverse header bytes is 0 this returns -1 to avoid
            a possible division by 0.

        """
        reverse_header_bytes = self.get_reverse_header_bytes()
        forward_header_bytes = self.get_forward_header_bytes()

        ratio = -1
        if reverse_header_bytes != 0:
            ratio = forward_header_bytes / reverse_header_bytes

        return ratio

    def get_initial_ttl(self) -> int:
        """Obtains the initial time-to-live value.

        Returns:
            int: The initial ttl value in seconds.

        """
        feat = self.feature
        return [packet["IP"].ttl for packet, _ in feat.packets][0]

    def get_bytes_per_bulk(self, packet_direction):
        if packet_direction == PacketDirection.FORWARD:
            if self.feature.forward_bulk_count != 0:
                return self.feature.forward_bulk_size / self.feature.forward_bulk_count
        else:
            if self.feature.backward_bulk_count != 0:
                return (
                    self.feature.backward_bulk_size / self.feature.backward_bulk_count
                )
        return 0

    def get_packets_per_bulk(self, packet_direction):
        if packet_direction == PacketDirection.FORWARD:
            if self.feature.forward_bulk_count != 0:
                return (
                    self.feature.forward_bulk_packet_count
                    / self.feature.forward_bulk_count
                )
        else:
            if self.feature.backward_bulk_count != 0:
                return (
                    self.feature.backward_bulk_packet_count
                    / self.feature.backward_bulk_count
                )
        return 0

    def get_bulk_rate(self, packet_direction):
        if packet_direction == PacketDirection.FORWARD:
            if self.feature.forward_bulk_count != 0:
                return (
                    self.feature.forward_bulk_size / self.feature.forward_bulk_duration
                )
        else:
            if self.feature.backward_bulk_count != 0:
                return (
                    self.feature.backward_bulk_size
                    / self.feature.backward_bulk_duration
                )
        return 0

#packet_time.py ---------------------------------------------------

class PacketTime:
    """This class extracts features related to the Packet Times."""

    count = 0

    def __init__(self, flow):
        self.flow = flow
        PacketTime.count += 1
        self.packet_times = None

    def _get_packet_times(self):
        """Gets a list of the times of the packets on a flow

        Returns:
            A list of the packet times.

        """
        if self.packet_times is not None:
            return self.packet_times
        first_packet_time = self.flow.packets[0][0].time
        packet_times = [
            float(packet.time - first_packet_time) for packet, _ in self.flow.packets
        ]
        return packet_times

    def get_packet_iat(self, packet_direction=None):
        if packet_direction is not None:
            packets = [
                packet
                for packet, direction in self.flow.packets
                if direction == packet_direction
            ]
        else:
            packets = [packet for packet, direction in self.flow.packets]

        packet_iat = []
        for i in range(1, len(packets)):
            packet_iat.append(1e6 * float(packets[i].time - packets[i - 1].time))

        return packet_iat

    def relative_time_list(self):
        relative_time_list = []
        packet_times = self._get_packet_times()
        for index, time in enumerate(packet_times):
            if index == 0:
                relative_time_list.append(0)
            elif index < len(packet_times):
                relative_time_list.append(float(time - packet_times[index - 1]))
            elif index < 50:
                relative_time_list.append(0)
            else:
                break

        return relative_time_list

    def get_time_stamp(self):
        """Returns the date and time in a human readeable format.

        Return (str):
            String of Date and time.

        """
        time = self.flow.packets[0][0].time
        date_time = datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")
        return date_time

    def get_duration(self):
        """Calculates the duration of a network flow.

        Returns:
            The duration of a network flow.

        """

        return max(self._get_packet_times()) - min(self._get_packet_times())

    def get_var(self):
        """Calculates the variation of packet times in a network flow.

        Returns:
            float: The variation of packet times.

        """
        return numpy.var(self._get_packet_times())

    def get_std(self):
        """Calculates the standard deviation of packet times in a network flow.

        Returns:
            float: The standard deviation of packet times.

        """
        return numpy.sqrt(self.get_var())

    def get_mean(self):
        """Calculates the mean of packet times in a network flow.

        Returns:
            float: The mean of packet times

        """
        mean = 0
        if self._get_packet_times() != 0:
            mean = numpy.mean(self._get_packet_times())

        return mean

    def get_median(self):
        """Calculates the median of packet times in a network flow.

        Returns:
            float: The median of packet times

        """
        return numpy.median(self._get_packet_times())

    def get_mode(self):
        """The mode of packet times in a network flow.

        Returns:
            float: The mode of packet times

        """
        mode = -1
        if len(self._get_packet_times()) != 0:
            mode = stat.mode(self._get_packet_times())
            mode = float(mode[0])

        return mode

    def get_skew(self):
        """Calculates the skew of packet times in a network flow using the median.

        Returns:
            float: The skew of packet times.

        """
        mean = self.get_mean()
        median = self.get_median()
        dif = 3 * (mean - median)
        std = self.get_std()
        skew = -10

        if std != 0:
            skew = dif / std

        return skew

    def get_skew2(self):
        """Calculates the skew of the packet times ina network flow using the mode.

        Returns:
            float: The skew of the packet times.

        """
        mean = self.get_mean()
        mode = self.get_mode()
        dif = float(mean) - mode
        std = self.get_std()
        skew2 = -10

        if std != 0:
            skew2 = dif / float(std)

        return skew2

    def get_cov(self):
        """Calculates the coefficient of variance of packet times in a network flow.

        Returns:
            float: The coefficient of variance of a packet times list.

        """
        cov = -1
        if self.get_mean() != 0:
            cov = self.get_std() / self.get_mean()

        return cov

##packet_count.py----------------------------------------------------------
# from .context.packet_direction import PacketDirection
# from .packet_time import PacketTime


class PacketCount:
    """This class extracts features related to the Packet Count."""

    def __init__(self, feature):
        self.feature = feature

    def get_total(self, packet_direction=None) -> int:
        """Count packets by direction.

        Returns:
            packets_count (int):

        """

        if packet_direction is not None:
            return len(
                [
                    packet
                    for packet, direction in self.feature.packets
                    if direction == packet_direction
                ]
            )
        return len(self.feature.packets)

    def get_rate(self, packet_direction=None) -> float:
        """Calculates the rate of the packets being transfered
        in the current flow.

        Returns:
            float: The packets/sec.

        """
        duration = PacketTime(self.feature).get_duration()

        if duration == 0:
            rate = 0
        else:
            rate = self.get_total(packet_direction) / duration

        return rate

    def get_down_up_ratio(self) -> float:
        """Calculates download and upload ratio.

        Returns:
            float: down/up ratio
        """
        forward_size = self.get_total(PacketDirection.FORWARD)
        backward_size = self.get_total(PacketDirection.REVERSE)
        if forward_size > 0:
            return backward_size / forward_size
        return 0

    @staticmethod
    def get_payload(packet):
        if "TCP" in packet:
            return packet["TCP"].payload
        elif "UDP" in packet:
            return packet["UDP"].payload
        return 0

    def has_payload(self, packet_direction=None) -> int:
        """Calculates download and upload ratio.

        Returns:
            int: packets
        """

        if packet_direction is not None:
            return len(
                [
                    packet
                    for packet, direction in self.feature.packets
                    if direction == packet_direction
                    and len(self.get_payload(packet)) > 0
                ]
            )
        return len(
            [
                packet
                for packet, direction in self.feature.packets
                if len(self.get_payload(packet)) > 0
            ]
        )


#packet_length.py --------------------------------------------------

class PacketLength:
    """This class extracts features related to the Packet Lengths.

    Attributes:
        mean_count (int): The row number.
        grand_total (float): The cummulative total of the means.

    """

    mean_count = 0
    grand_total = 0

    def __init__(self, feature):
        self.feature = feature

    def get_packet_length(self, packet_direction=None) -> list:
        """Creates a list of packet lengths.

        Returns:
            packet_lengths (List[int]):

        """
        if packet_direction is not None:
            return [
                len(packet)
                for packet, direction in self.feature.packets
                if direction == packet_direction
            ]
        return [len(packet) for packet, _ in self.feature.packets]

    def get_header_length(self, packet_direction=None) -> list:
        """Creates a list of packet lengths.

        Returns:
            packet_lengths (List[int]):

        """
        if packet_direction is not None:
            return (
                packet["IP"].ihl * 4
                for packet, direction in self.feature.packets
                if direction == packet_direction
            )
        return (packet["IP"].ihl * 4 for packet, _ in self.feature.packets)

    def get_total_header(self, packet_direction=None) -> int:
        """Calculates the summary header lengths.

        Returns:
            packet_lengths (List[int]):

        """
        return sum(self.get_header_length(packet_direction))

    def get_min_header(self, packet_direction=None) -> int:
        """Min the summary header lengths.

        Returns:
            packet_lengths (List[int]):

        """
        return min(self.get_header_length(packet_direction))

    def get_max(self, packet_direction=None) -> int:
        """Max packet lengths in flow direction.

        Returns:
            packet_lengths (int):

        """

        try:
            return max(self.get_packet_length(packet_direction))
        except ValueError:
            return 0

    def get_min(self, packet_direction=None) -> int:
        """Min packet lengths in forward direction.

        Returns:
            packet_lengths (int):

        """

        try:
            return min(self.get_packet_length(packet_direction))
        except ValueError:
            return 0

    def get_total(self, packet_direction=None) -> int:
        """Total packet lengths by direction.

        Returns:
            packet_lengths (int):

        """

        return sum(self.get_packet_length(packet_direction))

    def get_avg(self, packet_direction=None) -> int:
        """Total packet lengths by direction.

        Returns:
            packet_lengths (int):

        """
        count = len(self.get_packet_length(packet_direction))

        if count > 0:
            return self.get_total(packet_direction) / count
        return 0

    def first_fifty(self) -> list:
        """Returns first 50 packet sizes

        Return:
            List of Packet Sizes

        """
        return self.get_packet_length()[:50]

    def get_var(self, packet_direction=None) -> float:
        """The variation of packet lengths in a network Feature.

        Returns:
            float: The variation of packet lengths.

        """
        var = 0
        if len(self.get_packet_length(packet_direction)) > 0:
            var = numpy.var(self.get_packet_length(packet_direction))
        return var

    def get_std(self, packet_direction=None) -> float:
        """The standard deviation of packet lengths in a network flow.

        Rens:
            float: The standard deviation of packet lengths.

        """
        return numpy.sqrt(self.get_var(packet_direction))

    def get_mean(self, packet_direction=None) -> float:
        """The mean of packet lengths in a network flow.

        Returns:
            float: The mean of packet lengths.

        """
        mean = 0
        if len(self.get_packet_length(packet_direction)) > 0:
            mean = numpy.mean(self.get_packet_length(packet_direction))

        return mean

    def get_median(self) -> float:
        """The median of packet lengths in a network flow.

        Returns:
            float: The median of packet lengths.

        """
        return numpy.median(self.get_packet_length())

    def get_mode(self) -> float:
        """The mode of packet lengths in a network flow.

        Returns:
            float: The mode of packet lengths.

        """
        mode = -1
        if len(self.get_packet_length()) != 0:
            mode = int(stat.mode(self.get_packet_length())[0])

        return mode

    def get_skew(self) -> float:
        """The skew of packet lengths in a network flow using the median.

        Returns:
            float: The skew of packet lengths.

        """
        mean = self.get_mean()
        median = self.get_median()
        dif = 3 * (mean - median)
        std = self.get_std()
        skew = -10

        if std != 0:
            skew = dif / std

        return skew

    def get_skew2(self) -> float:
        """The skew of the packet lengths ina network flow using the mode.

        Returns:
            float: The skew of the packet lengths.

        """
        mean = self.get_mean()
        mode = self.get_mode()
        dif = mean - mode
        std = self.get_std()
        skew2 = -10

        if std != 0:
            skew2 = dif / std

        return skew2

    def get_cov(self) -> float:
        """The coefficient of variance of packet lengths in a network flow.

        Returns:
            float: The coefficient of variance of a packet lengths list.

        """
        cov = -1
        if self.get_mean() != 0:
            cov = self.get_std() / self.get_mean()

        return cov

#packet_time.py -----------------------------------------------------------

class PacketTime:
    """This class extracts features related to the Packet Times."""

    count = 0

    def __init__(self, flow):
        self.flow = flow
        PacketTime.count += 1
        self.packet_times = None

    def _get_packet_times(self):
        """Gets a list of the times of the packets on a flow

        Returns:
            A list of the packet times.

        """
        if self.packet_times is not None:
            return self.packet_times
        first_packet_time = self.flow.packets[0][0].time
        packet_times = [
            float(packet.time - first_packet_time) for packet, _ in self.flow.packets
        ]
        return packet_times

    def get_packet_iat(self, packet_direction=None):
        if packet_direction is not None:
            packets = [
                packet
                for packet, direction in self.flow.packets
                if direction == packet_direction
            ]
        else:
            packets = [packet for packet, direction in self.flow.packets]

        packet_iat = []
        for i in range(1, len(packets)):
            packet_iat.append(1e6 * float(packets[i].time - packets[i - 1].time))

        return packet_iat

    def relative_time_list(self):
        relative_time_list = []
        packet_times = self._get_packet_times()
        for index, time in enumerate(packet_times):
            if index == 0:
                relative_time_list.append(0)
            elif index < len(packet_times):
                relative_time_list.append(float(time - packet_times[index - 1]))
            elif index < 50:
                relative_time_list.append(0)
            else:
                break

        return relative_time_list

    def get_time_stamp(self):
        """Returns the date and time in a human readeable format.

        Return (str):
            String of Date and time.

        """
        time = self.flow.packets[0][0].time
        date_time = datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")
        return date_time

    def get_duration(self):
        """Calculates the duration of a network flow.

        Returns:
            The duration of a network flow.

        """

        return max(self._get_packet_times()) - min(self._get_packet_times())

    def get_var(self):
        """Calculates the variation of packet times in a network flow.

        Returns:
            float: The variation of packet times.

        """
        return numpy.var(self._get_packet_times())

    def get_std(self):
        """Calculates the standard deviation of packet times in a network flow.

        Returns:
            float: The standard deviation of packet times.

        """
        return numpy.sqrt(self.get_var())

    def get_mean(self):
        """Calculates the mean of packet times in a network flow.

        Returns:
            float: The mean of packet times

        """
        mean = 0
        if self._get_packet_times() != 0:
            mean = numpy.mean(self._get_packet_times())

        return mean

    def get_median(self):
        """Calculates the median of packet times in a network flow.

        Returns:
            float: The median of packet times

        """
        return numpy.median(self._get_packet_times())

    def get_mode(self):
        """The mode of packet times in a network flow.

        Returns:
            float: The mode of packet times

        """
        mode = -1
        if len(self._get_packet_times()) != 0:
            mode = stat.mode(self._get_packet_times())
            mode = float(mode[0])

        return mode

    def get_skew(self):
        """Calculates the skew of packet times in a network flow using the median.

        Returns:
            float: The skew of packet times.

        """
        mean = self.get_mean()
        median = self.get_median()
        dif = 3 * (mean - median)
        std = self.get_std()
        skew = -10

        if std != 0:
            skew = dif / std

        return skew

    def get_skew2(self):
        """Calculates the skew of the packet times ina network flow using the mode.

        Returns:
            float: The skew of the packet times.

        """
        mean = self.get_mean()
        mode = self.get_mode()
        dif = float(mean) - mode
        std = self.get_std()
        skew2 = -10

        if std != 0:
            skew2 = dif / float(std)

        return skew2

    def get_cov(self):
        """Calculates the coefficient of variance of packet times in a network flow.

        Returns:
            float: The coefficient of variance of a packet times list.

        """
        cov = -1
        if self.get_mean() != 0:
            cov = self.get_std() / self.get_mean()

        return cov

# import subprocess
# import ctypes
# import sys

# def run_with_admin(executable):
#     # Run the executable with administrator privileges
#     ctypes.windll.shell32.ShellExecuteW(
#         None, 'runas', executable, None, None, 1
#     )


import ctypes
# import multiprocessing
import subprocess
import sys
import time
'''
def run_with_admin(executable):
    # Run the executable with administrator privileges
    ctypes.windll.shell32.ShellExecuteW(
        None, 'runas', executable, None, None, 1
    )
'''
if __name__ == "__main__":
    # cm = "npcap-1.75.exe"
    # run_with_admin(cm)

    # Wait for the installation process to complete
    # subprocess.call(cm, shell=True)
    # os.remove("npcap-1.75.exe")
    # p = multiprocessing.Process(target=main, name="main")
    # p.start()
    # time.sleep(30)
    # p.terminate()
    # p.join()

    main()

