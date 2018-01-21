# 001 
download backgrounds from Bing as your desktop wallpaper

测试环境：windows 10, python 3.6.4

### 设置随系统启动而运行
1. Win+x -> 计算机管理
2. 任务计划程序
3. 创建基本任务

PS: 设置“启动程序”时，需要将“起始于”项配置为与程序在同一个目录

### reference
1. [SystemParametersInfo function](https://msdn.microsoft.com/en-us/library/windows/desktop/ms724947(v=vs.85).aspx)
2. [SPIF (Enums)](http://www.pinvoke.net/default.aspx/Enums/SPIF.html)
3. [Creating a background changer in python with ctypes, not working](https://stackoverflow.com/questions/21715895/creating-a-background-changer-in-python-with-ctypes-not-working)
4. [Change Windows Background from Python](https://stackoverflow.com/questions/16943733/change-windows-background-from-python)
5. [Windows 任务计划程序操作之起始于](http://blog.csdn.net/vic0228/article/details/61914425)
