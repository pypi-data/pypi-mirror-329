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


class UpdateIndexOptionRequest(JDCloudRequest):
    """
    更新索引配置：业务日志指定索引相关的配置，包含全局及字段级别的配置
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(UpdateIndexOptionRequest, self).__init__(
            '/regions/{regionId}/logtopics/{logtopicUID}/indexoptions', 'PUT', header, version)
        self.parameters = parameters


class UpdateIndexOptionParameters(object):

    def __init__(self,regionId, logtopicUID, logReduce, fulltextIndex, caseSensitive, chn, maxTextLen):
        """
        :param regionId: 地域 Id
        :param logtopicUID: 日志主题 UID
        :param logReduce: 是否开启日志聚类，0-禁用，1-启用
        :param fulltextIndex: 是否开启全文检索，0-禁用，1-启用
        :param caseSensitive: 是否大小写敏感
        :param chn: 是否开启中文分词
        :param maxTextLen: 统计分析字段最大长度
        """

        self.regionId = regionId
        self.logtopicUID = logtopicUID
        self.logReduce = logReduce
        self.fulltextIndex = fulltextIndex
        self.caseSensitive = caseSensitive
        self.chn = chn
        self.token = None
        self.fieldIndexOptions = None
        self.maxTextLen = maxTextLen

    def setToken(self, token):
        """
        :param token: (Optional) 分词符
        """
        self.token = token

    def setFieldIndexOptions(self, fieldIndexOptions):
        """
        :param fieldIndexOptions: (Optional) 字段索引配置
        """
        self.fieldIndexOptions = fieldIndexOptions

