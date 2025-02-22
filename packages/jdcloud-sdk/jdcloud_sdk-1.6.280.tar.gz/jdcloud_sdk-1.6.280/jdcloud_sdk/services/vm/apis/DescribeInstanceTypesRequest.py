# coding=utf8

# Copyright 2018 JDCLOUD.COM
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# NOTE: This class is auto generated by the jdcloud code generator program.

from jdcloud_sdk.core.jdcloudrequest import JDCloudRequest


class DescribeInstanceTypesRequest(JDCloudRequest):
    """
    
查询实例规格列表。

详细操作说明请参考帮助文档：[实例规格类型](https://docs.jdcloud.com/cn/virtual-machines/instance-type-family)

## 接口说明
- 调用该接口可查询全量实例规格信息。
- 可查询实例规格的CPU、内存大小、可绑定的弹性网卡数量、可挂载的云硬盘数量，是否售卖等信息。
- GPU 或 本地存储型的规格可查询 GPU型号、GPU卡数量、本地盘数量。
- 尽量使用过滤器查询关心的实例规格，并适当缓存这些信息。否则全量查询可能响应较慢。

    """

    def __init__(self, parameters, header=None, version="v1"):
        super(DescribeInstanceTypesRequest, self).__init__(
            '/regions/{regionId}/instanceTypes', 'GET', header, version)
        self.parameters = parameters


class DescribeInstanceTypesParameters(object):

    def __init__(self,regionId, ):
        """
        :param regionId: 地域ID。
        """

        self.regionId = regionId
        self.serviceName = None
        self.chargeMode = None
        self.filters = None

    def setServiceName(self, serviceName):
        """
        :param serviceName: (Optional) 产品线类型，默认为 `vm`。支持范围：`vm` 云主机，`nc` 原生容器。
        """
        self.serviceName = serviceName

    def setChargeMode(self, chargeMode):
        """
        :param chargeMode: (Optional) 目前支持postpaid_by_spot：抢占式实例(后付费)。
        """
        self.chargeMode = chargeMode

    def setFilters(self, filters):
        """
        :param filters: (Optional) <b>filters 中支持使用以下关键字进行过滤</b>
`instanceTypes`: 实例规格，精确匹配，支持多个
`az`: 可用区，精确匹配，支持多个
`architecture`: CPU架构，精确匹配，支持单个，可选范围:x86_64或arm64

        """
        self.filters = filters

