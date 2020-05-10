using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Stone : MonoBehaviour
{
    // Start is called before the first frame update
    private Vector2 StonePosition;
    public string StoneName;
    void Start()
    {
        StonePosition = transform.position;
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
