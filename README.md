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
检查备案状态：

```
➜ python3 autoQuery.py

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

0  7  *  *  * cd /root/pkubeian && ./submit.sh  # 即每天早上7点运行, 自动提交备案申请，项目目录为/root/pkubeian，root身份运行，如果submit.sh权限不够，请chmod +x submit.sh
0  16  *  *  * cd /root/pkubeian && ./query.sh  # 即每天下午4点运行, 自动检查备案是否审核，项目目录为/root/pkubeian，root身份运行，如果query.sh权限不够，请chmod +x query.sh
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
	"gate": "燕园大厦门",        // 起点门
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
注意：默认从校内到校外，因为从校外到校内不能使用导师同意书，校外返校必须上传”北京健康宝“截图！使用时请注意！