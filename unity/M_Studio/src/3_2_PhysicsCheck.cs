// PhysicsCheck.cs
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PhysicsCheck : MonoBehaviour
{
    CapsuleCollider2D coll;

    [Header("检测参数")]
    // 是否手动设置检测范围
    public bool manual;
    // 人物脚底位移插值
    public Vector2 bottomOffset;

    public Vector2 leftOffset;
    public Vector2 rightOffset;

    public float checkRadius;

    // 检测的层级
    public LayerMask groundLayer;

    [Header("状态")]
    // 检测半径
    public bool isGround;
    
    public bool touchLeftWall;
    public bool touchRightWall;

    // 是否在跑
    public bool isRun;

    private void Awake() {
        coll = GetComponent<CapsuleCollider2D>();
        if (!manual)
        {
            // rightOffset = new Vector2(coll.size.x/2, coll.size.y / 2);
            // leftOffset = new Vector2(-coll.size.x/2, coll.size.y / 2);
            rightOffset = new Vector2(coll.bounds.size.x / 2 + coll.offset.x , coll.bounds.size.y / 2);
            leftOffset = new Vector2(-rightOffset.x - checkRadius, rightOffset.y);
        }
    }

    private void Update()
    {
        Check();
    }

    public void Check()
    {
        // 地面判断
        isGround = Physics2D.OverlapCircle((Vector2)transform.position + new Vector2(bottomOffset.x * transform.localScale.x, bottomOffset.y), checkRadius, groundLayer);
        // 墙体判断
        touchLeftWall = Physics2D.OverlapCircle((Vector2)transform.position + leftOffset, checkRadius, groundLayer);
        touchRightWall = Physics2D.OverlapCircle((Vector2)transform.position + rightOffset, checkRadius, groundLayer);
    }

    // Unity内置的方法，绘制到Scene窗口内
    private void OnDrawGizmosSelected() {
        Gizmos.DrawWireSphere((Vector2)transform.position + new Vector2(bottomOffset.x * transform.localScale.x, bottomOffset.y), checkRadius, groundLayer);
        Gizmos.DrawWireSphere((Vector2)transform.position + leftOffset, checkRadius);
        Gizmos.DrawWireSphere((Vector2)transform.position + rightOffset, checkRadius);
    }
}
