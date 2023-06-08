#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class final_topo(Topo):
  def build(self):
    # Examples!
    # Create a host with a default route of the ethernet interface. You'll need to set the
    # default gateway like this for every host you make on this assignment to make sure all 
    # packets are sent out that port. Make sure to change the h# in the defaultRoute area
    # and the MAC address when you add more hosts!
    # h1 = self.addHost('h1',mac='00:00:00:00:00:01',ip='1.1.1.1/24', defaultRoute="h1-eth0")
    # h2 = self.addHost('h2',mac='00:00:00:00:00:02',ip='2.2.2.2/24', defaultRoute="h2-eth0")

    # Create a switch. No changes here from Lab 1.
    # s1 = self.addSwitch('s1')

    # Connect Port 8 on the Switch to Port 0 on Host 1 and Port 9 on the Switch to Port 0 on 
    # Host 2. This is representing the physical port on the switch or host that you are 
    # connecting to.
    #
    # IMPORTANT NOTES: 
    # - On a single device, you can only use each port once! So, on s1, only 1 device can be
    #   plugged in to port 1, only one device can be plugged in to port 2, etc.
    # - On the "host" side of connections, you must make sure to always match the port you 
    #   set as the default route when you created the device above. Usually, this means you 
    #   should plug in to port 0 (since you set the default route to h#-eth0).
    #
    # self.addLink(s1,h1, port1=8, port2=0)
    # self.addLink(s1,h2, port1=9, port2=0)

    # Switches and links
    dataCenterSwitch = self.addSwitch('s1')
    coreSwitch = self.addSwitch('s2')
    self.addLink(dataCenterSwitch, coreSwitch, port1=1, port2=1)
    floor1Switch1 = self.addSwitch('s3')
    self.addLink(floor1Switch1, coreSwitch, port1=1, port2=2)
    floor1Switch2 = self.addSwitch('s4')
    self.addLink(floor1Switch2, coreSwitch, port1=1, port2=3)
    floor2Switch1 = self.addSwitch('s5')
    self.addLink(floor2Switch1, coreSwitch, port1=1, port2=4)
    floor2Switch2 = self.addSwitch('s6')
    self.addLink(floor2Switch2, coreSwitch, port1=1, port2=5)
    # Hosts and links
    server = self.addHost('server', mac='00:00:00:00:00:90', ip='10.3.9.90/24', defaultRoute = 'server-eth0')
    self.addLink(server, dataCenterSwitch, port1=0, port2=2)
    host10 = self.addHost('h10', mac='00:00:00:00:00:10', ip='10.1.1.10/24', defaultRoute = 'h10-eth0')
    host20 = self.addHost('h20', mac='00:00:00:00:00:20', ip='10.1.2.20/24', defaultRoute = 'h20-eth0')
    self.addLink(host10, floor1Switch1, port1=0, port2=2)
    self.addLink(host20, floor1Switch1, port1=0, port2=3)
    host30 = self.addHost('h30', mac='00:00:00:00:00:30', ip='10.1.3.30/24', defaultRoute = 'h30-eth0')
    host40 = self.addHost('h40', mac='00:00:00:00:00:40', ip='10.1.4.40/24', defaultRoute = 'h40-eth0')
    self.addLink(host30, floor1Switch2, port1=0, port2=2)
    self.addLink(host40, floor1Switch2, port1=0, port2=3)
    host50 = self.addHost('h50', mac='00:00:00:00:00:50', ip='10.2.5.50/24', defaultRoute = 'h50-eth0')
    host60 = self.addHost('h60', mac='00:00:00:00:00:60', ip='10.2.6.60/24', defaultRoute = 'h60-eth0')
    self.addLink(host50, floor2Switch1, port1=0, port2=2)
    self.addLink(host60, floor2Switch1, port1=0, port2=3)
    host70 = self.addHost('h70', mac='00:00:00:00:00:70', ip='10.2.7.70/24', defaultRoute = 'h70-eth0')
    host80 = self.addHost('h80', mac='00:00:00:00:00:80', ip='10.2.8.80/24', defaultRoute = 'h80-eth0')
    self.addLink(host70, floor2Switch2, port1=0, port2=2)
    self.addLink(host80, floor2Switch2, port1=0, port2=3)
    hostTrusted = self.addHost('trusted', mac='12:34:56:78:90:AB', ip='108.24.31.112/24', defaultRoute = 'trusted-eth0')
    hostHacker = self.addHost('hacker', mac='BA:09:87:65:43:21', ip='106.44.82.103/24', defaultRoute = 'hacker-eth0')
    self.addLink(hostTrusted, coreSwitch, port1=0, port2=6)
    self.addLink(hostHacker, coreSwitch, port1=0, port2=7)

def configure():
  topo = final_topo()
  net = Mininet(topo=topo, controller=RemoteController)
  net.start()

  CLI(net)
  
  net.stop()


if __name__ == '__main__':
  configure()
