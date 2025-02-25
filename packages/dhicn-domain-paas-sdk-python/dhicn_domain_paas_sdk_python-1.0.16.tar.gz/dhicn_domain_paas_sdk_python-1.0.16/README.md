<h1 align="center"> Domain-PaaS-SDK for Python </h1>
<div align="center">

 ![Python version](https://img.shields.io/pypi/pyversions/mikeio.svg)
[![PyPI version](https://badge.fury.io/py/dhicn_domain_paas_sdk_python.svg)](https://badge.fury.io/py/dhicn_domain_paas_sdk_python)
  
这是一个[DHI 中国 业务中台](https://online-products.dhichina.cn/) 的 Client SDK 开发辅助包，帮您快速通过我们的业务中台构建应用。

</div>

## 🔆 功能清单

- [x] dhicn_identity_service 用户认证管理服务
- [x] dhicn_scenario_manager_service 方案管理服务
- [x] dhicn_message_service 消息服务
- [x] dhicn_document_service 文档服务
- [x] dhicn_scenario_compute_service 方案计算服务
- [ ] dhicn_model_driver_service 模型计算服务
- [x] dhicn_result_analysis_service 结果分析服务
- [x] dhicn_model_information_service 模型分析服务
- [x] dhicn_model_configuration_service 模型计算服务
- [ ] dhicn_text_search_service 全文搜索服务
- [ ] dhicn_device_management_service 资产设备服务
- [x] dhicn_accident_management_service 事故管理服务
- [x] dhicn_digital_twin_service 模型映射服务
- [x] dhicn_iot_service IoT 服务
- [x] dhicn_wwtp_data_bus_service 污水业务中台领域服务
- [x] dhicn_wwtp_infrastructure_service 污水业务中台基础服务
- [x] dhicn_wd_domain_service 供水业务中台领域服务

## 适用平台
* Mac、Windows和Linux

## Installation

From PyPI: 

`pip install dhicn_domain_paas_sdk_python`

## 使用

需要先联系我们获取的 [DHI 中国 业务中台](https://online-products.dhichina.cn/) 使用许可和认证信息。

### 基础使用
test.py
```
# coding: utf-8

// 引入需要使用的包
from wwtp_paas_main_bus_service import *
from wwtp_paas_main_bus_service import ApiClient
from wwtp_paas_main_bus_service import CalculateDosageApi
// 构建参数
configuration=Configuration.get_default_copy()
configuration.verify_ssl=False
configuration.host="http://172.23.21.60:61120"
// 初始化
client = ApiClient(configuration)
calculate = CalculateDosageApi(client)
// 调用接口
response = calculate.api_calculate_dosage_excute_plc_get()

```
