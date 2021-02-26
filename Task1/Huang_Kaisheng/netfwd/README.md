## SRE Winter Assessment
Task-1.

### Summary

果然鸽子的下场就是两天半 851 行代码。(2.25 - 2.27)

已达成 Levels:
 - [x] level-0: TCP 端口转发
 - [x] level-1: http 分流转发
 - [ ] level-2: https 分流转发目前未实现，但可使用 TCP
 - [x] level-3: 客户端集成静态页面托管

额外特点:
 - [x] http 分流支持中文域名
 - [x] 使用 YAML 作为配置文件
 - [x] 面向对象程序设计，服务器客户端均使用类
 - [x] 使用二进制协议传输数据
 - [x] 支持多端口多用户转发
 - [x] Worker 架构

不足之处:
 - 错误处理不够好
 - 命令主程序面向对象化程度不足
 - 目测性能不够高
 - 不够稳定，偶尔出现卡死

### Screenshot
![运行截图](https://static.imvictor.tech/wp-content/uploads/2021/02/screenshot_assessment.png)


Code with ♥ by Victor Huang &lt;i@qwq.ren&gt;