# [创建版本库](https://www.liaoxuefeng.com/wiki/896043488029600/896827951938304)

`git add <file>`

增加文件：把文件添加到仓库

`git commit -m <message>  `

提交文件：提交文件，会显示你仓库中的文件的改动情况

```
e:\GitHub\LightNote>git commit -m "my first git commit"
[master (root-commit) a311ad6] my first git commit
 1 file changed, 3 insertions(+)
 create mode 100644 README.md
```



# [时光机穿梭](https://www.liaoxuefeng.com/wiki/896043488029600/896954074659008)

Git无法显示中文

cmd：`set LESSCHARSET=utf-8`

PowerShell: `$env:LESSCHARSET='utf-8'`