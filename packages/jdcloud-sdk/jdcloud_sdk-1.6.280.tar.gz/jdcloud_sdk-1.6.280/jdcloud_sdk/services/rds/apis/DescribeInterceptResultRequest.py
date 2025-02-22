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


class DescribeInterceptResultRequest(JDCloudRequest):
    """
    查看开启高安全模式后，当前实例的 SQL 拦截记录<br>- 仅支持MySQL
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(DescribeInterceptResultRequest, self).__init__(
            '/regions/{regionId}/instances/{instanceId}/intercept:describeInterceptResult', 'GET', header, version)
        self.parameters = parameters


class DescribeInterceptResultParameters(object):

    def __init__(self,regionId, instanceId, ):
        """
        :param regionId: Region ID
        :param instanceId: Instance ID
        """

        self.regionId = regionId
        self.instanceId = instanceId
        self.pageNumber = None
        self.pageSize = None
        self.filters = None

    def setPageNumber(self, pageNumber):
        """
        :param pageNumber: (Optional) 显示数据的页码，默认为1，取值范围：[-1,∞)。pageNumber为-1时，返回所有数据页码；
        """
        self.pageNumber = pageNumber

    def setPageSize(self, pageSize):
        """
        :param pageSize: (Optional) 每页显示的数据条数，默认为10，取值范围：[10,100]，且为10的整数倍
        """
        self.pageSize = pageSize

    def setFilters(self, filters):
        """
        :param filters: (Optional) 过滤参数，多个过滤参数之间的关系为“与”(and);
支持以下属性的过滤：account,database,keyword; 支持operator选项：eq,in; 仅支持 MySQL，Percona，MariaDB

        """
        self.filters = filters

