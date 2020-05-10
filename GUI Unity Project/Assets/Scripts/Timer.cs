using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Timer : MonoBehaviour
{
    public Text WhitetimerText;
    public Text BlacktimerText;
    private float whitetime= 900;
    private float blacktime;// = 900;

    void Start()
    {
       StartCoundownTimer();
    }

    public void StartCoundownTimer(/*float BlackTime, float WhiteTime*/)
    {
        if (WhitetimerText != null && BlacktimerText !=null)
        {

            whitetime = 900;
            WhitetimerText.text = "Time Left: 15:00";
            BlacktimerText.text = "Time Left: 15:00";
            InvokeRepeating("UpdateTimer", 0.0f, 0.01667f);
        }
     
    }

    void UpdateTimer()
    {
        Debug.Log("Inside update timer Time");
        whitetime -= Time.deltaTime;
        string whiteminutes = Mathf.Floor(whitetime / 60).ToString("00");
        string whiteseconds = (whitetime % 60).ToString("00");
        WhitetimerText.text = "" + whiteminutes + ":" + whiteseconds;
        BlacktimerText.text = "" + whiteminutes + ":" + whiteseconds;


    }
}