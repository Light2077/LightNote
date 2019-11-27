# [创建版本库](https://www.liaoxuefeng.com/wiki/896043488029600/896827951938304)

**增加文件：把文件添加到仓库**

`git add <file>`

**提交文件：会显示你仓库中的文件的改动情况**

`git commit -m <message>  `



```
e:\GitHub\LightNote>git commit -m "my first git commit"
[master (root-commit) a311ad6] my first git commit
 1 file changed, 3 insertions(+)
 create mode 100644 README.md
```



# [时光机穿梭](https://www.liaoxuefeng.com/wiki/896043488029600/896954074659008)

**查看工作区状态：查看有哪些文件改动**

`git status`

**查看文件改动的情况**

`git diff <file>`

**Git无法显示中文**

cmd：`set LESSCHARSET=utf-8`

PowerShell: `$env:LESSCHARSET='utf-8'`

**重命名文件**

`git mv oldname newname`

## [版本回退](https://www.liaoxuefeng.com/wiki/896043488029600/897013573512192)

- 发生了什么