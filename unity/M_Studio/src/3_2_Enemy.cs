using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Enemy : MonoBehaviour
{
    PhysicsCheck physicsCheck;
    [Header("计时器")]
    public float waitTime;
    public float waitTimeCounter;
    public bool wait;


    [Header("基本参数")]
    public float normalSpeed;
    public float chaseSpeed;
    public float currentSpeed;
    public Vector3 faceDir;

    Rigidbody2D rb;
    protected Animator anim;

    private void Awake() {
        rb = GetComponent<Rigidbody2D>();
        anim = GetComponent<Animator>();
        physicsCheck = GetComponent<PhysicsCheck>();
        currentSpeed = normalSpeed;
        waitTimeCounter = waitTime;
    }

    private void Update() {
        faceDir = new Vector3(-transform.localScale.x, 0, 0);
        // Vector3 scale = transform.localScale;
        
        // if (physicsCheck.touchLeftWall)
        // {
        //     scale.x = -1f;
        //     transform.localScale = scale;
        //     Debug.Log(transform.localScale);
        // }

        // if (physicsCheck.touchRightWall)
        // {
        //     scale.x = 1f;
        //     transform.localScale = scale;
        //     Debug.Log(transform.localScale);
        // }

        // 老师写的
        // if (physicsCheck.touchLeftWall || physicsCheck.touchRightWall)) {
        //     // 这种感觉有问题，撞墙是一个连续的状态，会不断更改猪的方向
        //     transform.localScale = new Vector3(faceDir.x, 1, 1);
        // }

        // 自己写的改版
        // if (physicsCheck.touchLeftWall) {
        //     transform.localScale = new Vector3(-1, 1, 1);
        // }
        // else if (physicsCheck.touchRightWall) {
        //     transform.localScale = new Vector3(1, 1, 1);
        // }

        // 老师的改版，撞墙时等待，撞墙时停止播放动画
        if ((physicsCheck.touchLeftWall && faceDir.x < 0) || (physicsCheck.touchRightWall && faceDir.x > 0)) {
            wait = true;
            anim.SetBool("walk", false);
        }
        TimeCounter();
    }
    private void FixedUpdate() {
        Move();
    }
    public virtual void Move() {
        rb.velocity = new Vector2(currentSpeed * faceDir.x * Time.deltaTime ,rb.velocity.y);
    }

    public void TimeCounter()
    {
        if (wait)
        {
            waitTimeCounter -= Time.deltaTime;
            if (waitTimeCounter <= 0)
            {
                wait = false;
                waitTimeCounter = waitTime;
                transform.localScale = new Vector3(faceDir.x, 1, 1);
            }
        }
    }
}
