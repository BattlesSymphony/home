## 列表
```bash
# 在列表左边/右边添加一个元素
lpush/rpush mylist "imooc.com"

# 查看列表元素
lrange mylist 0 10

# key是列表名
# 从列表的左侧/右侧删除一个元素
blpop/brpop key1 [keys2] timeout
# 和上面一样都是删除操作 不用传timeout 
lpop/rpop key
# 列表长度
llen key
# 获取列表的第几个元素
lindex key index
```


```bash
lpush imooc_courses "scrapy"
lpush imooc_courses "django"

lrange imooc_courses 0 10
rpush imooc_courses "scrapy-redis"

# imooc_courses = ['django', 'scrapy', 'scrapy-redis']
# blpop 会删除列表imooc_courses最左面的元素
blpop imooc_courses 3
lpush imooc_courses "django"
brpop imooc_courses 3
```

## 集合 不重复
```bash
# 添加元素
sadd myset "imooc.com"
# 查看所有元素
smembers key
# 获取集合长度
scard key
# 两个set 取第一个集合中和第二个集合中 不同的
example: course1 django       course2 scrapy
		  	     scrapy 			  scrapy-redis
sdiff key1 [key2]
sdiff course1 course2 得到的结果是 django

# 两个set 取交集
sinter key1 [key2]
example:
sinter course1 course2 得到的结果是 scrapy

# 从里面随机删除一个元素， 并把这个元素返回回来
spop key

# 随机在列表中 获取 member 个 数据
srandmember key member
example: srandmember course1 10 
```

```bash
sadd course_set "django"
sadd course_set "django"
sadd course_set "scrapy"

```

## 可排序集合
```bash
zadd myset 0 "project" [1 "imooc.com"]
example:
ZADD zcourse_set 0 "django" 1 "scrapy" 5 "scrapy-redis"

# 获取分数在0-100的所有的元素
zrangebyscore myset 0 100
example:
ZRANGE zcourse_set 0 1
ZRANGE zcourse_set 1 5

# 获取分数在 min-max的所有元素的数量
zcount key min max
zcount zcourse_set 1 5
```

## redis 文档推荐
1. redis 教程
2. redis 命令参考