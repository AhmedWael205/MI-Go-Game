 using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.EventSystems;
using UnityEngine.UI;
using System;
using UnityEngine.SceneManagement;


public class AIMode : MonoBehaviour
{
    // Start is called before the first frame update
    public MainMenu M;
    public GameObject Background;
    public GameObject ExitButton;
    public GameObject BacktoMenuButton;
    public GameObject MainBacktoMenuButon;
    public GameObject StonePrefab;
    public GameObject LoseScreen;
    public GameObject WinScreen;        // Reem 
    public GameObject BlackPlate;
    public GameObject WhitePlate;
    public GameObject Board;
    public GameObject BlackScore;
    public GameObject WhiteScore;
    public Sprite[] StoneSprites;
    public UIManager UI;
    public Button DisplayTerr;
    public GameObject[] PrefabArr = new GameObject[361] { null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null,
    null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null,
    null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null,
    null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null,
    null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null,
    null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null,
    null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null,
    null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null,
    null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null,
    null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null,
    null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null,
    null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null,
    null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null,
    null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null,
    null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null,
    null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null,
    null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null,
    null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null,
    null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null};
    int count = 0;
    public int clickCount = 0;
    private static Communication ComObject;
    public string ReceivedMessage = "";
    string[] Result;
    string Winner = "";
    float [] Xpositions=new float[361];
    float[] Ypositions = new float[361];
    
    private int[] LastMove = new int[2]; //{ 0, 1 };
    private string[] Score = new string[2]; //{ 0, 1 };
    public int[] KimoArr = new int[361];

    //RUBA:
    private int MyColor;
    bool BlackPlayed = false;
    private int[] Time = new int[2];
    private int MoveValidation =0 ;
    private int IsBetterMove =0;
    private int[] BetterMove = new int[2];
    
    //FOR CAPTURED STONES:
    private int CapturedMoveWhite = 3;
    private int LastCapturedMoveWhite = 0;
    private int LastCapturedIndexWhite = 0;
    private int CapturedMoveBlack = 3;
    private int LastCapturedMoveBlack = 0;
    private int LastCapturedIndexBlack = 0;
    private float[] XCapturePositionWhite = new float[] { -13.73f, -14.73f, -13.97f, -13.67f, -13.03f, -12.74f, -13.5f, -14.09f, -12.97f, -14.44f, -13.33f, -12.44f, -14.68f, -13.15f };
    private float[] YCapturePositionWhite = new float[] { -2.07f, -2.08f, -2.95f, -1.25f, -2.84f, -2.02f, -3.49f, -2.43f, -1.44f, -1.49f, -2.67f, -2.96f, -2.79f, -2.09f };
    private float[] XCapturePositionBlack = new float[] { 13.73f, 14.73f, 13.97f, 13.67f, 13.03f, 12.74f, 13.5f, 14.09f, 12.97f, 14.44f, 13.33f, 12.44f, 14.68f, 13.15f };
    private float[] YCapturePositionBlack = new float[] { -2.07f, -2.08f, -2.95f, -1.25f, -2.84f, -2.02f, -3.49f, -2.43f, -1.44f, -1.49f, -2.67f, -2.96f, -2.79f, -2.09f };


    // Update is called once per frame
    void Start()
    {
        M = GameObject.FindWithTag("MainMenu").GetComponent<MainMenu>();
        ComObject = M.ComO;
        ComObject.Mode = "-1";
        ReceivedMessage = ComObject.message;
        Debug.Log("Inside SpawnStones:  " + ReceivedMessage);
        

    }
    void Update()
    {
        //////////////////////////////// RECEIVING DATA ///////////////////////////

        RecievingData();

        ////////////////////////////////////////// DRAWING: /////////////////////////////////

        DrawingStones();

        DrawCaptured();
    }


