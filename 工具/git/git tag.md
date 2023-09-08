# Git的Tag管理

`git tag`命令用于创建、查看和管理标签（tags）。

标签的作用：一般在版本发布的时候，会用标签来标记一下，以便以后更容易地识别和回溯到这些提交。

## 基本用法

### 创建标签

```shell
git tag -a v1.0.0 -m "Initial release"
```

这将在当前的commit创建一个名为`v1.0.0`的标签，并附带描述信息。

### 查看标签

查看所有已创建的标签

```shell
git tag
```

如果想查看特定标签的详细信息，包括创建者、创建时间和描述信息：

```shell
git show v1.0.0
```

### 删除标签

```shell
git tag -d v1.0.0
```

### 推送标签到远程仓库

```shell
git push origin v1.0.0
```

推送所有标签到远程仓库

```shell
git push origin --tags
```

## 其他用法

### 列出commit和tag

```shell
git log --oneline --decorate
```

`--decorate`选项用于显示commit相关的标签。

查看特定分支的标签

```shell
git log --oneline --decorate master
```

这将只显示主分支上的提交和相关的标签。

> 用 q 键退出 git log视图

### 指定commit添加tag

```shell
git tag -a 版本号 [commit id] -m "描述信息"
```

例如，如果要为提交ID为`abcd1234`的提交创建一个名为`v1.0.0`的标签，并附带描述信息：

```shell
git tag -a v1.0.0 abcd1234 -m "Release version 1.0.0"
```

