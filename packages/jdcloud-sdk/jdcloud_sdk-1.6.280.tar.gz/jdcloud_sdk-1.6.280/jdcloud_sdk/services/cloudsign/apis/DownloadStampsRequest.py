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


class DownloadStampsRequest(JDCloudRequest):
    """
    此接口仅供前端使用
1. 下载印章
2. 多个印章id用逗号分隔
 [MFA enabled]
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(DownloadStampsRequest, self).__init__(
            '/smqStamp/{stampId}:downloadStamps', 'GET', header, version)
        self.parameters = parameters


class DownloadStampsParameters(object):

    def __init__(self,stampId):
        """
        :param stampId: 印章ID
        """

        self.stampId = stampId

