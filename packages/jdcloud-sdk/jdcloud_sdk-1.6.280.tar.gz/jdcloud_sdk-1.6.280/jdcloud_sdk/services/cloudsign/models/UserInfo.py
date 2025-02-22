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


class UserInfo(object):

    def __init__(self, name=None, mobile=None, idCardNum=None, signOrder=None, userType=None, keyword=None):
        """
        :param name: (Optional) 姓名 或 企业名
        :param mobile: (Optional) 手机号（个人信息需要设置）
        :param idCardNum: (Optional) 身份证号（个人信息需要设置）
        :param signOrder: (Optional) 签署序号
        :param userType: (Optional) 用户类型 （0 个人用户，1 企业用户 ）
        :param keyword: (Optional) 关键字签署时，需要设置盖章关键字
        """

        self.name = name
        self.mobile = mobile
        self.idCardNum = idCardNum
        self.signOrder = signOrder
        self.userType = userType
        self.keyword = keyword
