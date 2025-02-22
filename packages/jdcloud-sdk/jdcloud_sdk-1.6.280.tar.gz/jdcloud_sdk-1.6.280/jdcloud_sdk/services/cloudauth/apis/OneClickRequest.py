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


class OneClickRequest(JDCloudRequest):
    """
    一键登录
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(OneClickRequest, self).__init__(
            '/oneClick:login', 'POST', header, version)
        self.parameters = parameters


class OneClickParameters(object):

    def __init__(self,token, appType):
        """
        :param token: 移动端获取的token
        :param appType: 应用类型（1 ios应用；2 H5应用；3 安卓应用）
        """

        self.token = token
        self.userInformation = None
        self.appType = appType

    def setUserInformation(self, userInformation):
        """
        :param userInformation: (Optional) 浏览器加密指纹（H5时必传）
        """
        self.userInformation = userInformation

