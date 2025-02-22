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


class UpdateAsRuleRequest(JDCloudRequest):
    """
    修改伸缩规则
- 所有参数取值为字符串类型的都严格区分大小写
- 所有伸缩规则不允许更换高可用组
- 所有伸缩规则不允许修改伸缩规则类型
- 步进规则不允许修改监控类型
- 所有参数都为非必传，但是至少需要传入一个参数，否则报错
- 伸缩功能开启或者关闭的情况下，都支持调用此接口

    """

    def __init__(self, parameters, header=None, version="v1"):
        super(UpdateAsRuleRequest, self).__init__(
            '/regions/{regionId}/asRules/{asRuleId}', 'POST', header, version)
        self.parameters = parameters


class UpdateAsRuleParameters(object):

    def __init__(self,regionId, asRuleId, ):
        """
        :param regionId: 地域ID
        :param asRuleId: 伸缩规则ID
        """

        self.regionId = regionId
        self.asRuleId = asRuleId
        self.name = None
        self.description = None
        self.simpleAsRuleSpec = None
        self.targetAsRuleSpec = None
        self.stepAsRuleSpec = None

    def setName(self, name):
        """
        :param name: (Optional) 伸缩规则名称，长度为1~32个字符，只允许中文、数字、大小写字母、英文下划线（_）、连字符（-）
        """
        self.name = name

    def setDescription(self, description):
        """
        :param description: (Optional) 伸缩规则描述，最大长度为256个字符
        """
        self.description = description

    def setSimpleAsRuleSpec(self, simpleAsRuleSpec):
        """
        :param simpleAsRuleSpec: (Optional) 简单规则相关参数，当待修改的规则类型为`Simple`时，填写此参数才有效
        """
        self.simpleAsRuleSpec = simpleAsRuleSpec

    def setTargetAsRuleSpec(self, targetAsRuleSpec):
        """
        :param targetAsRuleSpec: (Optional) 目标跟踪规则相关参数，当待修改的规则类型为`Target`时，填写此参数才有效
        """
        self.targetAsRuleSpec = targetAsRuleSpec

    def setStepAsRuleSpec(self, stepAsRuleSpec):
        """
        :param stepAsRuleSpec: (Optional) 步进规则相关参数，当待修改的规则类型为`Step`时，填写此参数才有效
        """
        self.stepAsRuleSpec = stepAsRuleSpec

