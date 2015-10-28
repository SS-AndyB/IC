using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;

namespace LightwaveRFCommand
{
    class Program
    {
        static UdpClient udpClient;

        static int cmdSequence = 1;

        static void Main(string[] args)
        {
            var receiveThread = new Thread(new ThreadStart(UdpListener));
            receiveThread.Start();

            CreateUdpClient();

            var cmd = "";


            var dimmerMap = new[] {
                                new { value = "0", level = 0 },
                                new { value = "1", level = 3 },
                                new { value = "2", level = 7 },
                                new { value = "3", level = 10 },
                                new { value = "4", level = 14 },
                                new { value = "5", level = 18 },
                                new { value = "6", level = 21 },
                                new { value = "7", level = 25 },
                                new { value = "8", level = 28 },
                                new { value = "9", level = 32 }};

            if (args.Contains("register"))
            {
                cmd = "000,!F*p\n";
                SendCmd(cmd);
                Thread.Sleep(60000);
            }

            var cmdLampOff = "001,!R1D1F0\n";
            SendCmd(cmdLampOff);

            var r = new Regex("[0-9]{1}");

            var s = Console.ReadLine();
            if (s.Length > 1)
            {
                s = s.Substring(0, 1);
            }

            while (r.IsMatch(s))
            {
                if (s == "0")
                    cmd = cmdLampOff;
                else
                {
                    var level = dimmerMap.Single(dm => dm.value == s).level;

                    cmd = $"001,!R1D1FdP{level}\n";                          
                }
                SendCmd(cmd);
                s = Console.ReadLine();

            }


        }

        static void CreateUdpClient()
        {
            Console.WriteLine("Creating Udp Sender");

            var lightwaveHubAddress = IPAddress.Parse("10.33.26.125");
            var ep = new IPEndPoint(lightwaveHubAddress, 9760);
            udpClient = new UdpClient();
            udpClient.Connect(ep);
        }

        static void SendCmd(string cmd)
        {
            cmdSequence++;
            Console.WriteLine($"Sending Command {cmd}");
            var cmdBytes = Encoding.ASCII.GetBytes(cmd);
            udpClient.Send(cmdBytes, cmdBytes.Length);

        }

        static void UdpListener()
        {
            Console.WriteLine("Listening for responses");

            var udpClient = new UdpClient(9761);
            var ipEndpoint = new IPEndPoint(IPAddress.Any, 0);

            bool running = true;

            while (running)
            {
                var bytesReceived = udpClient.Receive(ref ipEndpoint);
                var s = Encoding.ASCII.GetString(bytesReceived);
                Console.WriteLine(s);
            }


        }
    }
}
