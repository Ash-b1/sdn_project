from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet import ethernet, arp
from pox.lib.addresses import IPAddr, EthAddr

log = core.getLogger()

class ARPHandler(object):
    def __init__(self):
        core.openflow.addListeners(self)
        self.ip_to_mac = {}

    def _handle_ConnectionUp(self, event):
        log.info("Switch %s connected", event.dpid)

    def _handle_PacketIn(self, event):
        packet = event.parsed

        if not packet:
            return

        # ---- HANDLE ARP ----
        if packet.type == ethernet.ARP_TYPE:
            arp_packet = packet.payload

            # Learn mapping
            self.ip_to_mac[arp_packet.protosrc] = arp_packet.hwsrc

            if arp_packet.opcode == arp.REQUEST:
                log.info("ARP Request: Who has %s? Tell %s",
                         arp_packet.protodst, arp_packet.protosrc)

                # If we know destination, reply directly
                if arp_packet.protodst in self.ip_to_mac:
                    reply = arp()
                    reply.opcode = arp.REPLY
                    reply.hwsrc = self.ip_to_mac[arp_packet.protodst]
                    reply.hwdst = arp_packet.hwsrc
                    reply.protosrc = arp_packet.protodst
                    reply.protodst = arp_packet.protosrc

                    eth = ethernet()
                    eth.type = ethernet.ARP_TYPE
                    eth.src = reply.hwsrc
                    eth.dst = reply.hwdst
                    eth.payload = reply

                    msg = of.ofp_packet_out()
                    msg.data = eth.pack()
                    msg.actions.append(of.ofp_action_output(port=event.port))
                    event.connection.send(msg)

                    log.info("ARP Reply sent: %s is at %s",
                             reply.protosrc, reply.hwsrc)
                    return

                else:
                    # Flood if unknown
                    msg = of.ofp_packet_out(data=event.ofp)
                    msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
                    event.connection.send(msg)
                    return

        # ---- HANDLE ALL OTHER TRAFFIC (ICMP, etc.) ----
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet)
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(msg)


def launch():
    core.registerNew(ARPHandler)