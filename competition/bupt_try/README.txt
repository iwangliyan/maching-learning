1. 运行环境

Ubuntu16.04、16G内存、安装jupyter notebook

2. 运行依赖

python3.6、numpy、pandas、sklearn、lightgbm、scipy、datetime、matplotlib、contextlib等 

3. 代码文件说明

0_analysisi.ipynb: 为可视化分析的部分，分析规则与模型预测结果和9,10,11月的趋势，以此来指导模型融合的部分。

weather.ipynb: 从网站 http://tianqi.2345.com/ 上爬取的天气信息，保存为天气编码格式和天气未编码的格式。

要得到预测结果，运行步骤为1-4:

1_process.ipynb: 为预处理部分，只用9,10,11月数据，根据3sigama原则，剔除部分异常值，并且去掉十一假期等异常日期的数据。

2_model.ipynb: 模型预测部分，使用lgb，rf，gbdt三个模型来预测12月的人流量。 

3_rule.ipynb: 规则预测部分，仅适用11月数据，添加日期衰减系数，和天气修正系数，得到12月的预测结果。

4_blend.ipynb: 融合规则和模型的预测结果，根据0_analysisi.ipynb的可视化结果，确定最终的融合方案。


代码的具体细节和实现，见ipynb内的注释。
