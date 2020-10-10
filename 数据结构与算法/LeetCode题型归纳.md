## 说明



:cheese: 多做几次

:x:毫无头绪

## 常见错误

- 返回值没考虑特殊情况

## 经验总结

### 思路启迪

- 一维数组，关于求和，可以想到
  - 前缀和
  - 把目标值考虑到算法中，比如创建一个`dp = [0] * len(nums)`
- 有正有负的乘法动态规划，可以考虑用两个dp数组

### o(n^2)怎么优化到o(nlogn)

- 排序（排序后结合二分法）
- 堆

### 动态规划的思考流程

- 考虑能否缩减问题的规模
  - 分治：每次减小一半
  - 每次减小一个
- dp数组的形式
  - 一个一维dp，dp[n]可能与dp[n-1]有关，也可能与dp[1] 到 dp[n-1] 都有关
  - 两个一维dp，关联程度如上
  - 如果只与dp[n-1]有关，可以简化成单个数字

### 字符串

#### [剑指 Offer 58 - I. 翻转单词顺序](https://leetcode-cn.com/problems/fan-zhuan-dan-ci-shun-xu-lcof/)

要求，不能使用队列，不能使用word列表

#### [剑指 Offer 46. 把数字翻译成字符串](https://leetcode-cn.com/problems/ba-shu-zi-fan-yi-cheng-zi-fu-chuan-lcof/)

从前往后跟从后往前是一样的

### 数组

#### [剑指 Offer 45. 把数组排成最小的数](https://leetcode-cn.com/problems/ba-shu-zu-pai-cheng-zui-xiao-de-shu-lcof/)

(难) 感觉我的方法有点取巧，但是思路应该是对的。有更加精妙的思路。

#### [剑指 Offer 39. 数组中出现次数超过一半的数字](https://leetcode-cn.com/problems/shu-zu-zhong-chu-xian-ci-shu-chao-guo-yi-ban-de-shu-zi-lcof/)

摩尔排序法很秀。

### **二分查找**：

