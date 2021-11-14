配合element一起用https://element.eleme.cn/#/zh-CN



单vue

```html
<!DOCTYPE html>
<html>
<head>
    <title></title>
</head>
<body>
    <div id="app">
        <table id="emp">
            <thead>
                <tr>
                    <th>编号</th>
                    <th>姓名</th>
                    <th>职位</th>
                    <th>工资</th>
                    <th>补贴</th>
                    <th>所在部门</th>
                </tr>
            </thead>
            <tbody>
                <!-- emps有多长，就会有多少行 -->
                <tr v-for="emp in emps">
                    <td>{{ emp.no }}</td>
                    <td>{{ emp.name }}</td>
                    <td>{{ emp.job }}</td>
                    <td>{{ emp.sal }}</td>
                    <td>{{ emp.comm }}</td>
                    <td>{{ emp.dept.name }}</td>
                </tr>
            </tbody>
        </table>
        <div id="page">

            <!-- <a id="prev" v-bind:href=prev>上一页</a>&nbsp;&nbsp;
            <a id="next" v-bind:href=next>下一页</a> -->
            <a id="prev" @click='prevPage()'>上一页</a>
            <a id="next" @click='nextPage()'>下一页</a>
        </div>
    </div>
    <script src="https://cdn.bootcdn.net/ajax/libs/vue/2.6.10/vue.min.js"></script>
    <script src="https://cdn.bootcdn.net/ajax/libs/element-ui/2.13.2/index.js"></script>
    <script>
        let pageSize = 5
        const app = new Vue({
            el: '#app',
            data: {
                emps: [],
                currentPage: 1,
                totalPage: 0,
                loading: true
            },
            created() {
                this.getEmpData()
            }.
            methods: {
                getEmpData() {
                    this.loading = true
                    const url = `.....`
                    fetch(url, {
                        headers: {}
                    })
                        .then(resp => resp.json())
                        .then(json => {
                            setTimeout(() => {
                                this.emps = json.results
                                this.totalPage = parseInt((json.count - 1) / pageSize)
                                this.loading = false
                            }, 500)
                        })
                }
                prevPage() {
                    if (this.currentPage > 1) {
                        this.currentPage -= 1
                        this.getEmpData()
                    }
                }
                nextPage() {
                    if (this.currentPage < this.totalPage) {
                        this.currentPage += 1
                        this.getEmpData()
                    }
                }
            }
        })
    </script>
</body>
</html>
```

vue + element

```html
<!DOCTYPE html>
<html>
<head>
    <title></title>
    <link href="https://cdn.bootcdn.net/ajax/libs/element-ui/2.13.2/theme-chalk/index.css" rel="stylesheet">
</head>
<body>
    <div id="app">
        <h1>员工信息表</h1>
        <hr>
        <el-table v-loading="loading" :data="emps" stripe style="width: 100%">
            <el-table-column prop="no" label="编号" width="180"></el-table-column>
            <el-table-column prop="name" label="姓名" width="180"></el-table-column>
            <el-table-column prop="job" label="职位"></el-table-column>
            <el-table-column prop="sal" label="工资"></el-table-column>
            <el-table-column prop="comm" label="补贴"></el-table-column>
            <el-table-column prop="dept.name" label="所在部门"></el-table-column>
        </el-table>
        <div id="page">

            <!-- <a id="prev" v-bind:href=prev>上一页</a>&nbsp;&nbsp;
            <a id="next" v-bind:href=next>下一页</a> -->
            <a id="prev" @click='prevPage()'>上一页</a>
            <a id="next" @click='nextPage()'>下一页</a>
        </div>
    </div>
    <script src="https://cdn.bootcdn.net/ajax/libs/vue/2.6.10/vue.min.js"></script>
    <script src="https://cdn.bootcdn.net/ajax/libs/element-ui/2.13.2/index.js"></script>
    <script>
        let pageSize = 5
        const app = new Vue({
            el: '#app',
            data: {
                emps: [],
                currentPage: 1,
                totalPage: 0,
                loading: true
            },
            created() {
                this.getEmpData()
            }.
            methods: {
                getEmpData() {
                    this.loading = true
                    const url = `.....`
                    fetch(url, {
                        headers: {}
                    })
                        .then(resp => resp.json())
                        .then(json => {
                            setTimeout(() => {
                                this.emps = json.results
                                this.totalPage = parseInt((json.count - 1) / pageSize)
                                this.loading = false
                            }, 500)
                        })
                }
                prevPage() {
                    if (this.currentPage > 1) {
                        this.currentPage -= 1
                        this.getEmpData()
                    }
                }
                nextPage() {
                    if (this.currentPage < this.totalPage) {
                        this.currentPage += 1
                        this.getEmpData()
                    }
                }
            }
        })
    </script>
</body>
</html>
```

echarts

https://echarts.apache.org/zh/tutorial.html#5%20%E5%88%86%E9%92%9F%E4%B8%8A%E6%89%8B%20ECharts

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>ECharts</title>
    <!-- 引入 echarts.js -->
    <script src="https://cdn.bootcdn.net/ajax/libs/echarts/5.0.0-alpha.1/echarts.common.min.js"></script>
</head>
<body>
    <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
    <div id="main" style="width: 600px;height:400px;margin: 0 auto;border: 1px solid;padding: 100px;"></div>
    <script type="text/javascript">
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('main'));

        // 指定图表的配置项和数据
        var option = {
            title: {
                text: 'ECharts 入门示例'
            },
            tooltip: {},
            legend: {
                data:['销量']
            },
            xAxis: {
                data: ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
            },
            yAxis: {},
            series: [{
                name: '销量',
                type: 'bar',
                data: [5, 20, 36, 10, 10, 20]
            }]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    </script>
</body>
</html>
```

bootstrap

https://www.bootcss.com/

https://www.bootcss.com/p/layoutit/ 可视化布局

```html

```

