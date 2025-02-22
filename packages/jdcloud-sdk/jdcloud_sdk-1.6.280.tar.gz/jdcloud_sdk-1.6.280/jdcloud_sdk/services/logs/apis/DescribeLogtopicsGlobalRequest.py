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


class DescribeLogtopicsGlobalRequest(JDCloudRequest):
    """
    查询日志主题列表，支持按照名称模糊查询。
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(DescribeLogtopicsGlobalRequest, self).__init__(
            '/regions/{regionId}/logtopics', 'GET', header, version)
        self.parameters = parameters


class DescribeLogtopicsGlobalParameters(object):

    def __init__(self,regionId, ):
        """
        :param regionId: 地域 Id
        """

        self.regionId = regionId
        self.filters = None
        self.tags = None
        self.appName = None

    def setFilters(self, filters):
        """
        :param filters: (Optional) 过滤条件，key，Values， 合法的key：logtopicName， logtopicUID， logsetName， logsetUID
        """
        self.filters = filters

    def setTags(self, tags):
        """
        :param tags: (Optional) 过滤条件，key，Values
        """
        self.tags = tags

    def setAppName(self, appName):
        """
        :param appName: (Optional) 日志主题采集的日志类型
        """
        self.appName = appName

