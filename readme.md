FlappyBird
===============

​	本项目设计并实现了基于Python中的Pygame和Tkinter实现的FlappyBird游戏，游戏中利用Pygame模块来实现游戏核心部分，包括游戏中角色的移动、障碍物的移动、玩家与游戏之间的交互，以及获取金币增加得分等功能，而游戏的登入界面则采用Tkinter模块进行设计，记录玩家的用户名以及分数。最终实现的FlappyBird游戏主要以清新简单的画面风格呈现，可以通过用户按键对游戏角色“小鸟”进行控制飞行来躲避障碍物“管道”和吃取游戏中随机出现的“金币”来获得分数，当“小鸟”与“管道”碰撞时则游戏结束，用户的得分将会被刊登在排行榜上。

如何运行？(以windows10 x64为例)
---------------------------

1. 安装python 3.x或者python 2.x。(推荐使用python 3.x及以上版本) [下载](https://www.python.org/downloads/)

2. 安装pip [下载](https://bootstrap.pypa.io/get-pip.py)

3. 安装pygame

   运行-cmd命令行，在命令行中输入

   ```bash
   pip install pygame
   ```

   如果由于网络原因安装失败或者速度过慢，可以改为输入：

   ```bash
   pip install pygame -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

   以上是采用清华大学的镜像源安装pygame。

   如果依然无法安装，可以尝试更换镜像源。

   阿里云：http://mirrors.aliyun.com/pypi/simple/

   中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple/

   华中理工大学：http://pypi.hustunique.com/

   山东理工大学：http://pypi.sdutlinux.org/ 

   豆瓣：http://pypi.douban.com/simple/

   将-i后面的链接替换为相应镜像源的链接即可。

4. 运行源文件中的teamwork_flappybird.py

   5.使用 <kbd>&uarr;</kbd> 键或者 <kbd>Space</kbd> 键 来控制小鸟飞行，按 <kbd>Esc</kbd> 键退出游戏

相关项目
-------------

- [FlapPyBird](https://github.com/sourabhv/FlapPyBird)

  该项目参考以上项目开发，对原作者表达感谢与敬意。


项目维护者信息
----------

李海鹏：ariharasuzune009@gmail.com

