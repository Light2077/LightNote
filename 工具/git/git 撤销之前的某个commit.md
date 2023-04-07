https://blog.csdn.net/weixin_43743711/article/details/116158827

假如我先后提交了commit，c1, c2, c3，c3是最新的commit，结果我发现c1有错，需要撤销c1的更改，如何操作？

要撤销一个之前的 commit，可以使用 `git revert` 命令。在您的例子中，如果您想要撤销 c1 的更改，而保留 c2 和 c3 的更改，可以按照以下步骤操作：

1. 执行 `git log` 命令，查找 c1 的 SHA-1 值（commit ID）。您可以在 commit 记录中找到该值，它通常以 40 个字符的哈希值表示。
2. 执行 `git revert <c1 SHA-1>` 命令，其中 `<c1 SHA-1>` 是您在第 1 步中找到的 c1 的 SHA-1 值。该命令会创建一个新的 commit，该 commit 会撤销 c1 的更改，但保留 c2 和 c3 的更改。
3. 在提交撤销 commit 后，可以使用 `git log` 命令来查看提交历史记录，并确保您已成功撤销了 c1 的更改。

需要注意的是，使用 `git revert` 命令会创建一个新的 commit，该 commit 撤销之前的 commit，而不是从代码库中完全删除该 commit。这样可以保持代码库的完整性，同时确保不会丢失任何已有的更改历史记录。