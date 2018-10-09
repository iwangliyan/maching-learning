##  2018高校校园大数据竞赛代码说明

### 1、简介

​       该程序是2018高校校园大数据竞赛算法赛tensorflow-boys小组使用的代码。该竞赛题目是提供了北京邮电大学2017年1-11月份33个地点不同时刻（以小时为单位）校园网IP出现的记录，要求对2017年12月份33个地点每个时刻的IP出现次数进行估计，评判标准为RMSE。我们主要使用了规则模型、决策树、Xgboost、RNN等机器学习和深度学习算法，实现算法的语言是Python。下面将介绍安装、运行方法，以及部分模块的主要功能。

### 2、安装

* 该程序主要用Python 3.6.2编写，需要安装的库及其版本有：

  matplotlib==2.2.2
  numpy==1.14.2
  pandas==0.20.3
  scikit-learn==0.19.0
  tensorflow==1.7.0

  xgboost==0.71

  其中，Python可以从[Python官网](https://www.python.org/downloads/)下载，Windows操作系统下Python库可以在cmd.exe执行pip命令安装:

  ```shell
  pip install numpy==1.14.2
  ```

  Linux操作系统下Python库也可以在terminal用pip3命令安装，也可以用yum，apt-get命令安装：

  ```shell
  sudo apt-get install python3-pandas
  ```

### 3、运行

* 方法一：将python3添加至环境变量后，在cmd/terminal下打开工程目录下运行python

* 方法二：如果电脑已安装可以运行Python工程的IDE，如Spyder，PyCharm等，则可直接在IDE中运行。       

### 4、模块介绍

- data目录：原始数据由cleaning.py,new_cleaning.py,res_method.py模块处理后，清洗后的训练数据储存在该目录下，数据类型为csv和json格式。
- fig目录：用pretreatment.py等分析生成的图像储存在该目录下。
- result目录，储存预测结果，数据类型为csv。
- cleaning.py, new_cleaning.py: 用于处理原始数据，将其转为字段为地点、时间、人数的csv数据，便于接下来的分析。
- pretreatment.py,error_method：用于探索性分析，绘制所需的时序图。
- regular_model.py,shallow_learning_model,rnn_model,xgboost：模型的主程序，分别为规则模型、随机怎林、Xgboost模型和RNN模型。
- res_method.py,compare.py, compare_all_place.py：用于对结果进行分析，调整。


