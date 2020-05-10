using AsyncIO;
using NetMQ;
using NetMQ.Sockets;
using UnityEngine;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System;
using System.IO;
using System.Net.Sockets;
using System.Security;
using System.Net;
using System.Collections;

public class Communication : RunAbleThread
{

    public int[] outputt = new int[730];
    public string message = "TRIAL";
    public ResponseSocket server;
    public RequestSocket client;
    public string Mode="-2";
    public string Xindex = "-2";
    public string Yindex = "-2";
    public string Pass = "-2";
    public string Resign = "-2";
    public String HumanColor = "-2";
    public Int64 MessageID;
    protected override void Run()
    {
        ForceDotNet.Force(); // this line is needed to prevent unity freeze after one use, not sure why yet

        using ( server = new ResponseSocket()) // check if its response or request ?
        {
            server.Bind("tcp://*:1234"); //SEND

            using ( client = new RequestSocket())
            {
                client.Connect("tcp://localhost:2222"); // RECIEVE


               // for (int i = 0; i < 2 && Running; i++)
                while(Running)
                {

                    // TO BE ABLE TO SEND USING SERVER SOCKET:
                    string DummyServerReceive = server.ReceiveFrameString();
                    //Debug.Log("MY DUMMY SERVER REC: " + DummyServerReceive);
                    //SENDING TO SERVER :  //SEND A VARIABLE BOOLEAN HERE
                    server.SendFrame(Mode+","+Yindex+","+Xindex+"," + Resign+ ","+ Pass+","+HumanColor);
                    //Pass = "-1";
                    //Resign = "-1";
                    //Debug.Log("SERVER IS DONE ");

                    // DUMMY SEND OF CLIENT TO RECEIVE
                    client.SendFrame("HELLOOOOOOO");

                    while (Running)
                    {
                        message = client.ReceiveFrameString(); // this returns true if it's successful

                        //Debug.Log("MESSAGE IS :" + this.message);

                        break;
                    }

                   
                }

                client.Disconnect("tcp://localhost:2222");
                client.Close();
                client.Dispose();

            }
            server.Disconnect("tcp://*:1234");
            server.Close();
            server.Dispose();
        }
        
        NetMQConfig.Cleanup();
    }

}



        