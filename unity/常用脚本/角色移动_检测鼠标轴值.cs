using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Player : MonoBehaviour
{
    // 另一种实现方式
    public float speed = 10;
    private void Start()
    {
        Cursor.lockState = CursorLockMode.Locked; // 将光标锁定在Game中央
        Cursor.visible = false; // 隐藏光标
    }
    void Update()
    {
        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");
        transform.Translate(new Vector3(horizontal * Time.deltaTime * speed, 0, vertical * Time.deltaTime * speed));

        transform.Rotate(Vector3.up * Input.GetAxis("Mouse X")); // 使用Mouse X驱动旋转

        // 利用轴值实现20度平滑倾斜（倾斜空父物体下的子物体，即模型）
        // 注意，只会倾斜父物体下的第一个子物体
        transform.GetChild(0).localEulerAngles = new Vector3(vertical * 20, 0, -horizontal * 20);

        // 按下退格键时显示光标并解除锁定
        if (Input.GetKeyDown(KeyCode.Escape))
        {
            Cursor.lockState = CursorLockMode.None;
            Cursor.visible = true;
        }

        // 按下鼠标左键
        if (Input.GetMouseButtonDown(0))
        {
            Cursor.lockState = CursorLockMode.Locked;
            Cursor.visible = false;
        }
    }
}
