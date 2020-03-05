# 更新历史 
- Feb. 03, 2020
  - 迁移目录到根，删除python3目录
  - 检索修改为移动端（对应：Mar. 18, 2019  ），修改解析规则
  - 修改测试url
- Apr. 23, 2019
* 修改代码部分单词错误。`arduino` -> `android`
  
* 增加.gitignore -> `*.mp4`
- Apr. 1, 2019  

  * 貌似增加了HTTPS，修改一下代码。（后来发现原来是开着Fidder的原因。不过既然代码改了就保留吧，反正不影响使用……）

  * 增加`urllib3.disable_warnings()`和`verify=False`

  * 测试url由 [卖茶女](http://v.douyin.com/FLBYQq) 的换成 [小姐姐](http://v.douyin.com/2EW6fW) 的


- Mar. 18, 2019  

  * 经@**steven7851** 提醒，下载UA换成移动端。检索UA仍为电脑端（懒得改……）。

  * 增加下载后自动播放功能，看反馈再看看是否要取消……


- Mar. 12, 2019   

  解析正常，下载失效


- Feb. 16, 2019  

  项目init  