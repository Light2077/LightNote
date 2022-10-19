## 学习之前

- 怎么学
- 如何安装
- 第一个页面，如何定制这个页面
- 文件组织结构



怎么学：

官方教程：https://cn.vuejs.org/guide/introduction.html

菜鸟教程：https://www.runoob.com/vue3/vue3-tutorial.html



我先阅读了官方教程的[简介](https://cn.vuejs.org/guide/introduction.html)和[互动教程](https://cn.vuejs.org/tutorial/#step-1)，然后发现继续往下阅读时有些许困难，就开始阅读菜鸟教程。

最开始遇到的疑问

- 怎么创建vue项目
- 初始化vue项目后，里面的各个文件的作用是什么
- 怎么修改初始页面

菜鸟教程的[创建项目](https://www.runoob.com/vue3/vue3-create-project.html)和[目录结构](https://www.runoob.com/vue3/vue3-directory-structure.html)很好地解决了这些疑问。



主要的操作在src文件夹下，直接修改`App.vue`

以下内容是基于官方的[互动教程](https://cn.vuejs.org/tutorial/#step-1)整理所得

## 快速上手

主要结构

传递变量

```vue
<script>
export default {
  data() {
    return {
      test_class: 'test_class_name'
    }
  }
}
</script>
```

传递函数

```vue
<script>
methods: {
  onInput(e) {
    this.text = e.target.value
  }
}
</script>
```



绑定属性

```vue
<div :class="test_class">...</div>
```

绑定事件

```vue
<div @click="event_function">...</div>
```

绑定表单

```vue
<input :value="text" @input="onInput">
```

简写

```vue
<input v-model="text">
```

相当于把input的value属性绑定text变量上





### 声明式渲染

- 单文件组件(Single-File Component, SFC)

SFC的目的是高复用，等于说项目是一个大城堡的乐高积木，SFC就封装了一个小房间，可以到处拿去拼接。



在script标签中export一些变量

要定义一个名为`data()`的函数，然后在这个函数里返回一些变量

就可以在template标签中显示了。





### Attribute绑定

可以用`v-bind`绑定属性

```vue
<div v-bind:id="dynamicId"></div>
```

元素的 `id` 属性将与组件状态里的 `dynamicId` 属性保持同步。

简写语法

```vue
<div :id="dynamicId"></div>
```

示例

```vue
<script>
export default {
  data() {
    return {
      titleClass: 'title'
    }
  }
}
</script>

<template>
  <h1 :class="titleClass">Make me red</h1>
</template>

<style>
.title {
  color: red;
}
</style>
```

语法

```
v-bind:属性名="变量名"
```

### 事件监听

可以使用`v-on`指令监听DOM事件

```vue
<button v-on:click="increment">{{ count }}</button>
<button @click="increment">{{ count }}</button>
```

当按钮被点击时，触发increment这个函数

函数要放在`methods`选项下

### 表单绑定

同时使用属性绑定和时间监听

```js
<input :value="text" @input="onInput">
```

```js
methods: {
  onInput(e) {
    // v-on 处理函数会接收原生 DOM 事件
    // 作为其参数。
    this.text = e.target.value
  }
}
```

简化双向绑定，是上述操作的语法糖，不必再实现事件处理函数了。

相当于把input的value属性绑定text变量上

```js
<input v-model="text">
```

```vue
<script>
export default {
  data() {
    return {
      text: ''
    }
  }
}
</script>

<template>
  <input v-model="text" placeholder="Type here">
  <p>{{ text }}</p>
</template>
```

### 条件渲染

我们可以使用 `v-if` 指令来有条件地渲染元素：

```vue
<h1 v-if="awesome">Vue is awesome!</h1>
```

这个 `<h1>` 标签只会在 `awesome` 的值为[真值 (Truthy)](https://developer.mozilla.org/zh-CN/docs/Glossary/Truthy) 时渲染。若 `awesome` 更改为[假值 (Falsy)](https://developer.mozilla.org/zh-CN/docs/Glossary/Falsy)，它将被从 DOM 中移除。

我们也可以使用 `v-else` 和 `v-else-if` 来表示其他的条件分支：

```vue
<h1 v-if="awesome">Vue is awesome!</h1>
<h1 v-else>Oh no 😢</h1>
```

现在，示例程序同时展示了两个 `<h1>` 标签，并且按钮不执行任何操作。尝试给它们添加 `v-if` 和 `v-else` 指令，并实现 `toggle()` 方法，让我们可以使用按钮在它们之间切换。

```vue
<script>
export default {
  data() {
    return {
      awesome: true
    }
  },
  methods: {
    toggle() {
      this.awesome = !this.awesome
    }
  }
}
</script>

<template>
  <button @click="toggle">toggle</button>
  <h1 v-if="awesome">Vue is awesome!</h1>
  <h1 v-else>Oh no 😢</h1>
</template>	
```

### 列表渲染

我们可以使用 `v-for` 指令来渲染一个基于源数组的列表：

```js
<ul>
  <li v-for="todo in todos" :key="todo.id">
    {{ todo.text }}
  </li>
</ul>

```

更新列表的方法

1.在源数组上调用[变更方法](https://stackoverflow.com/questions/9009879/which-javascript-array-functions-are-mutating)：

```js
this.todos.push(newTodo)
```

2.使用新的数组替代原数组：

```js
this.todos = this.todos.filter(/* ... */)
```

案例

```js
<script>
// 给每个 todo 对象一个唯一的 id
let id = 0

export default {
  data() {
    return {
      newTodo: '',
      todos: [
        { id: id++, text: 'Learn HTML' },
        { id: id++, text: 'Learn JavaScript' },
        { id: id++, text: 'Learn Vue' }
      ]
    }
  },
  methods: {
    addTodo() {
      this.todos.push({ id: id++, text: this.newTodo })
      this.newTodo = ''
    },
    removeTodo(todo) {
      this.todos = this.todos.filter((t) => t !== todo)
    }
  }
}
</script>

<template>
  <form @submit.prevent="addTodo">
    <input v-model="newTodo">
    <button>Add Todo</button>    
  </form>
  <ul>
    <li v-for="todo in todos" :key="todo.id">
      {{ todo.text }}
      <button @click="removeTodo(todo)">X</button>
    </li>
  </ul>
</template>
```

### 计算属性

https://cn.vuejs.org/tutorial/#step-8

用到`computed`

```js
<script>
let id = 0

export default {
  data() {
    return {
      newTodo: '',
      hideCompleted: false,
      todos: [
        { id: id++, text: 'Learn HTML', done: true },
        { id: id++, text: 'Learn JavaScript', done: true },
        { id: id++, text: 'Learn Vue', done: false }
      ]
    }
  },
  computed: {
    filteredTodos() {

      if (this.hideCompleted) {
        return this.todos.filter((t) => !t.done)
      } else {
        return this.todos
      }
    }
    
  },
  methods: {
    addTodo() {
      this.todos.push({ id: id++, text: this.newTodo, done: false })
      this.newTodo = ''
    },
    removeTodo(todo) {
      this.todos = this.todos.filter((t) => t !== todo)
    }
  }
}
</script>

<template>
  <form @submit.prevent="addTodo">
    <input v-model="newTodo">
    <button>Add Todo</button>
  </form>
  <ul>
    <li v-for="todo in filteredTodos" :key="todo.id">
      <input type="checkbox" v-model="todo.done">
      <span :class="{ done: todo.done }">{{ todo.text }}</span>
      <button @click="removeTodo(todo)">X</button>
    </li>
  </ul>
  <button @click="hideCompleted = !hideCompleted">
    {{ hideCompleted ? 'Show all' : 'Hide completed' }}
  </button>
</template>

<style>
.done {
  text-decoration: line-through;
}
</style>
```

### 生命周期和模板引用

目前为止，Vue 为我们处理了所有的 DOM 更新，这要归功于响应性和声明式渲染。然而，有时我们也会不可避免地需要手动操作 DOM。

这时我们需要使用**模板引用**——也就是指向模板中一个 DOM 元素的 ref。我们需要通过[这个特殊的 `ref` attribute](https://cn.vuejs.org/api/built-in-special-attributes.html#ref) 来实现模板引用：

```vue
<p ref="p">hello</p>
```

此元素将作为 `this.$refs.p` 暴露在 `this.$refs` 上。然而，你只能在组件**挂载**之后访问它。

要在挂载之后执行代码，我们可以使用 `mounted` 选项：

js

```vue
<script>
export default {
  mounted() {
    // 此时组件已经挂载。
  }
}
</script>
```

这被称为**生命周期钩子**——它允许我们注册一个在组件的特定生命周期调用的回调函数。还有一些其他的钩子如 `created` 和 `updated`。更多细节请查阅[生命周期图示](https://cn.vuejs.org/guide/essentials/lifecycle.html#lifecycle-diagram)。



```js
<script>
export default {
  mounted() {
    this.$refs.p.textContent = '是'
  },
  methods:  {
    change(e) {
      this.$refs.p.textContent == '是' ? 
        this.$refs.p.textContent = '否' : 
        this.$refs.p.textContent = '是'
      // this.$refs.p.textContent = '否'
    }
  }
}
</script>

<template>
  <p ref="p">hello</p>
  <button @click="change">
    click
  </button>
</template>
```

### 侦听器

有时我们需要响应性地执行一些“副作用”——例如，当一个数字改变时将其输出到控制台。我们可以通过侦听器来实现它：

```js
<script>
export default {
  data() {
    return {
      todoId: 1,
      todoData: null
    }
  },
  methods: {
    async fetchData() {
      this.todoData = null
      const res = await fetch(
        `https://jsonplaceholder.typicode.com/todos/${this.todoId}`
      )
      this.todoData = await res.json()
    }
  },
  mounted() {
    this.fetchData()
  },
  watch: {
    todoId() {
      this.fetchData()
    }
  }
}
</script>

<template>
  <p>Todo id: {{ todoId }}</p>
  <button @click="todoId++">Fetch next todo</button>
  <p v-if="!todoData">Loading...</p>
  <pre v-else>{{ todoData }}</pre>
</template>
```

这里，我们使用 `watch` 选项来侦听 `count` 属性的变化。当 `count` 改变时，侦听回调将被调用，并且接收新值作为参数。更多详情请参阅[指南——侦听器](https://cn.vuejs.org/guide/essentials/watchers.html)。

一个比在控制台输出更加实际的例子是当 ID 改变时抓取新的数据。在右边的例子中就是这样一个组件。该组件被挂载时，会从模拟 API 中抓取 todo 数据，同时还有一个按钮可以改变要抓取的 todo 的 ID。现在，尝试实现一个侦听器，使得组件能够在按钮被点击时抓取新的 todo 项目。



> 这里的count是定义在data中的变量。



### 组件

目前为止，我们只使用了单个组件。真正的 Vue 应用往往是由嵌套组件创建的。

父组件可以在模板中渲染另一个组件作为子组件。要使用子组件，我们需要先导入它：



```js
import ChildComp from './ChildComp.vue'

export default {
  components: {
    ChildComp
  }
}
```

我们还需要使用 `components` 选项注册组件。这里我们使用对象属性的简写形式在 `ChildComp` 键下注册 `ChildComp` 组件。

然后我们就可以在模板中使用组件，就像这样：



```js
<ChildComp />
```



现在自己尝试一下——导入子组件并在模板中渲染它。

### Props

子组件可以通过 **props** 从父组件接受动态数据。首先，需要声明它所接受的 props：

```js
// 在子组件中
export default {
  props: {
    msg: String
  }
}
```

一旦声明，`msg` prop 就会暴露在 `this` 上，并可以在子组件的模板中使用。

父组件可以像声明 HTML attributes 一样传递 props。若要传递动态值，也可以使用 `v-bind` 语法：

template

```js
<ChildComp :msg="greeting" />
```

案例

```js
<script>
import ChildComp from './ChildComp.vue'

export default {
  components: {
    ChildComp
  },
  data() {
    return {
      greeting: 'Hello from parent'
    }
  }
}
</script>

<template>
  <ChildComp :msg="greeting" />
</template>
```

### Emits

除了接收 props，子组件还可以向父组件触发事件：



```js
export default {
  // 声明触发的事件
  emits: ['response'],
  created() {
    // 带参数触发
    this.$emit('response', 'hello from child')
  }
}
```

`this.$emit()` 的第一个参数是事件的名称。其他所有参数都将传递给事件监听器。

父组件可以使用 `v-on` 监听子组件触发的事件——这里的处理函数接收了子组件触发事件时的额外参数并将它赋值给了本地状态：

template

```js
<ChildComp @response="(msg) => childMsg = msg" />
```

### 插槽

相当于模板的默认设置

除了通过 props 传递数据外，父组件还可以通过**插槽** (slots) 将模板片段传递给子组件：

template

```vue
<ChildComp>
  This is some slot content!
</ChildComp>
```



在子组件中，可以使用 `<slot>` 元素作为插槽出口 (slot outlet) 渲染父组件中的插槽内容 (slot content)：

template

```vue
<!-- 在子组件的模板中 -->
<slot/>
```



`<slot>` 插口中的内容将被当作“默认”内容：它会在父组件没有传递任何插槽内容时显示：

template

```vue
<slot>Fallback content</slot>
```