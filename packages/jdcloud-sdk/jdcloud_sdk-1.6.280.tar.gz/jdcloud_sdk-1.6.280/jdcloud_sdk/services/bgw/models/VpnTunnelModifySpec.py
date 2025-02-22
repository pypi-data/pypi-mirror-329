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


class VpnTunnelModifySpec(object):

    def __init__(self, psk=None, tunnelIp=None, localTunnelIp=None, ikeVersion=None, ikeMode=None, ikeKeyExchange=None, ikeCipher=None, ikeAuth=None, ikeDpdSec=None, ikeSaLifeSec=None, ipsecCipher=None, ipsecAuth=None, ipsecKeyExchange=None, ipsecSaLifeSec=None, ipsecSaLifepkt=None, ipsecSaLifebyte=None, bandwidthMbps=None):
        """
        :param psk: (Optional) 预共享秘钥字符串, 只允许输入数字、大小写字母、英文下划线“_”及中划线“-”，不允许为空且不超过20字符, 不能以0x或0s开头
        :param tunnelIp: (Optional) VPN隧道内网的掩码长度必须为30的CIDR格式IPv4地址段，必须在169.254.0.0/20, 10.0.0.0/8, 192.168.0.0/16, 172.16.0.0/12这四个网段内，且不能和同一边界网关上的其它VPN隧道内层地址冲突
        :param localTunnelIp: (Optional) VPN隧道内网的本端ip，必须是/30的且不能是第一个和最后一个ip
        :param ikeVersion: (Optional) IKE版本, 取值范围为：v1、v2
        :param ikeMode: (Optional) IKE模式, IKEv2时忽略, 取值范围为：main、aggressive
        :param ikeKeyExchange: (Optional) DH秘钥协商算法组选项. 取值范围为：modp1024、modp1536、modp2048、ecp256、ecp384
        :param ikeCipher: (Optional) 加密算法. 取值范围为：aes128、aes192、aes256、3des
        :param ikeAuth: (Optional) 认证算法. 取值范围为：sha1、sha256、sha384
        :param ikeDpdSec: (Optional) DPD开关, 取值范围为：0、10，10代表10秒
        :param ikeSaLifeSec: (Optional) IKE SA重协商时间，单位秒，取值范围为[60,86400]的整数
        :param ipsecCipher: (Optional) 加密算法. 取值范围为：aes128、aes192、aes256
        :param ipsecAuth: (Optional) 认证算法. 取值范围为：sha1、sha256、sha384
        :param ipsecKeyExchange: (Optional) DH组选项. 取值范围为：null、modp1024、modp1536、modp2048、ecp256、ecp384
        :param ipsecSaLifeSec: (Optional) Child SA重协商时间. 单位秒, 取值范围为[60,86400]的整数
        :param ipsecSaLifepkt: (Optional) Child SA重协商报数，单位个, 0代表不开启，取值范围为[0,100000000]的整数
        :param ipsecSaLifebyte: (Optional) Child SA重协商字节数. 单位字节, 0代表不开启，取值范围为[0,107374182400]的整数
        :param bandwidthMbps: (Optional) VPN隧道公网限速带宽（单位：Mbps），取值范围为[1-1500]
        """

        self.psk = psk
        self.tunnelIp = tunnelIp
        self.localTunnelIp = localTunnelIp
        self.ikeVersion = ikeVersion
        self.ikeMode = ikeMode
        self.ikeKeyExchange = ikeKeyExchange
        self.ikeCipher = ikeCipher
        self.ikeAuth = ikeAuth
        self.ikeDpdSec = ikeDpdSec
        self.ikeSaLifeSec = ikeSaLifeSec
        self.ipsecCipher = ipsecCipher
        self.ipsecAuth = ipsecAuth
        self.ipsecKeyExchange = ipsecKeyExchange
        self.ipsecSaLifeSec = ipsecSaLifeSec
        self.ipsecSaLifepkt = ipsecSaLifepkt
        self.ipsecSaLifebyte = ipsecSaLifebyte
        self.bandwidthMbps = bandwidthMbps
