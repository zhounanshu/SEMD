### 可穿戴环境感知  
#### 1. 项目简介   
 
“气象徽章”是一款基于蓝牙4.0的可穿戴式气象监测设备。该项目为设备的数据采集提供接入后台，并对数据进行清洗和处理，为第三方的应用提供restful API接口。  
#### 2. 气象徽章  

“气象徽章”蓝牙设备测试指标：    

* 温度： -10 ~ 75℃  
* 湿度：0% ~ 100%RH 
* 气压: 300 ~ 1100 Hpa
* 紫外: 0 ~ 15@365nm  

本项目采用Flask框架，利用其蓝图模式可实现对应用的扩展，为第三方应用提供丰富的数据接口。 


