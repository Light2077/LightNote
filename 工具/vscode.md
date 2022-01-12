https://www.zhihu.com/question/322530705/answer/860418884

## 常用快捷键

变量重命名：`F2`（会自动对其他文件里引用的该变量进行重命名）

设置代码运行使用的python解释器：

- 输入快捷键`ctrl + shift + P`，在界面顶端弹出搜索窗
- 在搜索窗中输入`>python select interpreter`，回车
- 选择自动搜索到的python解释器路径，或手动输入路径。

代码跳转后回退：`alt + ←`



## 免密登录

本机为windows，远端为linux。希望vscode每次连接到远端时无需重新输入密码

将本机的`id_rsa.pub`文件拷贝到远端`~`目录下

写入authorized_keys

```
cat ~/id_rsa.pub >> authorized_keys
```

