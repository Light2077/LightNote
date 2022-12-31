using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Player : MonoBehaviour
{

    // 另一种实现方式 效果更好，而且有平滑的倾斜效果
    // 不用绑定WASD了，Unity会自动检测有没有按下WASD 或者 上下左右
    public float speed = 10;
    private void FixedUpdate()
    {
        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");
        transform.Translate(new Vector3(horizontal * Time.deltaTime * speed, 0, vertical * Time.deltaTime * speed));

        if (Input.GetKey(KeyCode.Q)) transform.Rotate(Vector3.down);
        if (Input.GetKey(KeyCode.E)) transform.Rotate(Vector3.up);

        // 利用轴值实现20度平滑倾斜（倾斜空父物体下的子物体，即模型）
        // 注意，只会倾斜父物体下的第一个子物体
        transform.GetChild(0).localEulerAngles = new Vector3(vertical * 20, 0, -horizontal * 20);

    }

}
