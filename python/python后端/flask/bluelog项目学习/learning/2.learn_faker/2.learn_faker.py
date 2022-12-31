from faker import Faker
fake = Faker('zh-cn')

print('单词:', fake.word())
print('一句话:', fake.sentence())
print('指定字符数量的一段话:', fake.text())
print('时间戳:', fake.date_time_this_year())

print('姓名:', fake.name())
print('邮箱:', fake.email())
print('链接:', fake.url())
