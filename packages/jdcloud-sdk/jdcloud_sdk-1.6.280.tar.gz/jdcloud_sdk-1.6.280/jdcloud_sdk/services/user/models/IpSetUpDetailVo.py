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


class IpSetUpDetailVo(object):

    def __init__(self, title=None, titleCode=None, ip=None, pin=None, isApi=None):
        """
        :param title: (Optional) 标题
        :param titleCode: (Optional) 标题编码 用户ip白名单为空
        :param ip: (Optional) ip集合 逗号区分
        :param pin: (Optional) pin/pin集合 逗号区分
        :param isApi: (Optional) 是否控制网关sdk：0否，1是
        """

        self.title = title
        self.titleCode = titleCode
        self.ip = ip
        self.pin = pin
        self.isApi = isApi
