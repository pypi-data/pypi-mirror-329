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


class CompanyBaseInfo(object):

    def __init__(self, companyName=None, creditCode=None, legalRepresentative=None, establishedDate=None, registeredOffice=None, registeredCapital=None, companyType=None, industry=None, businessTerm=None, managementForms=None):
        """
        :param companyName: (Optional) 公司名称
        :param creditCode: (Optional) 统一社会信用代码
        :param legalRepresentative: (Optional) 法定代表人
        :param establishedDate: (Optional) 成立时间
        :param registeredOffice: (Optional) 注册地
        :param registeredCapital: (Optional) 注册资本
        :param companyType: (Optional) 企业类型
        :param industry: (Optional) 所属行业
        :param businessTerm: (Optional) 营业期限
        :param managementForms: (Optional) 经营状态
        """

        self.companyName = companyName
        self.creditCode = creditCode
        self.legalRepresentative = legalRepresentative
        self.establishedDate = establishedDate
        self.registeredOffice = registeredOffice
        self.registeredCapital = registeredCapital
        self.companyType = companyType
        self.industry = industry
        self.businessTerm = businessTerm
        self.managementForms = managementForms
