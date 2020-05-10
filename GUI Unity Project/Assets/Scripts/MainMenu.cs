using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEditor;

public class MainMenu : MonoBehaviour
{
    //Ruba
    public GameObject AIIcon;
    public GameObject HumanIcon;
    public GameObject QuitIcon;
    public GameObject WhiteStone;
    public GameObject BlackStone;
    public GameObject BackIcon;
    public GameObject ChooseIcon;
    public GameObject Logo;

    public static MainMenu M=null;
    public Communication ComO;
    public int ChoosenColor=-2 ;
    
    void Awake()
    {

        if (M == null)
        {
            M = this;
            ComO = new Communication();
             ComO.Start();
            DontDestroyOnLoad(gameObject);
        }
        //else if (M != this)
        //{
        //    Destroy(this.gameObject);
        //    return;
        //}
        //if (!notCreated)
        //{
        //    ComO = new Communication();
        //    ComO.Start();
        //    //ComO.Start();
        //    M = this;
        //    notCreated = true;
        //}
        //DontDestroyOnLoad(gameObject);
    }
    
    public void AIMode ()
    {
        Debug.Log("AI MODE");
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex + 1);
    }

    public void HumanMode()
    {
        //Ruba
        //Hide the main menu components:
        AIIcon.SetActive(false);
        HumanIcon.SetActive(false);
        QuitIcon.SetActive(false);
        Logo.SetActive(false);

        //Display New menu components:
        BlackStone.SetActive(true);
        WhiteStone.SetActive(true);
        BackIcon.SetActive(true);
        ChooseIcon.SetActive(true);

        
    }

    public void Quit()
    {
        
        Debug.Log("QUITTTTTTT");
        Application.Quit();
        //UnityEditor.EditorApplication.isPlaying = false;
        ComO.Stop();
        //Application.Quit();
        
    }

    public void SetChoosenColorToBlack()
    {
        ChoosenColor = 1;
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex + 2);
    }


    public void SetChoosenColorToWhite()
    {
        ChoosenColor = 0;
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex + 2);
    }

    //Ruba
    public void BackButton()
    {
        Debug.Log("Back Button Clicked in AI");

        //Show the main menu components:
        AIIcon.SetActive(true);
        HumanIcon.SetActive(true);
        QuitIcon.SetActive(true);
        Logo.SetActive(true);

        //Hide Human mode menu components:
        BlackStone.SetActive(false);
        WhiteStone.SetActive(false);
        BackIcon.SetActive(false);
        ChooseIcon.SetActive(false);
    }




}
