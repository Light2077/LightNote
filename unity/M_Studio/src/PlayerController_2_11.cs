using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;
public class PlayerController : MonoBehaviour
{
    public PlayerInputControl inputControl;
    // 获取刚体组件
    private Rigidbody2D rb;
    // 获取碰撞体
    private CapsuleCollider2D coll;  // 也可以直接使用 Collider2D
    // 获取另一个脚本对象
    private PhysicsCheck physicsCheck;

    // 获取Sprite Renderer
    private SpriteRenderer sr;

    public Vector2 inputDirection;

    [Header("基本参数")]
    // 定义速度
    public float speed;
    private float runSpeed;
    // 这表示自动属性，如果speed变化，这个属性也变化
    private float walkSpeed => speed / 2f;
    public float jumpForce;

    // 下蹲状态
    public bool isCrouch;

    // 碰撞体的初始状态
    private Vector2 orginalOffset;
    private Vector2 orginalSize;
    // 反弹的力
    public float hurtForce;
    // 受伤判断变量
    public bool isHurt;

    public bool isDead;

    private void Awake()
    {
        inputControl = new PlayerInputControl();
        rb = GetComponent<Rigidbody2D>();
        sr = GetComponent<SpriteRenderer>();
        physicsCheck = GetComponent<PhysicsCheck>();
        coll = GetComponent<CapsuleCollider2D>();
        inputControl.Gameplay.Jump.started += Jump;
        // inputControl.Gameplay.Run.started += Run;

        // 要在awake() 里获取这个值
        runSpeed = speed;

        // 获得碰撞体的初始状态
        orginalOffset = coll.offset;
        orginalSize = coll.size;

        #region 强制走路
        // 老师在 InputAction.CallbackContext ctx 的左右没有加括号，应该跟c#版本有关。
        inputControl.Gameplay.WalkButton.performed += (InputAction.CallbackContext ctx) => {
            if (physicsCheck.isGround)
                speed = walkSpeed;
        };

        inputControl.Gameplay.WalkButton.canceled += (InputAction.CallbackContext ctx) => {
            if (physicsCheck.isGround)
                speed = runSpeed;
        };
        #endregion
        // 自己写的
        // #region 下蹲
        // inputControl.Gameplay.Crouch.performed += (InputAction.CallbackContext ctx) => {
        //     isCrouch = true;
        // };

        // inputControl.Gameplay.Crouch.canceled += (InputAction.CallbackContext ctx) => {
        //     isCrouch = false;
        // };
        // #endregion
    }

    private void OnEnable()
    {
        inputControl.Enable();
    }

    private void OnDisable()
    {
        inputControl.Disable();
    }

    private void Update() {
        inputDirection = inputControl.Gameplay.Move.ReadValue<Vector2>();
        // 按住Run键时是跑步
        // if (inputControl.Gameplay.Run.inProgress) {
        //     speed = 300;
        // }
        // else {
        //     speed = 150;
        // }
        
    }

    private void FixedUpdate() {
        if (!isHurt)
        {
            Move();
        }
    }
    // 测试
    // private void OnTriggerStay2D(Collider2D other) {
    //     Debug.Log(other.name);
    // }
    public void Move() {
        // 默认的y是 -9.81
        rb.velocity = new Vector2(inputDirection.x * speed * Time.deltaTime, rb.velocity.y);

        // 人物翻转
        // int faceDir = (int)transform.localScale.x;
        if (inputDirection.x > 0)
            sr.flipX = false;

        if (inputDirection.x < 0)
            sr.flipX = true;

        // transform.localScale = new Vector3(faceDir, 1, 1);
        isCrouch = inputDirection.y < -0.5f && physicsCheck.isGround;

        if (isCrouch)
        {
            // 修改碰撞体大小和位移
            coll.offset = new Vector2(-0.05f, 0.85f);
            coll.size = new Vector2(0.7f, 1.7f);
        }
        else
        {
            // 还原
            coll.offset = orginalOffset;
            coll.size = orginalSize;
        }
    }

    private void Jump(InputAction.CallbackContext obj) {
        // Debug.Log("JUMP");
        if (physicsCheck.isGround) {
            rb.AddForce(transform.up * jumpForce, ForceMode2D.Impulse);
        }
    }

    private void Run(InputAction.CallbackContext obj) {
        if (speed >= 200) 
        {
            //isRun = false;
            speed = 150;
        }
        else
        {
            //isRun = true;
            speed = 300;
        }
    }
    public void GetHurt(Transform attacker)
    {
        isHurt = true;
        rb.velocity = Vector2.zero;
        Vector2 dir = new Vector2((transform.position.x - attacker.position.x), 0).normalized;
        rb.AddForce(dir * hurtForce, ForceMode2D.Impulse);
    }

    public void PlayerDead()
    {
        isDead = true;
        inputControl.Gameplay.Disable(); // 不给玩家操作了
    }
}
