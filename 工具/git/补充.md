# note的补充

- 如何初始化Gitignore，在这个网站查找https://github.com/github/gitignore

### 清除工作区未跟踪的文件

- `git clean -f -d`清除工作目录中所有未追踪的文件以及空的子目录（不会清除.gitiignore匹配到的文件）
- `git clean -d -n`只是看看会清除什么，不会清除

### stash保存工作区进度

适用于不能马上commit的情况，只会隐藏`git add`后的文件。

`git stash list`

`git stash pop`

### git查看树形结构图

### reset的 --hard --mixed

--hard 重置的同时 工作区 暂存区 本地库都变化

--mixed 暂存区 本地库变化，工作区不变

--soft 只变本地库，暂存区，工作区不变



### diff命令

`git diff test1.txt`

比较工作区与暂存区的文件

`git diff`

比较工作区与暂存区所有文件的差异



`git diff HEAD test1.txt  ` 

比较暂存区与**本地库**的文件差异

**主要用hard**

## 自检

- 查看分支

