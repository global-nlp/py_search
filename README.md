# py-search
	通过python简单实现倒排索引存储

# 目录结构
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

# TODO
待优化完善

1.读取文件加载问答对进行批量添加

2.关键词模糊查询

3.web接口开发

4.考虑数据字典大小超过阈值，创建新的数据字典文件