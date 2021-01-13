# PKU新版本出入校自动报备

# Dependency

```
pip3 install requests
```

# Usage
一次性直接运行（只运行一次）：

```
➜ python3 autoSubmitter.py

```

添加定时任务（每天自动运行）：

这里以linux系统的crontab为例，这里来一个crontab的配置demo:
terminal运行 `crontab -e`编辑任务，如下：
```
SHELL=/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root

# For details see man 4 crontabs

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name  command to be executed

0  7  *  *  * cd /root/pkubeian && ./start.sh  # 即每天早上7点运行, 项目目录为/root/pkubeian，root身份运行，如果start.sh权限不够，请chmod +x start.sh
```

然后加载任务
```
crontab /etc/crontab
```

# 配置文件说明
请手动修改config.json为自己的信息，参数说明如下：

```
{
	"username": "1901xxxxxx",    // 学号
	"password": "xxxxxxxxxx",    // 校园门户密码
	"gate": "燕园大厦门",        // 终点门（默认从校外到燕园（感觉这个方向影响不大））
	"email": "xxxxxx@pku.edu.cn",// 邮箱
	"phone": "xxxxxxxx",         // 手机号
	"reason": "科研",            // 出入校事由：就业、学业、科研、就医、寒假离校返乡，五选一别写错了
	"street": "中关村街道",      // 所在的街道，脚本默认海淀区，要改的自己抓包改
	"route": "中关村-燕园大厦",  // 行动轨迹
	"desc": "去实验室",          // 出入校具体事项
	"file": "./bjjkb.jpg",       // 证明材料
	"file_type": 1,              // 证明文件类型：健康宝写1，导师同意书写2，建议搞一个导师同意书
				     //	因为健康宝【可能】要每天截图
	"wechat_key": "xxxxxxxxxx"   //  微信推送key，在 http://sc.ftqq.com/3.version 获取，可以没有
}
```
