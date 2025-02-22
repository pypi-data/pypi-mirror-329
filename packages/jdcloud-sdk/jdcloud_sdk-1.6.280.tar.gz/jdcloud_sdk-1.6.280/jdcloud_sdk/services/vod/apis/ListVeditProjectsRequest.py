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


class ListVeditProjectsRequest(JDCloudRequest):
    """
    查询视频剪辑工程列表。
允许通过条件过滤查询，支持的过滤字段如下：
  - projectId[eq] 按照工程ID精确查询

    """

    def __init__(self, parameters, header=None, version="v1"):
        super(ListVeditProjectsRequest, self).__init__(
            '/veditProjects', 'GET', header, version)
        self.parameters = parameters


class ListVeditProjectsParameters(object):

    def __init__(self, ):
        """
        """

        self.pageNumber = None
        self.pageSize = None
        self.filters = None

    def setPageNumber(self, pageNumber):
        """
        :param pageNumber: (Optional) 页码；默认值为 1
        """
        self.pageNumber = pageNumber

    def setPageSize(self, pageSize):
        """
        :param pageSize: (Optional) 分页大小；默认值为 10；取值范围 [10, 100]
        """
        self.pageSize = pageSize

    def setFilters(self, filters):
        """
        :param filters: (Optional) 
        """
        self.filters = filters

