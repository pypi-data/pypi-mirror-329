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


class CreateKeypair(object):

    def __init__(self, name, keyFingerprint=None, cloudID=None, publicKey=None):
        """
        :param name:  密钥名称
        :param keyFingerprint: (Optional) 密钥指纹
        :param cloudID: (Optional) 云注册信息ID
        :param publicKey: (Optional) 否  导入的公钥
        """

        self.name = name
        self.keyFingerprint = keyFingerprint
        self.cloudID = cloudID
        self.publicKey = publicKey
