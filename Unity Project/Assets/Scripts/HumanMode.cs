using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.EventSystems;
using UnityEngine.UI;
using System;
using UnityEngine.SceneManagement;

public class HumanMode : MonoBehaviour
{
    public MainMenu M;
    public Timer timer;
    public GameObject Background;
    public GameObject StonePrefab;
    public GameObject BlackPlate;
    public GameObject WhitePlate;
    public GameObject Board;
    public GameObject LoseScreen;
    public GameObject WinScreen;
    public GameObject BlackScore;
    public GameObject WhiteScore;
    public GameObject PassButton;
    public GameObject ResignButton;
    public GameObject BacktoMenuButton;
    public GameObject MainBacktoMenuButon;
    public GameObject ExitButton;
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
    public int clickCount = 0;
    private Communication ComObject;
    public string ReceivedMessage;
    string[] Result;
    string Winner = "";
    bool Validation;
    private int[] LastMove = new int[2]; //{ 0, 1 };
    private string[] Score = new string[2]; //{ 0, 1 };
    public int[] KimoArr = new int[361];
    double [] xpositions=new double []{-9.35,-8.3325,-7.305,-6.272501,-5.236667,-4.198334,-3.158,-2.116,-1.072572,-0.0278933,1.017896,2.064686,3.112385,4.160917,5.210218,6.260233,7.310915,8.362223,9.414118};
    double[] Ypositions = new double[] { 9.35, 8.3325, 7.305, 6.272501, 5.236667, 4.198334, 3.158, 2.116, 1.072572, 0.0278933, - 1.017896, -2.064686, -3.112385, -4.160917, -5.210218, -6.260233, -7.310915, -8.362223, -9.414118 };
    int Xindex;
    int Yindex;
    Vector3 MousePosition;
    private int MyColor=0;          //CHANGE IT TO 0
    bool BlackPlayed = false;
    private float[] Time = new float[2];
    private int MoveValidation = -1;
    private int IsBestMove = -1;  //--> -1 if not best move , 1 if best 
    private int[] BestMove = new int[2];
    private int passcounter;
    private float TimeoldBlack;
    private float TimeoldWhite;


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




    // Start is called before the first frame update
    void Start()
    {
        timer = new Timer();
        M = GameObject.FindWithTag("MainMenu").GetComponent<MainMenu>();
        ComObject = M.ComO;
        ComObject.Mode = "1";
        ComObject.HumanColor =Convert.ToString(M.ChoosenColor);
        MyColor = M.ChoosenColor;
        Debug.Log("My color is: " + MyColor);
        ReceivedMessage = ComObject.message;
        Debug.Log("We Are In Human Mode");
        //Debug.Log("Inside SpawnStones:  " + ReceivedMessage);
        LoseScreen.SetActive(false);
        WhiteScore.SetActive(true);
        BlackScore.SetActive(true);
        WhitePlate.SetActive(true);
        BlackPlate.SetActive(true);
        Board.SetActive(true);
        WinScreen.SetActive(true);
        ExitButton.SetActive(false);
        BacktoMenuButton.SetActive(false);
        MainBacktoMenuButon.SetActive(true);
        Background.SetActive(false);
        PassButton.SetActive(true);
        ResignButton.SetActive(true);

    }

    // Update is called once per frame
    void Update()
    {
        RecievingData();
        GetMouseClick();
        DrawStones();
        DrawCaptured();
    }

    public void  onClickPass()
    {
       
        passcounter++;
        ComObject.Pass = Convert.ToString(passcounter);
        Debug.Log("Pass Button Clicked: "+ ComObject.Pass);

    }

    public void onClickResign()
    {
        Debug.Log("Resign Button Clicked");
        ComObject.Resign = "1";
        //To be removed
        LoseScreen.SetActive(true);
        WhiteScore.SetActive(false);
        BlackScore.SetActive(false);
        WhitePlate.SetActive(false);
        BlackPlate.SetActive(false);
        Board.SetActive(false);
        WinScreen.SetActive(false);
        ExitButton.SetActive(true);
        BacktoMenuButton.SetActive(true);
        MainBacktoMenuButon.SetActive(false);
        Background.SetActive(true);
        PassButton.SetActive(false);
        ResignButton.SetActive(false);

    }

