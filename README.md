# KnifeREC 推荐系统

系统预览
![view](./doc/sys_view.png)
目前支持模型：

    1.排序
    2.FM
    3.lda
    4.DeepCTR

## 安装

    pip install -r requirements.txt
    
或者使用conda
    
    conda install tensorflow-gpu

## 使用

    python app.py

## 接口调用

    todo restapi
    
后台管理帐号：
admin@admin.com / admin
    
预测结果调用

    http://localhost:5000/predict

## Features

1.数据源管理；
2.数据预处理；
3.模型管理；
4.模型输出；
5.策略管理；
6.模型监控；

## Questions

1.模型的启停设计；
2.模型的监控指标；
3.画像的生成管理；
4.选项细节操作；

## todo

1.模型管理参考digits；
2.GMV的管控；
3.使用EasyRL控制策略；
4.使用孪生网络进行相似用户、商品划分和推荐；
5.使用FP-Growth对用户行为频繁项挖掘；

## 相关研究进展

https://github.com/microsoft/recommenders

https://github.com/grahamjenson/list_of_recommender_systems


## 参与贡献

欢迎参与贡献开发

QQ群：747460350

[功能设计](./doc/design.md)

[框架设计](./doc/Dev.md)

### 技术支持

<a href="mailto:zergskj@163.com">夜半饿得慌</a>
