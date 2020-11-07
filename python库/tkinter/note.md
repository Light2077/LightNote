self 是tk.Tk

### 可以通过改变var，间接改变label的值
var = tkinter.stringVar()
var.set('hello')
var.get()

### 实现拷贝到剪贴板功能
self.clipboard_clear()
self.clipboard_append(text)

### 菜单功能
https://blog.csdn.net/qq_41556318/article/details/85273584

```python
# 新建一个菜单
self.menu = tk.Menu(self, bg="yellow", fg="lightgrey")
# 在这菜单之上增加一个选单
self.languages_menu = tk.Menu(self.menu, tearoff=1, bg="yellow", fg="black")
# 纵向添加
self.languages_menu.add_command(label="Portuguese", command=self.add_portuguese_tab)
# 横向添加
self.menu.add_cascade(label="Languages", menu=self.languages_menu)
# 把这个菜单设为窗体的总菜单
self.config(menu=self.menu)

...
# 把某个label设置为不活跃状态
# readonly只读？
self.languages_menu.entryconfig("Portuguese", state="disabled")
```
- 本质上是一堆Button的列表
- 参数tearoff=0, 使用户不能拖拽这个菜单，如果tearoff=1，可以把这个菜单变成一个单独小窗

### 捕获错误的好习惯
```python
try:
	...
except Exception as e:
    msg.showerror("Translation Failed", str(e))
else:
	...
```

### 获得上一级窗口
root = self.winfo_toplevel()

### 焦点设置
self.focus_set()