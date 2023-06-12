# Final Skeleton
#
# Hints/Reminders from Lab 3:
#
# To check the source and destination of an IP packet, you can use
# the header information... For example:
#
# ip_header = packet.find('ipv4')
#
# if ip_header.srcip == "1.1.1.1":
#   print "Packet is from 1.1.1.1"
#
# Important Note: the "is" comparison DOES NOT work for IP address
# comparisons in this way. You must use ==.
# 
# To send an OpenFlow Message telling a switch to send packets out a
# port, do the following, replacing <PORT> with the port number the 
# switch should send the packets out:
#
#    msg = of.ofp_flow_mod()
#    msg.match = of.ofp_match.from_packet(packet)
#    msg.idle_timeout = 30
#    msg.hard_timeout = 30
#
#    msg.actions.append(of.ofp_action_output(port = <PORT>))
#    msg.data = packet_in
#    self.connection.send(msg)
#
# To drop packets, simply omit the action.
#

# ISSUE: Exception: Error creating interface pair (s1-eth1,h1-eth0): RTNETLINK answers: File exists
# Solution: https://github.com/mininet/mininet/issues/804

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Final (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)       

  def do_final (self, packet, packet_in, port_on_switch, switch_id):
    # This is where you'll put your code. The following modifications have 
    # been made from Lab 3:
    #   - port_on_switch: represents the port that the packet was received on.
    #   - switch_id represents the id of the switch that received the packet.
    #      (for example, s1 would have switch_id == 1, s2 would have switch_id == 2, etc...)
    # You should use these to determine where a packet came from. To figure out where a packet 
    # is going, you can use the IP header information.
    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet_in)

    floor1Switch1 = ['10.1.1.10', '10.1.2.20']
    floor1Switch2 = ['10.1.3.30', '10.1.4.40']
    floor1 = floor1Switch1 + floor1Switch2
    floor2Switch1 = ['10.2.5.50', '10.2.6.60']
    floor2Switch2 = ['10.2.7.70', '10.2.8.80']
    floor2 = floor2Switch1 + floor2Switch2
    hostUntrusted = ['106.44.82.103']
    hostTrusted = ['108.24.31.112']
    server = ['10.3.9.90']

    ip = packet.find('ipv4')
    if ip != None:
      destIP = ip.dstip
      icmp = packet.find('icmp') # ICMP is IP traffic (https://www.cloudflare.com/learning/ddos/glossary/internet-control-message-protocol-icmp/)
      if switch_id == 1: # Data center switch
        if port_on_switch == 1: # Traffic coming from core switch should reach the server
          msg.actions.append(of.ofp_action_output(port = 2))
        else: # Outgoing traffic should be sent to the core switch
          msg.actions.append(of.ofp_action_output(port = 1))
      elif switch_id == 2: # Core switch - process traffic from different locations according to rules
        # Untrusted host - block all ICMP traffic except to trusted host, and other IP traffic only to server
        # OR Trusted host - block all ICMP traffic to floor 2 and server, and other IP traffic only to server
        # OR floor 2 hosts - block all ICMP traffic to floor 1 hosts
        # OR floor 1 hosts - block all ICMP traffic to floor 2 hosts
        # OR server - allow all outgoing traffic
        # Allow all other traffic
        if (port_on_switch == 7 and ((icmp and destIP not in hostTrusted) or destIP in server)) \
        or (port_on_switch == 6 and ((icmp and destIP in floor2) or destIP in server)) \
        or (port_on_switch in [4, 5] and (icmp and destIP in floor1)) \
        or (port_on_switch in [2, 3] and (icmp and destIP in floor2)):
          msg.actions.append(of.ofp_action_output(port = of.OFPP_NONE))
        else: # Resolve allowed network traffic at core switch
          if destIP in server:
            msg.actions.append(of.ofp_action_output(port = 1))
          elif destIP in floor1Switch1:
            msg.actions.append(of.ofp_action_output(port = 2))
          elif destIP in floor1Switch2:
            msg.actions.append(of.ofp_action_output(port = 3))
          elif destIP in floor2Switch1:
            msg.actions.append(of.ofp_action_output(port = 4))
          elif destIP in floor2Switch2:
            msg.actions.append(of.ofp_action_output(port = 5))
          elif destIP in hostTrusted:
            msg.actions.append(of.ofp_action_output(port = 6))
          elif destIP in hostUntrusted:
            msg.actions.append(of.ofp_action_output(port = 7))
      # For floor traffic within the switch
      elif (switch_id == 3 and destIP == floor1Switch1[0]) \
        or (switch_id == 4 and destIP == floor1Switch2[0]) \
        or (switch_id == 5 and destIP == floor2Switch1[0]) \
        or (switch_id == 6 and destIP == floor2Switch2[0]):
        msg.actions.append(of.ofp_action_output(port = 2))
      elif (switch_id == 3 and destIP == floor1Switch1[1]) \
        or (switch_id == 4 and destIP == floor1Switch2[1]) \
        or (switch_id == 5 and destIP == floor2Switch1[1]) \
        or (switch_id == 6 and destIP == floor2Switch2[1]):
        msg.actions.append(of.ofp_action_output(port = 3))
      # For all other traffic across switches
      else:
        msg.actions.append(of.ofp_action_output(port = 1))
    else:
      msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
    self.connection.send(msg)

    # Send packet back to switch for processing by new flow table entry
    msg = of.ofp_packet_out(data = packet_in)
    msg.actions.append(of.ofp_action_output(port = of.OFPP_TABLE))
    self.connection.send(msg)

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_final(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Final(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
