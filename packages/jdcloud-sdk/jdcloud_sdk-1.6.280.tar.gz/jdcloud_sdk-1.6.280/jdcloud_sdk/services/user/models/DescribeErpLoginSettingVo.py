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


class DescribeErpLoginSettingVo(object):

    def __init__(self, loginName=None, pin=None, disableOtherLogin=None, erps=None, updateTime=None, operator=None, userResourceType=None, userReportType=None, remark=None, enableErpLogin=None):
        """
        :param loginName: (Optional) 账号名
        :param pin: (Optional) pin
        :param disableOtherLogin: (Optional) 是否禁用其他登录方式
        :param erps: (Optional) erps
        :param updateTime: (Optional) 修改时间
        :param operator: (Optional) 操作人
        :param userResourceType: (Optional) 用户资源类型
        :param userReportType: (Optional) 报备类型
        :param remark: (Optional) 备注
        :param enableErpLogin: (Optional) 1开启，0关闭
        """

        self.loginName = loginName
        self.pin = pin
        self.disableOtherLogin = disableOtherLogin
        self.erps = erps
        self.updateTime = updateTime
        self.operator = operator
        self.userResourceType = userResourceType
        self.userReportType = userReportType
        self.remark = remark
        self.enableErpLogin = enableErpLogin