    public void onClickBack()
    {
        Debug.Log("Back Button Clicked in AI");
        ComObject.Resign = "1";
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex -1);
        //SceneManager.GetSceneAt(0);

    }

    public void onClickExit()
    {
        Debug.Log("Exit Button Clicked");
        Application.Quit();

    }

    void RecievingData()
    {
        // RECEIVING BOARD ARRAY :

        ReceivedMessage = string.Copy(ComObject.message);
        Debug.Log("In update of SpwanStone:  " + ReceivedMessage);


        Result = ReceivedMessage.Split(',');
        Debug.Log("In update Result Length:  " + Result.Length);



        if (ReceivedMessage != "TRIAL")
        {
            //TO SET WINNER:
            Winner = Result[0];


            //RUBA:
            //TO SET BOARD ARRAY :
            for (int i = 1; i < Result.Length - 12; i++) //RUBA : CHANGE THE 12 ! 
            {
                KimoArr[i - 1] = Convert.ToInt32(Result[i]);
                Debug.Log("  Received --> " + i + " " + Result[i]);
            }

            //TO SET SCORE:
            Score[0] = Result[362];
            Score[1] = Result[363];



            //TO SET LAST MOVE:
            LastMove[0] = Convert.ToInt32(Result[364]);
            LastMove[1] = Convert.ToInt32(Result[365]);

            //RUBA + REEM :
            //RECIEVE TIME TO DISPLAY :
            Time[0] = Convert.ToInt32(Result[366]);  // BLACK
            Time[1] = Convert.ToInt32(Result[367]);  // WHITE
            Debug.Log("TIME: " + Time[0] + " " + Time[1]);

            MoveValidation = Convert.ToInt32(Result[368]);
            Debug.Log("VAL: " + MoveValidation);

            IsBetterMove = Convert.ToInt32(Result[369]);
            Debug.Log("IsBetterMove : " + IsBetterMove);


            BetterMove[0] = Convert.ToInt32(Result[370]);
            BetterMove[1] = Convert.ToInt32(Result[371]);
            Debug.Log("BetterMove X,Y : " + BetterMove[0] + BetterMove[1]);

            CapturedMoveBlack = Convert.ToInt32(Result[372]); // black
            CapturedMoveWhite = Convert.ToInt32(Result[373]); // white
            Debug.Log("Captured: " + CapturedMoveBlack + " " + CapturedMoveWhite);

            UI = GameObject.FindWithTag("UI").GetComponent<UIManager>();
            UI.updateScore(Score);

            if (Winner == "w")
            {
                WinScreen.SetActive(true);
                WhiteScore.SetActive(false);
                BlackScore.SetActive(false);
                WhitePlate.SetActive(false);
                BlackPlate.SetActive(false);
                Board.SetActive(false);
                LoseScreen.SetActive(false);
                Background.SetActive(true);
                ExitButton.SetActive(true);
                BacktoMenuButton.SetActive(true);
                MainBacktoMenuButon.SetActive(false);

            }
            else if (Winner == "l")
            {
                LoseScreen.SetActive(true);
                WhiteScore.SetActive(false);
                BlackScore.SetActive(false);
                WhitePlate.SetActive(false);
                BlackPlate.SetActive(false);
                Board.SetActive(false);
                WinScreen.SetActive(false);
                Background.SetActive(true);
                ExitButton.SetActive(true);
                BacktoMenuButton.SetActive(true);
                MainBacktoMenuButon.SetActive(false);
                


}
            else
            {
                LoseScreen.SetActive(false);
                WinScreen.SetActive(false);
            }

        }
    }

    void DrawingStones()
    {

        // TOP LEFT CORNER -> STARTING POSITION :
        float pos_x = -9.35f;
        float pos_y = 9.35f;

        // Trial and error values to move stones:
        float inc_X = 0.0175f;
        float inc_Y = 0.0175f;
        float inc_2 = 1.0f;
        float inc_3 = 1.0f;

        for (int i = 0; i < KimoArr.Length; i++)
        {
            if (i % 19 == 0 && i != 0)
            {
                pos_x = -9.35f;                     //--> TO RESET Y POSITION AFTER EVERY 19 MOVES
                pos_y = pos_y - 1.0f - inc_Y;

                inc_X = 0.0175f;
                inc_Y = inc_Y + (0.01f / inc_3);

                inc_3 += 1.0f;
                inc_2 = 1.0f;


            }
            //White Stone
            if (KimoArr[i] == 1)
            {
                Sprite StoneSprite;
                if (LastMove[0] * 19 + LastMove[1] == i)
                {
                    StoneSprite = StoneSprites[2];
                }
                else
                {
                    StoneSprite = StoneSprites[0];
                }
                string StoneName = StoneSprite.name;
                if (PrefabArr[i] == null)
                {

                    PrefabArr[i] = Instantiate(StonePrefab, new Vector2(pos_x, pos_y), Quaternion.identity);
                    Xpositions[i] = pos_x;
                    Ypositions[i] = pos_y;
                }
                PrefabArr[i].GetComponent<Stone>().StoneName = StoneName;
                PrefabArr[i].GetComponent<SpriteRenderer>().sprite = StoneSprite;
                PrefabArr[i].SetActive(true);

            }
            //Black
            else if (KimoArr[i] == -1)
            {
                Sprite StoneSprite;
                if (LastMove[0] * 19 + LastMove[1] == i)
                {
                    StoneSprite = StoneSprites[3];
                }
                else
                {
                    StoneSprite = StoneSprites[1];
                }
                string StoneName = StoneSprite.name;
                if (PrefabArr[i] == null)
                {

                    PrefabArr[i] = Instantiate(StonePrefab, new Vector2(pos_x, pos_y), Quaternion.identity);
                    Xpositions[i] = pos_x;
                    Ypositions[i] = pos_y;
                }
                PrefabArr[i].GetComponent<Stone>().StoneName = StoneName;
                PrefabArr[i].GetComponent<SpriteRenderer>().sprite = StoneSprite;
                PrefabArr[i].SetActive(true);


            }
            else if (KimoArr[i] == 0)
            {
                // continue;
                Xpositions[i] = pos_x;
                Ypositions[i] = pos_y;
                if (PrefabArr[i] != null)
                {
                    PrefabArr[i].SetActive(false);
                    PrefabArr[i].GetComponent<SpriteRenderer>().sortingOrder = -1;
                }
            }
            else
            {

            }


            // TO UPDATE POSITION PROPERLY --> BASED ON TRY & ERROR !
            pos_x = pos_x + 1.0f + inc_X;//+ (i/8.0f);
            inc_X += (0.01f / inc_2);
            inc_2++;
        }


        
    }

    void DrawCaptured()
    {
        //CapturedMove White Drawing:
        if (CapturedMoveWhite != LastCapturedMoveWhite && CapturedMoveWhite < 13)
        {
            //Debug.Log("Inside Before Drawing Last Captured Move :" + LastCapturedMoveWhite);
            //Debug.Log("Inside Before Drawing Captured Move :" + CapturedMoveWhite);
            for (int n = 0; n < (CapturedMoveWhite - LastCapturedMoveWhite); n++)
            {
                Sprite StoneSprite;
                StoneSprite = StoneSprites[0];
                string StoneName = StoneSprite.name;
                // Debug.Log("Inside  Drawing n :" + n);
                GameObject CapturedStone = Instantiate(StonePrefab, new Vector2(XCapturePositionWhite[LastCapturedIndexWhite + n], YCapturePositionWhite[LastCapturedIndexWhite + n]), Quaternion.identity);
                CapturedStone.GetComponent<Stone>().StoneName = StoneName;
                CapturedStone.GetComponent<SpriteRenderer>().sprite = StoneSprite;

            }
            LastCapturedIndexWhite += CapturedMoveWhite - LastCapturedMoveWhite;
            //Debug.Log("Inside After Drawing Captured Move Index :" + LastCapturedIndexWhite);
            LastCapturedMoveWhite = CapturedMoveWhite;
            //Debug.Log("Inside After Drawing Last Captured Move :" + LastCapturedMoveWhite);

        }

        //CapturedMove Black Drawing:
        if (CapturedMoveBlack != LastCapturedMoveBlack && CapturedMoveBlack < 13)
        {
            //Debug.Log("Inside Before Drawing Last Captured Move :" + LastCapturedMoveBlack);
            //Debug.Log("Inside Before Drawing Captured Move :" + CapturedMoveBlack);
            for (int n = 0; n < (CapturedMoveBlack - LastCapturedMoveBlack); n++)
            {
                Sprite StoneSprite;
                StoneSprite = StoneSprites[1];
                string StoneName = StoneSprite.name;
                //  Debug.Log("Inside  Drawing n :" + n);
                GameObject CapturedStone = Instantiate(StonePrefab, new Vector2(XCapturePositionBlack[LastCapturedIndexBlack + n], YCapturePositionBlack[LastCapturedIndexBlack + n]), Quaternion.identity);
                CapturedStone.GetComponent<Stone>().StoneName = StoneName;
                CapturedStone.GetComponent<SpriteRenderer>().sprite = StoneSprite;

            }
            LastCapturedIndexBlack += CapturedMoveBlack - LastCapturedMoveBlack;
            //Debug.Log("Inside After Drawing Captured Move Index :" + LastCapturedIndexBlack);
            LastCapturedMoveBlack = CapturedMoveBlack;
            // Debug.Log("Inside After Drawing Last Captured Move :" + LastCapturedMoveBlack);

        }
    }

}





