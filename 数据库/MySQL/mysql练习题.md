DROP TABLE IF EXISTS user_log;
CREATE TABLE user_log(
id int,
uid int,
equipment_id int,
start_time datetime null,
end_time datetime null,
ip int
);

insert into user_log values
(1, 632251001, 86900199, '2022-07-02 06:01:01', '2022-07-02 06:21:01', 80),
(2, 632251002, 86900199, '2022-06-05 19:01:01', '2022-06-05 19:40:01', 81),
(3, 632251002, 86900299, '2022-06-02 12:01:01', NULL, NULL),
(4, 632251002, 86900399, '2022-06-01 12:01:01', NULL, NULL),
(5, 632251002, 86900199, '2022-07-02 19:01:01', '2022-07-02 19:30:01', 82),
(6, 632251002, 86900299, '2022-07-05 18:01:01', '2022-07-05 18:59:02', 90),
(7, 632251003, 86900299, '2022-07-06 12:01:01', NULL, NULL),
(8, 632251003, 86900399, '2022-06-07 10:01:01', '2022-06-07 10:31:01', 86),
(9, 632251004, 86900399, '2022-06-06 12:01:01', NULL, NULL),
(10, 632251002, 86900399, '2022-06-01 12:01:01', '2022-06-01 12:31:01', 81),
(11, 632251005, 86900199, '2022-06-01 12:01:01', '2022-06-01 12:31:01', 88),
(12, 632251005, 86900299, '2022-06-01 12:01:01', '2022-06-01 12:31:01', 88),
(13, 632251006, 86900299, '2022-06-02 12:11:01', '2022-06-02 12:31:01', 89)


DROP TABLE IF EXISTS equipment_info;
CREATE TABLE equipment_info(
id int,
equipment_id int,
tag VARCHAR(20)
);

insert into equipment_info values
(1, 86900199, '小米'),
(2, 86900299, '华为'),
(3, 86900399, '苹果')



-- 请统计每个登录未下线次数大于1的有效用户的数据（有效用户指有完整上下线时间登录的次数至少为1），输出用户ID、登录未下线次数、完整上下线登录次数、登录的tag集合，按登录未下线次数由多到少排序。
-- 开发环境：hive/mysql
-- 要求：请通过代码实现题目，过程中的输入输出处理方式请参考题目输入输出描述，注意代码缩进

SELECT 
t1.uid,
sum( case when t1.end_time is NULL then 1 ELSE 0 END) 登录未下线次数,
sum( case when t1.ip is NOT NULL then 1 ELSE 0 END) 完整上下线登录次数,
GROUP_CONCAT(distinct t2.tag) tag集合
FROM user_log t1 join equipment_info t2 on t1.equipment_id = t2.equipment_id
group by t1.uid
order by 登录未下线次数 desc





import numpy as np y = np.array([1, 0, 0]) y_pred = np.array([0.5, 0.2, 0.3]) ans = - np.sum(y * np.log(y_pred)) / len(y)