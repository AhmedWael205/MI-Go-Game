using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class UIManager : MonoBehaviour
{
    public Text BlackScoreText;
    public Text WhiteScoreText;
    public Text WhiteMessage;
    public Text BlackMessage;
    //public Text WhitetimerText;
    //public Text BlacktimerText;
    //private float whitetime;// = 900;
    //private float blacktime;// = 900;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    public void updateScore(string[] Score)
    {
        
        BlackScoreText.text = ""+Score[1];
        WhiteScoreText.text = "" + Score[0];
    }
    public void updateMessage(int best,int mycolor, int [] bestcoord)
    {
        if (best == 1 && mycolor == 0)
        {
            WhiteMessage.text = "Congarts! You played the best possible move";
        }
        else if (best ==-1 && mycolor == 0)
        {
            if (bestcoord[0] == -1 && bestcoord[1] == -1)
            {
                WhiteMessage.text = "Opps! The Best move was pass";
            }
            else
            {
                WhiteMessage.text = "Opps! There was a better move";
            }
        }
        else if (best == 1 && mycolor == 1)
        {
            BlackMessage.text = "Congarts! You played the best possible move";
        }
        else if(best ==-1 && mycolor ==1)
        {
            if (bestcoord[0] == -1 && bestcoord[1] == -1)
            {
                BlackMessage.text = "Opps! The Best move was pass";
            }
            else
            {
                BlackMessage.text = "Opps! There was a better move";
            }
        }
        else if(best==0)
        {
            BlackMessage.text = " ";
            WhiteMessage.text = " ";
        }
        else
        {

        }
    }


    //public void StartCoundownTimer(float BlackTime, float WhiteTime)
    //{
    //    if (WhitetimerText != null && BlacktimerText !=null)
    //    {
    //        Debug.Log("Inside start timer Time");
    //        blacktime = BlackTime / 1000;
    //        whitetime = WhiteTime / 1000;
    //        string blackminutes = Mathf.Floor(blacktime / 60).ToString("00");
    //        string blackseconds = (blacktime % 60).ToString("00");
    //        BlacktimerText.text = "" + blackminutes + ":" + blackseconds;
    //        string whiteminutes = Mathf.Floor(whitetime / 60).ToString("00");
    //        string whiteseconds = (whitetime % 60).ToString("00");
    //        WhitetimerText.text = "" + whiteminutes + ":" + whiteseconds;
    //        //whitetime = 900;
    //        //WhitetimerText.text = "Time Left: 15:00";
    //        //BlacktimerText.text = "Time Left: 15:00";
    //        InvokeRepeating("UpdateTimer", 0.0f, 0.01667f);
    //    }
     
    //}

    //void UpdateTimer()
    //{
    //    Debug.Log("Inside update timer Time");
    //    //whitetime -= Time.deltaTime;
    //    //string whiteminutes = Mathf.Floor(whitetime / 60).ToString("00");
    //    //string whiteseconds = (whitetime % 60).ToString("00");
    //    blacktime -= Time.deltaTime;
    //    whitetime -= Time.deltaTime; ;
    //    string blackminutes = Mathf.Floor(blacktime / 60).ToString("00");
    //    string blackseconds = (blacktime % 60).ToString("00");
    //    BlacktimerText.text = "" + blackminutes + ":" + blackseconds;
    //    string whiteminutes = Mathf.Floor(whitetime / 60).ToString("00");
    //    string whiteseconds = (whitetime % 60).ToString("00");
    //    WhitetimerText.text = "" + whiteminutes + ":" + whiteseconds;
    //    BlacktimerText.text = "" + whiteminutes + ":" + whiteseconds;


    //}
}
