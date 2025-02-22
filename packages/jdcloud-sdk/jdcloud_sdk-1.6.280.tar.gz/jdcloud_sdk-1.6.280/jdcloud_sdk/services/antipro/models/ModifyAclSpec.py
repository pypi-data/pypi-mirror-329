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


class ModifyAclSpec(object):

    def __init__(self, sipType, dipType, protocol, action, remark, sip=None, sipIpSetId=None, dip=None, dipIpSetId=None, portType=None, port=None, portSetId=None):
        """
        :param sipType:  源IP类型: 0: IP, 1: IP地址库
        :param sip: (Optional) 源IP, sipType 为 0 时有效, 否则为空
        :param sipIpSetId: (Optional) IP地址库 Id, sipType 为 1 时必传, 可以使用自定义地址库或以下地址库。<br>'-1' IP高防回源地址<br>'-2' Web应用防火墙回源地址
        :param dipType:  目的IP类型: 0: IP, 1: IP地址库
        :param dip: (Optional) 目的IP, dipType 为 0 时有效, 否则为空
        :param dipIpSetId: (Optional) IP地址库 Id, dipType 为 1 时必传, 可以使用自定义地址库或以下地址库。<br>'-1' IP高防回源地址<br>'-2' Web应用防火墙回源地址
        :param protocol:  协议类型: 支持 All Traffic, TCP, UDP, ICMP
        :param portType: (Optional) 端口类型: 0: 端口或端口范围, 1: 端口库
        :param port: (Optional) 端口或端口范围, portType 为 0 时有效，否则为空
        :param portSetId: (Optional) 端口库Id, portType 为 1 时必传
        :param action:  动作: 0: 放行, 1: 阻断. 阻断动作对ICMP协议所有端口生效, 所以动作为阻断, 且协议类型为 ICMP 时, 阻断动作端口类型, 端口或端口范围, 端口Id三个字段无效, 可不传
        :param remark:  备注
        """

        self.sipType = sipType
        self.sip = sip
        self.sipIpSetId = sipIpSetId
        self.dipType = dipType
        self.dip = dip
        self.dipIpSetId = dipIpSetId
        self.protocol = protocol
        self.portType = portType
        self.port = port
        self.portSetId = portSetId
        self.action = action
        self.remark = remark
