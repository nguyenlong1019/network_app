import ns.applications
import ns.core
import ns.internet
import ns.mobility
import ns.network
import ns.point_to_point
import ns.wifi
import ns.aodv

def main():
    ns.core.LogComponentEnable("UdpEchoClientApplication", ns.core.LOG_LEVEL_INFO)
    ns.core.LogComponentEnable("UdpEchoServerApplication", ns.core.LOG_LEVEL_INFO)

    # Tạo 10 nút mạng
    nodes = ns.network.NodeContainer()
    nodes.Create(10)

    # Cài đặt WiFi cho các nút
    wifi = ns.wifi.WifiHelper.Default()
    wifiMac = ns.wifi.NqosWifiMacHelper.Default()
    wifiChannel = ns.wifi.YansWifiChannelHelper.Default()
    wifiPhy = ns.wifi.YansWifiPhyHelper.Default()
    wifiPhy.SetChannel(wifiChannel.Create())

    wifi.SetRemoteStationManager("ns3::AarfWifiManager")
    devices = wifi.Install(wifiPhy, wifiMac, nodes)

    # Đặt mô hình di chuyển
    mobility = ns.mobility.MobilityHelper()
    positionAlloc = ns.mobility.ListPositionAllocator()
    for i in range(10):
        positionAlloc.Add(ns.core.Vector3D(i * 10, 0, 0))
    mobility.SetPositionAllocator(positionAlloc)
    mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel")
    mobility.Install(nodes)

    # Cài đặt giao thức AODV
    aodv = ns.aodv.AodvHelper()
    internetStack = ns.internet.InternetStackHelper()
    internetStack.SetRoutingHelper(aodv)
    internetStack.Install(nodes)

    # Gán địa chỉ IP
    address = ns.internet.Ipv4AddressHelper()
    address.SetBase(ns.network.Ipv4Address("10.1.1.0"), ns.network.Ipv4Mask("255.255.255.0"))
    interfaces = address.Assign(devices)

    # Tạo và cài đặt ứng dụng server
    echoServer = ns.applications.UdpEchoServerHelper(9)
    serverApp = echoServer.Install(nodes.Get(1))
    serverApp.Start(ns.core.Seconds(1.0))
    serverApp.Stop(ns.core.Seconds(10.0))

    # Tạo và cài đặt ứng dụng client
    echoClient = ns.applications.UdpEchoClientHelper(interfaces.GetAddress(1), 9)
    echoClient.SetAttribute("MaxPackets", ns.core.UintegerValue(1))
    echoClient.SetAttribute("Interval", ns.core.TimeValue(ns.core.Seconds(1.0)))
    echoClient.SetAttribute("PacketSize", ns.core.UintegerValue(1024))

    clientApp = echoClient.Install(nodes.Get(0))
    clientApp.Start(ns.core.Seconds(2.0))
    clientApp.Stop(ns.core.Seconds(10.0))

    # Chạy mô phỏng
    ns.core.Simulator.Run()
    ns.core.Simulator.Destroy()

if __name__ == "__main__":
    main()
