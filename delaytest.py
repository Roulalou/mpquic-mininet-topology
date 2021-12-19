#!/usr/bin/env python

"""
Simple example of setting network and CPU parameters
NOTE: link params limit BW, add latency, and loss.
There is a high chance that pings WILL fail and that
iperf will hang indefinitely if the TCP handshake fails
to complete.
"""

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

        # linkopts = dict(bw=10, delay='50ms', loss=10, use_htb=True)
        # example : self.addLink( s1, s2, **linkopts)

        # /* first path */
        s1 = self.addSwitch('s1')
        self.addLink(h1, s1, loss=25)
        self.addLink(h2, s1)

        # /* second path */
        s2 = self.addSwitch('s2')
        self.addLink(h1, s2)
        self.addLink(h2, s2)



def perfTest():
    "Create network and run simple performance test"
    topo = StaticTopo()
    net = Mininet( topo=topo, link=TCLink)
                    # host=CPULimitedHost, autoStaticArp=True

    net.start()
    print("Net start")

    h1 = net.get('h1')
    h2 = net.get('h2')

    for i in range(0, 2):
        #h1.cmd('ifconfig h1-eth' + str(i) + ' 1' + str(i) + '.0.0.1')
        h2.cmd('ifconfig h2-eth' + str(i) + ' 1' + str(i) + '.0.0.2')

    # net.pingAll()

    print( "Host", h1.name, "has IP address", h1.IP(), "and MAC address", h1.MAC() )
    print( "Host", h2.name, "has IP address", h2.IP(), "and MAC address", h2.MAC() )

    result = h1.cmd("./picoquicdemo -p 6653 -P plugins/multipath/multipath_rtt_cond.plugin &")
    print(result)

  
    rez = h2.cmd("./picoquicdemo -4 -G 20000 -P plugins/multipath/multipath_rtt_cond.plugin 10.0.0.1 6653")
    print(rez)

    net.stop()
    print("Net Stop")
    


if __name__ == '__main__':
    setLogLevel( 'info' )
    # Prevent test_simpleperf from failing due to packet loss
    perfTest()