# 统计学习方法 ----Chapter1：统计学习方法概论

## 1.1 统计学习

（1）统计学习关于数据的夹假设是同类数据具有一定的统计规律性。统计学习包括监督学习，非监督学习，半监督学习，和强化学习。

（2）统计学习方法的三要素：假设空间（**模型**），模型选择的准则（**策略**），模型学习的算法（**算法**）。

## 1.2 监督学习

（1）监督学习的任务时学习一个模型，使模型能够对任意给定的输入，对其相对应的输出作出一个好的预测。监督学习中，假设训练数据与测试数据是依联合概率![](http://latex.codecogs.com/gif.latex?P(X,Y))独立同分布产生的

（2）输入变量与输出变量均为连续变量的预测问题称为**回归问题** ；输出变量为有限个离散变量的预测问题称为**分类问题**；输入变量与输出变量均为变量序列的预测问题称为**标注问题**。

## 1.3 统计学习三要素

### 1.3.1 模型

​	在监督学习中，模型就是所要学习的条件概率分布或决策函数。模型的假设空间包含所有可能的条件概率分布或决策函数。如，假设决策函数是输入变量的线性函数，那么模型的假设空间就是所有这些线性函数构成的组合。

​	假设空间用F表示。假设空间可以定义为决策函数的集合（非概率模型）：

<div align=center><img " src="http://latex.codecogs.com/gif.latex?F=\{f|Y=f(X)\}"/></div>

	其中，X和Y是定义在输入空间和输出空间上的变量，这时F通常是由一个参数向量决定的函数簇：
<div align=center><img " src="http://latex.codecogs.com/gif.latex?F=\{f|Y=f_{\theta}(X),\theta \in \bold{R}^n\}"/></div>
其中参数向量 <img " src="http://latex.codecogs.com/gif.latex?\theta "/>  取值与n维欧式空间<img " src="http://latex.codecogs.com/gif.latex?\bold{R}^n "/>，称为参数空间。
	假设空间也可以定义为条件概率的集合（概率模型）。
### 1.3.2 策略

​	首先介绍几种常见的损失函数：损失函数（或代价函数）用来度量预测的错误程度。损失函数时<img " src="http://latex.codecogs.com/gif.latex?f(X) "/>和<img " src="http://latex.codecogs.com/gif.latex?Y "/>的非负实值函数，记作<img " src="http://latex.codecogs.com/gif.latex?L(Y,f(X)) "/>.

	统计学中常用的损失函数：

（1）0-1损失函数
<div align=center><img " src="http://latex.codecogs.com/gif.latex?L(Y,f(X))=\left\{
\begin{aligned}
1, Y \neq f(X) \\
0, Y=f(X) 
\end{aligned}
\right."/></div>
（2）平方损失函数
<div align=center><img " src="http://latex.codecogs.com/gif.latex?L(Y,f(X))=(Y-f(X))^2"/></div>
（3）绝对损失函数
<div align=center><img " src="http://latex.codecogs.com/gif.latex?L(Y,f(X))=|Y-f(X)|"/></div>
（4）对数损失函数
<div align=center><img " src="http://latex.codecogs.com/gif.latex?L(Y,f(X))=-logP(Y|X)"/></div>

损失函数值越小，模型就越好。模型<img " src="http://latex.codecogs.com/gif.latex?f(X) "/>关于训练数据集的平均损失称为经验风险或经验损失。