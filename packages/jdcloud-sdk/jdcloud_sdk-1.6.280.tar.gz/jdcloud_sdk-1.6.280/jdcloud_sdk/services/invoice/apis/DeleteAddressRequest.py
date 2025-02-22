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


class DeleteAddressRequest(JDCloudRequest):
    """
    删除发票邮寄地址
    """

    def __init__(self, parameters, header=None, version="v2"):
        super(DeleteAddressRequest, self).__init__(
            '/regions/{regionId}/address/{id}', 'DELETE', header, version)
        self.parameters = parameters


class DeleteAddressParameters(object):

    def __init__(self,regionId, id, ):
        """
        :param regionId: 
        :param id: 
        """

        self.regionId = regionId
        self.id = id
        self.pin = None

    def setPin(self, pin):
        """
        :param pin: (Optional) 用户pin(运营后台必传)
        """
        self.pin = pin

