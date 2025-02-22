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


class DeviceCredential(object):

    def __init__(self, deviceId=None, deviceName=None, identifier=None, secret=None, productKey=None):
        """
        :param deviceId: (Optional) 设备Id
        :param deviceName: (Optional) 设备名称
        :param identifier: (Optional) 设备鉴权标识
        :param secret: (Optional) 设备秘钥
        :param productKey: (Optional) 所属产品
        """

        self.deviceId = deviceId
        self.deviceName = deviceName
        self.identifier = identifier
        self.secret = secret
        self.productKey = productKey
