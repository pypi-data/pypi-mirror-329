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


class GetSslCertListRequest(JDCloudRequest):
    """
    查看证书列表
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(GetSslCertListRequest, self).__init__(
            '/sslCert', 'GET', header, version)
        self.parameters = parameters


class GetSslCertListParameters(object):

    def __init__(self,):
        """
        """

        self.pageNumber = None
        self.pageSize = None
        self.domain = None

    def setPageNumber(self, pageNumber):
        """
        :param pageNumber: (Optional) 第几页，从1开始计数
        """
        self.pageNumber = pageNumber

    def setPageSize(self, pageSize):
        """
        :param pageSize: (Optional) 每页显示的数目
        """
        self.pageSize = pageSize

    def setDomain(self, domain):
        """
        :param domain: (Optional) 域名，支持按照域名检索证书
        """
        self.domain = domain