    public void onClickBack()
    {
        Debug.Log("Back Button Clicked");
        ComObject.Resign = "1";
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex - 2);

    }

    public void onClickExit()
    {
        Debug.Log("Exit Button Clicked");
        //ComObject.Resign = "1";
        Application.Quit();

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
                StoneSprite = StoneSprites[1];
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
                StoneSprite = StoneSprites[0];
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

    void RecievingData()
    {
        //TO KNOW WHICH COLOR I CHOSE :
        //MyColor = M.ChoosenColor;
        //Debug.Log("My color is: " + MyColor);

        //Communication
        ReceivedMessage = string.Copy(ComObject.message);

        Result = ReceivedMessage.Split(',');
        //Debug.Log("In update Result Length:  " + Result.Length);

        if (ReceivedMessage != "TRIAL")
        {
            //TO SET WINNER:
            Winner = Result[0];


            //TO SET BOARD ARRAY :
            for (int i = 1; i < Result.Length - 12; i++)
            {
                //To know if array contains a black stone:
                if (MyColor == 1 && KimoArr[i - 1] == -1)
                    BlackPlayed = true;

                KimoArr[i - 1] = Convert.ToInt32(Result[i]);
                //Debug.Log("  Received of " + i + "--> " + Result[i]);
            }

            //TO SET SCORE:
            Score[0] = Result[362];
            Score[1] = Result[363];


            //TO SET LAST MOVE:
            LastMove[0] = Convert.ToInt32(Result[364]);
            LastMove[1] = Convert.ToInt32(Result[365]);

            //TO SET TIME:
            Time[0] = float.Parse(Result[366]);  // BLACK
            Time[1] = float.Parse(Result[37]); // WHITE
            //Debug.Log("TIME: " + Time[0] + " " + Time[1]);

           
           

            //TO CHECK IF MOVE IS VALID:
            //MoveValidation = Convert.ToInt32(Result[368]); // CHECK HERE !
            //Debug.Log("VAL: " + MoveValidation);

            //TO CHECK IF ITS THE BEST MOVE:
            IsBestMove = Convert.ToInt32(Result[369]);
            Debug.Log("IsBetterMove : " + IsBestMove);

            //
            BestMove[0] = Convert.ToInt32(Result[370]);
            BestMove[1] = Convert.ToInt32(Result[371]);
            Debug.Log("BetterMove X,Y : " + BestMove[0] + BestMove[1]);

            CapturedMoveBlack = Convert.ToInt32(Result[372]); // black
            CapturedMoveWhite = Convert.ToInt32(Result[373]); // white
            //Debug.Log("Captured: " + CapturedMoveBlack + " " + CapturedMoveWhite);
            //Debug.Log("BETTER MOVE :" + BestMove[0] + BestMove[1]);

           
            //IF HE CHOOSE BLACK :
            if (MyColor == -1)
                BlackPlayed = true;

            //TO DISPLAY SCORE : CHANGE TIME ?
            UI = GameObject.FindWithTag("UI").GetComponent<UIManager>();
            UI.updateScore(Score);
            UI.updateMessage(IsBestMove,MyColor,BestMove);
            //if (Time[0] != -1 && Time[1] != -1 && Time[0] != TimeoldBlack && Time[1] != TimeoldWhite)
            //{
            //    Debug.Log("iNSIDE IF TIME:");
            //    UI.StartCoundownTimer(Time[0], Time[1]);
            //    TimeoldBlack = Time[0];
            //    TimeoldWhite = Time[1];
            //}



            if (Winner == "w")
            {
                PassButton.SetActive(false);
                ResignButton.SetActive(false);
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
                PassButton.SetActive(false);
                ResignButton.SetActive(false);
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
                Background.SetActive(false);
            }




        }


    }

    void GetMouseClick()
    {
        //Get Mouse Input
        if (Input.GetKeyDown(KeyCode.Mouse0))
        {
            MousePosition = Camera.main.ScreenToWorldPoint(Input.mousePosition);
            Debug.Log("Mouse Position: " + MousePosition);
            if (MousePosition.x < -9.7 || MousePosition.x > 9.7 || MousePosition.y < -9.7 || MousePosition.y > 9.7)
            {
                Xindex = -1;
                Yindex = -1;
            }
            else
            {
                for (int k = 0; k < xpositions.Length; k++)
                {
                    if (MousePosition.x > (xpositions[k] - 0.5) && MousePosition.x < (xpositions[k] + 0.5))
                    {
                        Yindex = k; // col sa7 
                        break;
                    }
                }
                for (int k = 0; k < Ypositions.Length; k++)
                {
                    if (MousePosition.y > (Ypositions[k] - 0.5) && MousePosition.y < (Ypositions[k] + 0.5))
                    {
                        Xindex = k;
                        break;
                    }
                }
            }

            ComObject.Xindex = Convert.ToString(Xindex);
            ComObject.Yindex = Convert.ToString(Yindex);
            Debug.Log("X index" + Xindex);
            Debug.Log("Y index" + Yindex);


        }

    }


    void DrawStones()
    {

        //if (BlackPlayed)
        
        Debug.Log("IN IF BLACK PLAYED");
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

                }
                PrefabArr[i].GetComponent<Stone>().StoneName = StoneName;
                PrefabArr[i].GetComponent<SpriteRenderer>().sprite = StoneSprite;
                PrefabArr[i].SetActive(true);


            }
            else if (KimoArr[i] == 0)
            {
                    
                bool DoNotEreaseBestMove = false;
                //TO DRAW THE BEST POSSIBLE MOVE :
                if (IsBestMove == -1 &&(BestMove[0] != -1 && BestMove[1]!=-1)&& (BestMove[0] * 19 + BestMove[1]) == i)       // if there is a better move , draw it in red
                {
                    //Debug.Log("henaaaaaa");
                    Sprite StoneSprite = StoneSprites[4];

                    if (PrefabArr[i] == null)
                        PrefabArr[i] = Instantiate(StonePrefab, new Vector2(pos_x, pos_y), Quaternion.identity);

                    PrefabArr[i].GetComponent<SpriteRenderer>().sprite = StoneSprite;
                    PrefabArr[i].SetActive(true);
                    DoNotEreaseBestMove = true;

                }

                //TO ERASE SPRITES:
                if (PrefabArr[i] != null && !DoNotEreaseBestMove)
                {
                    //Debug.Log("MSH HENAAAAA");
                    PrefabArr[i].SetActive(false);
                    //PrefabArr[i].GetComponent<SpriteRenderer>().sortingOrder = -1;

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


}



