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


class CreateFirewallRuleRequest(JDCloudRequest):
    """
    为指定的轻量应用云主机创建一条防火墙规则。

    """

    def __init__(self, parameters, header=None, version="v1"):
        super(CreateFirewallRuleRequest, self).__init__(
            '/regions/{regionId}/firewallRule', 'POST', header, version)
        self.parameters = parameters


class CreateFirewallRuleParameters(object):

    def __init__(self,regionId, instanceId, sourceAddress, ruleProtocol, port, ):
        """
        :param regionId: regionId

        :param instanceId: 指定的轻量应用云主机的实例ID

        :param sourceAddress: 源Ip的CRDI格式的地址

        :param ruleProtocol: 规则限定协议。取值范围：
TCP：TCP协议。
UDP：UDP协议。
ICMP：ICMP协议。

        :param port: 端口范围。若规则限定协议为传输层协议（TCP、UDP)，取值范围为1`~`65535，若规则限定协议为非传输层协议（ICMP协议），恒为0。使用正斜线（/）隔开起始端口和终止端口，例如：1024/1055表示端口范围为1024`~`1055。

        """

        self.regionId = regionId
        self.instanceId = instanceId
        self.sourceAddress = sourceAddress
        self.ruleProtocol = ruleProtocol
        self.port = port
        self.remark = None
        self.clientToken = None

    def setRemark(self, remark):
        """
        :param remark: (Optional) 防火墙规则的备注, 不超过100个字符

        """
        self.remark = remark

    def setClientToken(self, clientToken):
        """
        :param clientToken: (Optional) 用于保证请求的幂等性。由客户端生成，并确保不同请求中该参数唯一，长度不能超过64个字符。

        """
        self.clientToken = clientToken