- `nums[mid]` 不仅可以和target值比较
- `nums[mid]` 和 `nums[mid-1]` 或 `nums[mid+1]` 比较。比如[162. 寻找峰值](https://leetcode-cn.com/problems/find-peak-element/)
- `nums[mid]`和`nums[low]`或`nums[high]`比较[剑指 Offer 11. 旋转数组的最小数字](https://leetcode-cn.com/problems/xuan-zhuan-shu-zu-de-zui-xiao-shu-zi-lcof/)

#### [354. 俄罗斯套娃信封问题](https://leetcode-cn.com/problems/russian-doll-envelopes/)

难题，暴力最后一个样例通不过。

#### [剑指 Offer 53 - II. 0～n-1中缺失的数字](https://leetcode-cn.com/problems/que-shi-de-shu-zi-lcof/)

注意特例：缺失的数字处于边界的情况。	（用了新的二分查找思路，少了一个判断）

#### [209. 长度最小的子数组](https://leetcode-cn.com/problems/minimum-size-subarray-sum/)
:cheese:这题本来可以用o(n)复杂度解题的，但是为了追求骚操作，硬是要来o(log(n))的二分查找解题法。主要是熟悉二分查找模板。信手拈来。

#### [162. 寻找峰值](https://leetcode-cn.com/problems/find-peak-element/)
:cheese:这也能二分我是没想到的，做第二次时没做出来



#### [34. 在排序数组中查找元素的第一个和最后一个位置](https://leetcode-cn.com/problems/find-first-and-last-position-of-element-in-sorted-array/)
二分查找左右边界的问题比如`[4,5,5,8,8,8,9]`返回8的左或右索引

#### [240. 搜索二维矩阵 II](https://leetcode-cn.com/problems/search-a-2d-matrix-ii/)

#### [300. 最长上升子序列](https://leetcode-cn.com/problems/longest-increasing-subsequence/)

这也能二分我是没想到的

#### [35. 搜索插入位置](https://leetcode-cn.com/problems/search-insert-position/)

简单

#### [69. x 的平方根](https://leetcode-cn.com/problems/sqrtx/)

:cheese: 这也能二分我是没想到的

#### [剑指 Offer 11. 旋转数组的最小数字](https://leetcode-cn.com/problems/xuan-zhuan-shu-zu-de-zui-xiao-shu-zi-lcof/)

:cheese:，不要只考虑if else，考虑if elif else。

在考虑问题的时候，如果感觉很难办，试试考虑另一个方向

#### [剑指 Offer 31. 栈的压入、弹出序列](https://leetcode-cn.com/problems/zhan-de-ya-ru-dan-chu-xu-lie-lcof/)

### 队列

#### [剑指 Offer 59 - II. 队列的最大值](https://leetcode-cn.com/problems/dui-lie-de-zui-da-zhi-lcof/)

:cheese:这题算不算是单调队列的应用，这题算是对我思路的一个扩充，我知道是要使用单调队列来做，但是不知道怎么处理单调队列。主要是要考虑队列的特性：能在两边添加删除元素。

### 栈

#### [剑指 Offer 31. 栈的压入、弹出序列](https://leetcode-cn.com/problems/zhan-de-ya-ru-dan-chu-xu-lie-lcof/)

错了六次才对，看了题解发现自己的方法确实有点笨。。

#### [剑指 Offer 30. 包含min函数的栈](https://leetcode-cn.com/problems/bao-han-minhan-shu-de-zhan-lcof/)

这题考察的是单调栈

#### [剑指 Offer 09. 用两个栈实现队列](https://leetcode-cn.com/problems/yong-liang-ge-zhan-shi-xian-dui-lie-lcof/)

这题我在想一个栈存元素，一个栈存索引，我在想啥呢。要拓展思路，就是有可能一个栈存元素另一个存索引，也有可能两个栈都存元素，思路不应该太狭隘。

栈的特性：后进先出。且把一个栈的元素倒到另一个栈里就是先进先出。

### 链表

#### [剑指 Offer 52. 两个链表的第一个公共节点](https://leetcode-cn.com/problems/liang-ge-lian-biao-de-di-yi-ge-gong-gong-jie-dian-lcof/)

最容易想到的是hash表。双指针我一开始想到了，但是思路被局限了，对于链表这种题，可以考虑指针又重新归于头结点。

#### [剑指 Offer 25. 合并两个排序的链表](https://leetcode-cn.com/problems/he-bing-liang-ge-pai-xu-de-lian-biao-lcof/)

我手动创建了一个头结点。题解和我思路一致

#### [剑指 Offer 24. 反转链表](https://leetcode-cn.com/problems/fan-zhuan-lian-biao-lcof/)

非递归方式可以做出来，多想象链表的操作，有点类似于栈。

递归的方式没做出来，看了题解后恍然大悟，我当时再想怎么取到最后一个结点，然后把第一个结点接到最后一个结点上面，结果发现这其实是很容易的一件事。只要牢牢把握住第一个结点是指向谁的。

#### [剑指 Offer 18. 删除链表的节点](https://leetcode-cn.com/problems/shan-chu-lian-biao-de-jie-dian-lcof/)

能做出来，但是[代码](https://leetcode-cn.com/submissions/detail/101731003/)不是最优化的状态，可以少一个if判断

#### [剑指 Offer 22. 链表中倒数第k个节点](https://leetcode-cn.com/problems/lian-biao-zhong-dao-shu-di-kge-jie-dian-lcof/)

###  **双指针**

- 移动指针的时候，思考移动哪边，移动哪边能让答案更近一步

#### [11. 盛最多水的容器](https://leetcode-cn.com/problems/container-with-most-water/)

:cheese: 这题好吧，我想到了双指针，关键在于怎么移动指针，移动哪个。这个思路很关键。

#### [剑指 Offer 22. 链表中倒数第k个节点](https://leetcode-cn.com/problems/lian-biao-zhong-dao-shu-di-kge-jie-dian-lcof/)

#### [209. 长度最小的子数组](https://leetcode-cn.com/problems/minimum-size-subarray-sum/)

o(n)的双指针解法，注意怎么利用嵌套的while循环解决问题。第一次企图用一个while循环来解决(i++, j++)的问题，其实反而变复杂了。

#### [33. 搜索旋转排序数组](https://leetcode-cn.com/problems/search-in-rotated-sorted-array/)

### **二叉树**：

- 二叉搜索树性质，中序遍历是递增的

#### [501. 二叉搜索树中的众数](https://leetcode-cn.com/problems/find-mode-in-binary-search-tree/)

:cheese: 这题要多练，简单的代码都写不顺了。

#### [剑指 Offer 68 - I. 二叉搜索树的最近公共祖先](https://leetcode-cn.com/problems/er-cha-sou-suo-shu-de-zui-jin-gong-gong-zu-xian-lcof/)

简单题，利用二叉搜索树的性质可以轻松解题。



#### [剑指 Offer 68 - II. 二叉树的最近公共祖先](https://leetcode-cn.com/problems/er-cha-shu-de-zui-jin-gong-gong-zu-xian-lcof/)

:cheese:其实挺简单一题，就是没想明白，递归的返回值的含义。

#### [剑指 Offer 55 - II. 平衡二叉树](https://leetcode-cn.com/problems/ping-heng-er-cha-shu-lcof/)

返回值可以带上两个，一个表示子树是不是平衡二叉树，另一个表示高度

#### [剑指 Offer 37. 序列化二叉树](https://leetcode-cn.com/problems/xu-lie-hua-er-cha-shu-lcof/)



#### [剑指 Offer 33. 二叉搜索树的后序遍历序列](https://leetcode-cn.com/problems/er-cha-sou-suo-shu-de-hou-xu-bian-li-xu-lie-lcof/)

其实不难，好好结合二叉搜索树的性质就能解出来。

看了题解，真的妖孽。好好优化一下吧

#### [剑指 Offer 32 - I. 从上到下打印二叉树](https://leetcode-cn.com/problems/cong-shang-dao-xia-da-yin-er-cha-shu-lcof/)

#### [剑指 Offer 32 - II. 从上到下打印二叉树 II](https://leetcode-cn.com/problems/cong-shang-dao-xia-da-yin-er-cha-shu-ii-lcof/)

#### [剑指 Offer 32 - III. 从上到下打印二叉树 III](https://leetcode-cn.com/problems/cong-shang-dao-xia-da-yin-er-cha-shu-iii-lcof/)

#### [剑指 Offer 27. 二叉树的镜像](https://leetcode-cn.com/problems/er-cha-shu-de-jing-xiang-lcof/)

其实挺简单的，我自己想复杂了，把树的结构图画出来，观察一下结点的变化情况就可轻松求解。

#### [剑指 Offer 26. 树的子结构](https://leetcode-cn.com/problems/shu-de-zi-jie-gou-lcof/)

我自己写出来了，但是[代码](https://leetcode-cn.com/submissions/detail/102155961/)和[题解](https://leetcode-cn.com/problems/shu-de-zi-jie-gou-lcof/solution/mian-shi-ti-26-shu-de-zi-jie-gou-xian-xu-bian-li-p/)比真的差远了。

主要是可以优化的地方有很多，思路其实差不多。

#### [98. 验证二叉搜索树](https://leetcode-cn.com/problems/validate-binary-search-tree/)
中序遍历，上下界递归

#### [230. 二叉搜索树中第K小的元素](https://leetcode-cn.com/problems/kth-smallest-element-in-a-bst/)
中序遍历

#### [剑指 Offer 07. 重建二叉树](https://leetcode-cn.com/problems/zhong-jian-er-cha-shu-lcof/)

注意，在迭代的过程中，前序和中序的位置关系是会发生变化的。可能索引对应的位置会不一样。

### **回溯算法**

回溯是一种通过穷举所有可能情况来找到所有解的算法。如果一个候选解最后被发现并不是可行解，回溯算法会舍弃它，并在前面的一些步骤做出一些修改，并重新尝试找到可行解。

框架 func(组合, 缩小的子条件)

#### [剑指 Offer 38. 字符串的排列](https://leetcode-cn.com/problems/zi-fu-chuan-de-pai-lie-lcof/)

代码修改后，加入了剪枝，效率大幅提高

#### [17. 电话号码的字母组合](https://leetcode-cn.com/problems/letter-combinations-of-a-phone-number/)

#### [22. 括号生成](https://leetcode-cn.com/problems/generate-parentheses/)

#### [46. 全排列](https://leetcode-cn.com/problems/permutations/)

多做几遍

#### [78. 子集](https://leetcode-cn.com/problems/subsets/)
多做几遍

#### [79. 单词搜索](https://leetcode-cn.com/problems/word-search/)

多做几遍



### **排序**

#### [LCP 18. 早餐组合](https://leetcode-cn.com/problems/2vYnGI/)

:cheese: 这题，有线性复杂度的解法，把我给看呆了。我是先暴力解法解出来了，然后用排序求解。运用了**两数之和的思想**

#### [75. 颜色分类](https://leetcode-cn.com/problems/sort-colors/)

#### [56. 合并区间](https://leetcode-cn.com/problems/merge-intervals/)
官方的代码比我的优雅很多，我的思路是对的

### **堆**

#### [215. 数组中的第K个最大元素](https://leetcode-cn.com/problems/kth-largest-element-in-an-array/)

#### [692. 前K个高频单词](https://leetcode-cn.com/problems/top-k-frequent-words/)

### **快排**

#### [215. 数组中的第K个最大元素](https://leetcode-cn.com/problems/kth-largest-element-in-an-array/)



### **动态规划**

#### [740. 删除与获得点数](https://leetcode-cn.com/problems/delete-and-earn/)

:x:毫无头绪，思路是想办法转成打家劫舍问题，但其实也不是很像打家劫舍问题，需要一定的随机应变。

#### [213. 打家劫舍 II](https://leetcode-cn.com/problems/house-robber-ii/)

#### [198. 打家劫舍](https://leetcode-cn.com/problems/house-robber/)

:cheese:以前做过的题，结果居然做错了。

- 用一个N × 2的数组记录每天偷或不偷的最高收益
  - 优化成1 × 2
- 用一个N维列表记录第i天能获得的最大收益



#### [363. 矩形区域不超过 K 的最大数值和](https://leetcode-cn.com/problems/max-sum-of-rectangle-no-larger-than-k/)

:cheese: 思路是对的，暴力法差最后一个样例通过不了，和[面试题 17.24. 最大子矩阵](https://leetcode-cn.com/problems/max-submatrix-lcci/)的思路比较相似

#### [面试题 17.24. 最大子矩阵](https://leetcode-cn.com/problems/max-submatrix-lcci/)

:x:做完了，其实我的思路是对的，就是想办法把二维降成一维的，这题肯定是多练练，练习这个把二维降成一维的思路

然后就是写代码的时候要稳

#### [LCP 19. 秋叶收藏集](https://leetcode-cn.com/problems/UlBDOe/)

有点难的这道题，怎么想到初始状态的

#### [剑指 Offer 63. 股票的最大利润](https://leetcode-cn.com/problems/gu-piao-de-zui-da-li-run-lcof/)

就这

#### [剑指 Offer 14- I. 剪绳子](https://leetcode-cn.com/problems/jian-sheng-zi-lcof/)

我对了，虽然感觉自己也不信，但是就是这么不可思议的一次过。

好吧看了题解发现我还是太菜了，数学推导的方法可以o(1)解决问题。

#### [剑指 Offer 10- II. 青蛙跳台阶问题](https://leetcode-cn.com/problems/qing-wa-tiao-tai-jie-wen-ti-lcof/)

经典的简单题(略)

#### [55. 跳跃游戏](https://leetcode-cn.com/problems/jump-game/)

两个思路，从前往后或从后往前，我的是从后往前，感觉代码比官方简单一点。

#### [62. 不同路径](https://leetcode-cn.com/problems/unique-paths/)

简单的2维dp，知识点在于如何优化空间复杂度

#### [322. 零钱兑换](https://leetcode-cn.com/problems/coin-change/)

应该是很熟的题，但居然再做的时候做错了。

#### [300. 最长上升子序列](https://leetcode-cn.com/problems/longest-increasing-subsequence/)

#### [312. 戳气球](https://leetcode-cn.com/problems/burst-balloons/)

（难）记忆化搜索:x:与动态规划:heavy_check_mark:。分治算法的思想。这题跟矩阵的维数最大乘积和有点相似。主要是要有从后往前的思想，从前往后的可能性太多了，从后往前就少了一些。还有就是附带了邻近的信息。然后是遍历顺序，其实可以写成斜着往右上角遍历，但是这样会变麻烦。

#### [64. 最小路径和](https://leetcode-cn.com/problems/minimum-path-sum/)

与[62. 不同路径](https://leetcode-cn.com/problems/unique-paths/)有些相似。

2020.07.23

### 设计问题

#### [剑指 Offer 59 - II. 队列的最大值](https://leetcode-cn.com/problems/dui-lie-de-zui-da-zhi-lcof/)

#### [剑指 Offer 41. 数据流中的中位数](https://leetcode-cn.com/problems/shu-ju-liu-zhong-de-zhong-wei-shu-lcof/)

#### [297. 二叉树的序列化与反序列化](https://leetcode-cn.com/problems/serialize-and-deserialize-binary-tree/)



### BFS/DFS

#### [332. 重新安排行程](https://leetcode-cn.com/problems/reconstruct-itinerary/)

本题和 [753. 破解保险箱](https://leetcode-cn.com/problems/cracking-the-safe/) 类似，是力扣平台上为数不多的求解欧拉回路 / 欧拉通路的题目。读者可以配合着进行练习。

我们化简本题题意：给定一个 n 个点 m	 条边的图，要求从指定的顶点出发，经过所有的边恰好一次（可以理解为给定起点的「一笔画」问题），使得路径的字典序最小。

#### [剑指 Offer 13. 机器人的运动范围](https://leetcode-cn.com/problems/ji-qi-ren-de-yun-dong-fan-wei-lcof/)

这题我拿BFS写的，如果下次再写可以用DFS写。注意读题，题目说的是每次只能移动一格。然后对于搜索范围是有一个优化的，但是我没考虑到。

#### [剑指 Offer 12. 矩阵中的路径](https://leetcode-cn.com/problems/ju-zhen-zhong-de-lu-jing-lcof/)

这题的特点是如何避免重复的访问之前访问的节点。

看了题解发现不需要额外创建visited数组存储是否访问过的状态。

判断是否找到了这样一条路径，如何用与或非来表示最终结果。

#### [785. 判断二分图](https://leetcode-cn.com/problems/is-graph-bipartite/)

这题作为练手熟悉dfs和bfs的写题模板很好用

#### [200. 岛屿数量](https://leetcode-cn.com/problems/number-of-islands/)

### 快慢指针法

#### [202. 快乐数](https://leetcode-cn.com/problems/happy-number/)

掌握快慢指针法的模板

### 位运算

#### [剑指 Offer 56 - I. 数组中数字出现的次数](https://leetcode-cn.com/problems/shu-zu-zhong-shu-zi-chu-xian-de-ci-shu-lcof/)

:cheese:想到是异或了，但是没想到怎么分组。是拓展思路的一题。

#### [剑指 Offer 56 - II. 数组中数字出现的次数 II](https://leetcode-cn.com/problems/shu-zu-zhong-shu-zi-chu-xian-de-ci-shu-ii-lcof/)

没想到不是异或，是统计二进制1出现的次数，由于除了一个数以外，其他数都出现了三次，所以统计每个位置1出现的次数，用三来取余就得到了最后的结果。

#### [剑指 Offer 16. 数值的整数次方](https://leetcode-cn.com/problems/shu-zhi-de-zheng-shu-ci-fang-lcof/)

:cheese:可以体会一下快速幂的实现方式，随便加深2进制和10进制互相转换的理解。

### 数学

#### [剑指 Offer 49. 丑数](https://leetcode-cn.com/problems/chou-shu-lcof/)

:cheese:理解，题解。每个丑数和235结合，又能产生新的丑数

#### [剑指 Offer 44. 数字序列中某一位的数字](https://leetcode-cn.com/problems/shu-zi-xu-lie-zhong-mou-yi-wei-de-shu-zi-lcof/)

解是解出来了代码有点丑陋。规律找到了，但不如题解的优雅。

#### [剑指 Offer 43. 1～n整数中1出现的次数](https://leetcode-cn.com/problems/1nzheng-shu-zhong-1chu-xian-de-ci-shu-lcof/)

hhh我做出来了，分析技巧在于分而治之，如何统计个位数的1，统计10位数的1，统计百位数的1。耐心分析，分析到百位数，基本就能掌握规律了。

#### [202. 快乐数](https://leetcode-cn.com/problems/happy-number/)

:cheese:涉及循环检测，重点在于思路，思考一直按照它的方法做下去会有哪几种情况。

#### [171. Excel表列序号](https://leetcode-cn.com/problems/excel-sheet-column-number/)

（再做）虽然简单，但我第一次的写法不是最优的。

#### [172. 阶乘后的零](https://leetcode-cn.com/problems/factorial-trailing-zeroes/)

（再做）虽然做了很多次，但每次重新做的时候会忘了怎么分析的

#### [69. x 的平方根](https://leetcode-cn.com/problems/sqrtx/)

（再做）思路：想方设法构建一个函数$f(x)$使得当$f(x)=0$时，求出题目要求的解。

#### [50. Pow(x, n)](https://leetcode-cn.com/problems/powx-n/)

快速幂

#### [29. 两数相除](https://leetcode-cn.com/problems/divide-two-integers/)

