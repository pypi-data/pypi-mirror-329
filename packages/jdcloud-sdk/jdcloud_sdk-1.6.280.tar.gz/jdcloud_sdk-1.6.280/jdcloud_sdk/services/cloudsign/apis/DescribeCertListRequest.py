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


class DescribeCertListRequest(JDCloudRequest):
    """
    获取已申请证书列表
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(DescribeCertListRequest, self).__init__(
            '/smqCert:list', 'GET', header, version)
        self.parameters = parameters


class DescribeCertListParameters(object):

    def __init__(self,):
        """
        """

        self.pageNumber = None
        self.pageSize = None
        self.caType = None
        self.name = None
        self.serialNo = None
        self.keyAlg = None
        self.certStatus = None

    def setPageNumber(self, pageNumber):
        """
        :param pageNumber: (Optional) 页码, 默认为1
        """
        self.pageNumber = pageNumber

    def setPageSize(self, pageSize):
        """
        :param pageSize: (Optional) 分页大小, 默认为10, 取值范围[10, 100]
        """
        self.pageSize = pageSize

    def setCaType(self, caType):
        """
        :param caType: (Optional) 证书渠道
        """
        self.caType = caType

    def setName(self, name):
        """
        :param name: (Optional) 个人用户姓名或企业名
        """
        self.name = name

    def setSerialNo(self, serialNo):
        """
        :param serialNo: (Optional) 证书序列号
        """
        self.serialNo = serialNo

    def setKeyAlg(self, keyAlg):
        """
        :param keyAlg: (Optional) 证书算法
        """
        self.keyAlg = keyAlg

    def setCertStatus(self, certStatus):
        """
        :param certStatus: (Optional) 证书状态
        """
        self.certStatus = certStatus

