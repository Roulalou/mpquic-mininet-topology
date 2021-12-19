#!/usr/bin/env python

from sys import argv

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class StaticTopo(Topo):
    def build(self):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        # to change link parameters, you can add argument to addLink or use a variable like linkopts
        # linkopts = dict(bw=10, delay='50ms', loss=10, use_htb=True)
        # example : self.addLink( s1, s2, **linkopts)
        # or : self.addLink( s1, s2, delay='50ms')

        # /* first path */
        s1 = self.addSwitch('s1')
        self.addLink(h1, s1)
        self.addLink(h2, s1)

        # /* second path */
        s2 = self.addSwitch('s2')
        self.addLink(h1, s2)
        self.addLink(h2, s2)



def perfTest():
    "Create network and run simple performance test"
    topo = StaticTopo()
    net = Mininet( topo=topo, link=TCLink)

    net.start()
    print("Net start")

    h1 = net.get('h1')
    h2 = net.get('h2')

    # set different IP for the 2 paths
    for i in range(0, 2):
        h2.cmd('ifconfig h2-eth' + str(i) + ' 1' + str(i) + '.0.0.2')

    # we use pingAll to detect if there is a problem in the network
    net.pingAll()

    # print Host information
    print( "Host", h1.name, "has IP address", h1.IP(), "and MAC address", h1.MAC() )
    print( "Host", h2.name, "has IP address", h2.IP(), "and MAC address", h2.MAC() )

    # you can use ./picoquicdemo -h to see all possible parameters
    # replace 'rtt' by 'rr' in h1 and h2 to test with RR-COND
    result = h1.cmd("./picoquicdemo -p 6653 -P plugins/multipath/multipath_rtt_cond.plugin &")
    print(result)
  
    rez = h2.cmd("./picoquicdemo -4 -G 20000 -P plugins/multipath/multipath_rtt_cond.plugin 10.0.0.1 6653")
    print(rez)

    net.stop()
    print("Net Stop")
    


if __name__ == '__main__':
    setLogLevel( 'info' )
    perfTest()