# async_pt

异步项目工具，需根据实际api开发过程中的需求不断完善

# 包含内容

- 读取配置文件：默认读取`.env`，通过环境变量`CONFIG_FILE`控制
- 写日志：3种log handler：1- 输出到文件、输出到控制台、ddp输出到graylog，3个handler可以同时开启
- 异步es：异步连接、查询、关闭连接等功能


- 异步SQLAlchemy
- 异步mongo
- 异步redis
- fastapi response format
- try cache