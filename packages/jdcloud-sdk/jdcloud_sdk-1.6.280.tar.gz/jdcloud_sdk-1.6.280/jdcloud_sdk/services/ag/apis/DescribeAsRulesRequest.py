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


class DescribeAsRulesRequest(JDCloudRequest):
    """
    查看伸缩规则
- 所有参数取值为字符串类型的都严格区分大小写
- 伸缩功能开启或者关闭的情况下，都支持调用此接口

    """

    def __init__(self, parameters, header=None, version="v1"):
        super(DescribeAsRulesRequest, self).__init__(
            '/regions/{regionId}/asRules', 'GET', header, version)
        self.parameters = parameters


class DescribeAsRulesParameters(object):

    def __init__(self,regionId, agId, ):
        """
        :param regionId: 地域ID
        :param agId: 高可用组ID
        """

        self.regionId = regionId
        self.agId = agId
        self.pageNumber = None
        self.pageSize = None
        self.filters = None
        self.sorts = None

    def setPageNumber(self, pageNumber):
        """
        :param pageNumber: (Optional) 页码，默认为`1`，最小值必须大于0
        """
        self.pageNumber = pageNumber

    def setPageSize(self, pageSize):
        """
        :param pageSize: (Optional) 分页大小，默认为`20`，取值范围[`10` ~ `100`]
        """
        self.pageSize = pageSize

    def setFilters(self, filters):
        """
        :param filters: (Optional) 支持使用以下关键字进行过滤查询
- `asRuleId`: 伸缩规则ID，精确匹配，支持多个
- `name`: 伸缩规则名称，模糊匹配，支持单个
- `asRuleType`: 伸缩规则类型，精确匹配，支持多个，取值范围：[`Simple`,`Target`,`Step`]

        """
        self.filters = filters

    def setSorts(self, sorts):
        """
        :param sorts: (Optional) 排序条件列表，目前只支持单个排序条件，不支持多个排序条件，默认按照 `createTime` 降序排序
支持使用以下关键字进行排序
- `createTime`: 创建时间

        """
        self.sorts = sorts

