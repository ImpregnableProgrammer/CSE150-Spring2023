# Final Project - IP Router Implementation using OpenFlow
## Introduction
For this project, we build upon the work begun in lab 3 to implement an IPV4 router with a firewall that blocks traffic from an untrusted host but allows it from a trusted one, along with regulating traffic among the remaining hosts which are all separated by their own switches. There is a central switch that connects all hosts and a server along with their switches. The nine hosts in all have their traffic regulated by flow table entries installed on the switches that packets are matched against for them to reach their destinations. The flow table entries are installed on the switches by the network controller as matching packets are received.

## Files
* **README.md** - This is the explanatory file you are reading right now :)
* **final_skel.py** - This script implements the network topology using the Pox controller library in a Python environment. Invoke it by running `sudo python3 final_skel.py` on a system with [Mininet](http://mininet.org/download/) installed, which then shows the `Mininet` command line where commands, such as `pingall`, can be run to examine the network.
* **final_controller.py** - This file implements the network controller that manages packets flowing through the network switches by following the OpenFlow protocol. Invoke it my placing it in the `~/pox/pox/misc` directory and then running `sudo ~/pox/pox.py finalcontroller_skel.py` at the _same time_ as when the topology Mininet script `final_skel.py` is running on a system with Mininet installed.
* **project.pdf** - This PDF explains the router implementation and provides screenshots of various command outputs in Mininet.

## Resources used
* Pox documentation: https://noxrepo.github.io/pox-doc/html/