- # [创建版本库](https://www.liaoxuefeng.com/wiki/896043488029600/896827951938304)

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

`git diff --cached <file>`不知为何，我要这么写才能看到变化

**Git无法显示中文**

cmd：`set LESSCHARSET=utf-8`

PowerShell: `$env:LESSCHARSET='utf-8'`

**重命名文件**

`git mv oldname newname`

## [版本回退](https://www.liaoxuefeng.com/wiki/896043488029600/897013573512192)

**查看版本日志，按`Q`退出**
`head`表示当前版本，`head^`表示上个版本

`git log`

**回到以前的版本**

`git reset --hard HEAD^ `（最好在结尾加个空格，不然可能会出问题）

`git reset --hard <commit_id>`

`git reflog`查看以前输入的命令

## [工作区和暂存区](https://www.liaoxuefeng.com/wiki/896043488029600/897271968352576)

**工作区（Working Directory）**

电脑里能看到的目录，比如`LightNote`

  

  ![working-dir](picture\workingdir.png)

**版本库（Repository）**

工作区有一个隐藏目录`.git`，这个不算工作区，而是Git的版本库。

Git的版本库里存了很多东西，其中最重要的就是称为stage（或者叫index）的暂存区，还有Git为我们自动创建的第一个分支`master`，以及指向`master`的一个指针叫`HEAD`。

![git-repo](picture/git-repo)

分支和`HEAD`的概念我们以后再讲。

前面讲了我们把文件往Git版本库里添加的时候，是分两步执行的：

第一步是用`git add`把文件添加进去，实际上就是把文件修改添加到暂存区；

第二步是用`git commit`提交更改，实际上就是把暂存区的所有内容提交到当前分支。

因为我们创建Git版本库时，Git自动为我们创建了唯一一个`master`分支，所以，现在，`git commit`就是往`master`分支上提交更改。

你可以简单理解为，需要提交的文件修改通通放到暂存区，然后，一次性提交暂存区的所有修改。

## [管理修改](https://www.liaoxuefeng.com/wiki/896043488029600/897884457270432)

第一次修改->`git add`->第二次修改->`git commit`

其实只提交了第一次修改的内容，第二次修改**不会**更新。

想要提交修改，一定要在修改之后执行`git add`

## [撤销修改](https://www.liaoxuefeng.com/wiki/896043488029600/897889638509536)



## [删除文件](https://www.liaoxuefeng.com/wiki/896043488029600/900002180232448)



