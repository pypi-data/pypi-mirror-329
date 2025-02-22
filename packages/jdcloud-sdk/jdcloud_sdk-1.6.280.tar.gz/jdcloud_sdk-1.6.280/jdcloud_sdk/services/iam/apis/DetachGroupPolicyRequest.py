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


class DetachGroupPolicyRequest(JDCloudRequest):
    """
    为用户组解绑策略
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(DetachGroupPolicyRequest, self).__init__(
            '/group/{groupName}:detachGroupPolicy', 'DELETE', header, version)
        self.parameters = parameters


class DetachGroupPolicyParameters(object):

    def __init__(self,groupName, policyName, ):
        """
        :param groupName: 用户组名称
        :param policyName: 策略名称
        """

        self.groupName = groupName
        self.policyName = policyName
        self.scopeId = None
        self.allowDetachAddPolicy = None

    def setScopeId(self, scopeId):
        """
        :param scopeId: (Optional) 资源组id
        """
        self.scopeId = scopeId

    def setAllowDetachAddPolicy(self, allowDetachAddPolicy):
        """
        :param allowDetachAddPolicy: (Optional) 允许解除策略："Deny" 不允许，Allow 允许，空情况默认允许，兼容历史数据
        """
        self.allowDetachAddPolicy = allowDetachAddPolicy

