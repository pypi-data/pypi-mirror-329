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


class UpdateProbeTaskSpec(object):

    def __init__(self, probes, httpBody=None, httpCookie=None, httpHeader=None, httpType=None, name=None):
        """
        :param httpBody: (Optional) http body：选择探测类型为1=http时有效，最长不超过1024字节
        :param httpCookie: (Optional) http cookie：选择探测类型为1=http时有效，最大允许20个key、value对，最长不超过1024字节
        :param httpHeader: (Optional) http header：选择探测类型为1=http时有效，最大允许20个key、value对，最长不超过1024字节
        :param httpType: (Optional) http探测方法,可选值：1:get、2:post、3:head
        :param name: (Optional) task名称，不允许重复，长度不超过32字符，只允许中英文、数字、下划线_、中划线-, [0-9][a-z] [A-Z] [- _ ]
        :param probes:  探测源（发起对探测目标探测的云主机，需安装相应的agent才能探测）
        """

        self.httpBody = httpBody
        self.httpCookie = httpCookie
        self.httpHeader = httpHeader
        self.httpType = httpType
        self.name = name
        self.probes = probes
