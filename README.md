# py-search
	
## 项目介绍
    该项目通过python简单实现倒排索引存储。
    项目初衷是用于存储问答数据，便于对接问答系统。载入问答数据后，通过关键词搜索问题，获取问题答案。
## 项目功能
1. 读取问答数据并载入
2. 问答数据的增删改查
3. 已接入Flask，部署服务后可通过请求处理问答数据

## 基本原理
    通过对问题进行分词，将分词结果关联问答数据以字典形式存储(构建倒排索引); 搜索数据时，通过关键词查询数据记录id，通过数据记录id获取问答数据。

## 目录结构
py_search

- analyze **用于分词**

    analyzer.py 
	     
- data	**用于数据存放**

    py_search_data		数据文件

    py_search_index	索引文件

    py_search_map		映射文件

         
- dump	**用于持久化**

    dump.py
  
- handle  **用于数据处理(CRUD)**

    data.py

    index.py

    search.py
    
- test	**测试**

    test.py

- utils	**工具常量**

    constant.py

    util.py     
 
- web	**提供RESTFUL风格接口(待开发)**

## TODO
待优化完善
1. web启动时对索引及数据字典进行初始化，并兼容之前的初始化
2. 关键词模糊查询
3. 考虑数据字典大小超过阈值，创建新的数据字典文件


## 版本记录
v1.1.0
    1. 接入Flask，提供restful风格接口
v1.0.0
    1. 实现读取文件载入问答数据
    2. 实现问答数据基本增删改查