# ArknightsDamageCurve-明日方舟伤害曲线模拟器

 A simple *python* script to generate damage curve for game **Arknights**
 
 一个简单的python代码，用于生成300秒内各个干员的期望伤害的时间曲线
 
  数据和影像资源全部来自于游戏本体，如遇版权问题，可能随时删除（我猜这玩意儿应该遇不上版权问题<img src="enemy/扇子脸.png" width="60">）

## 环境配置
* 需要 [*Python*](https://www.python.org/)。理论上这份代码需要 *Python >= 3.6*，但我只在 *Python 3.7* 上测试过。
* 需要 [*matplotlib*](https://matplotlib.org/) >= 3.0 <br> Windows, Mac 和 Linux 均可通过 [pip](https://pypi.org/project/pip/) 安装*matplotlib*

	```
	python -m pip install -U pip 
	python -m pip install -U matplotlib
	```
* 需要 [思源黑体](https://github.com/adobe-fonts/source-han-sans) *字体*  <br> *matplotlib* 需要 TrueTypeFont (TTF) 文件, 但源文件没有TTF版本。所以我附带了一份我自己转换的 `SourceHanSansSC-Normal.ttf`
* 需要配置 *matplotlib* 来让它支持中文字体 <br> 你可以在知乎问题 [https://www.zhihu.com/question/25404709](https://www.zhihu.com/question/25404709) 里找到 Windows 和 Mac 中的 *matplotlib* 的中文配置方法

## 用法
1. <font color=brown>**简单用法：**</font>通过运行 `main.py` 来生成默认的一系列伤害曲线图
	* `python main.py`，当然你也可以在IDE里运行
	* 运行后会生成一系列的图片，包括了5种在高难合约里常见的干员组合面对各种敌人时的输出期望曲线
	* 预设的角色组合如下:
<table><tr><th>组合</th><th colspan="3">角色</th></tr>
	<tr> <td rowspan="2">Melee Physical<br>近战物理干员</td> <td>煌</td> <td>赫拉格</td> <td>陈</td> </tr>
	<tr> <td>银灰 (3)</td> <td></td> <td></td> </tr>
	<tr> <td rowspan="2">Melee Magic<br>近战法术干员</td> <td>陈 (2)</td> <td>布洛卡 (2)</td> <td>星极</td> </tr>
	<tr> <td>拉普兰德 (2)</td> <td>慕斯</td> <td></td> </tr>
	<tr> <td rowspan="2">Ranged Physical<br>高台物理干员</td> <td>黑 (2,3)</td> <td>能天使 (2,3)</td> <td>送葬人</td> </tr>
	<tr> <td>陨星</td> <td>蓝毒</td> <td></td> </tr>
	<tr> <td rowspan="1">Ranged Magic<br>高台法术干员</td> <td>安洁莉娜</td> <td>艾雅法拉</td> <td>伊芙利特</td> </tr>	<tr> <td rowspan="2">Control<br>控制队干员</td> <td>安洁莉娜 (2,3)</td> <td>莫斯提马 (2)</td> <td>格劳克斯 (2)</td> </tr>
	<tr> <td>食铁兽</td> <td>狮蝎 (1)</td> <td>伊桑 (2)</td></tr>
</table>

2. <font color=brown>**进阶用法：**</font>通过运行 `plot.py ` 来生成你自己想要的伤害曲线图，但你需要进行一些参数的设置
	* 修改 `plot.py` 中的参数，主要在 `__main__` 函数部分。你可以参考 `plot.py` 中的一些预设的参数
	* 在 `plot.plot(...)` 你可以看到更多的关于参数的注释
	  
3. 过一段时间会增加更多的介绍，包括假想敌的设置、更具体的用法、参数介绍、例子说明等 <del>在做了咕咕咕咕咕咕</del>


## Requirements
* Requires *Python*. In theory this code can be run on *Python >= 3.6*, but I only test this code in *Python 3.7*
* Requires [*matplotlib*](https://matplotlib.org/) >= 3.0. <br> Both Windows, Mac and Linux can install *matplotlib* from [pip](https://pypi.org/project/pip/)

	```
	python -m pip install -U pip 
	python -m pip install -U matplotlib
	```
* Requires *Font* [思源黑体](https://github.com/adobe-fonts/source-han-sans). <br> *matplotlib* requires TrueTypeFont file, but the source file does not provide a TTF version. So I provide a converted version `SourceHanSansSC-Normal.ttf` in the repo.
* You also need to configure your *matplotlib* to make it support Chinese font. <br> You may check [https://www.zhihu.com/question/25404709](https://www.zhihu.com/question/25404709), where both Mac and Windows can find instructions for setting Chinese font.

## Usage
1. <font color=brown>**Simple usage:**</font> To generate default damage curve images, run:
	* `python main.py`, or run the code in your IDE
	* It will automatically generate a series of images, containing the damage curves for some most commonly used characters.
	* Default characters are listed below:
<table><tr><th>Group</th><th colspan="3">Characters</th></tr>
	<tr> <td rowspan="2">Melee Physical</td> <td>Blaze</td> <td>Hellagur</td> <td>Ch'en</td> </tr>
	<tr> <td>Silver Ash (3)</td> <td></td> <td></td> </tr>
	<tr> <td rowspan="2">Melee Magic</td> <td>Ch'en (2)</td> <td>Broca (2)</td> <td>Astesia</td> </tr>
	<tr> <td>Lappland (2)</td> <td>Mousse</td> <td></td> </tr>
	<tr> <td rowspan="2">Ranged Physical</td> <td>Schwarz (2,3)</td> <td>Exusiai (2,3)</td> <td>Executor</td> </tr>
	<tr> <td>Meteorite</td> <td>Blue Poisson</td> <td></td> </tr>
	<tr> <td rowspan="1">Ranged Magic</td> <td>Angelina</td> <td>Eyjafjalla</td> <td>Ifrit</td> </tr>
	<tr> <td rowspan="2">Control</td> <td>Angelina (2,3)</td> <td>Mostima (2)</td> <td>Glaucus (2)</td> </tr>
	<tr> <td>FEater</td> <td>Manticore (1)</td> <td>Ethan (2)</td></tr>
</table>

2. <font color=brown>**More usages:**</font> To generate customized damage curve, you need to:
	* Change parameters in `plot.py`. There are some preset parameters in `plot.py`
	* You can see more description of those parameters in the comment of `plot.plot(...)`
	  
3. More descriptions will be added in the future
  