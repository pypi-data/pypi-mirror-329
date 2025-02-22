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


class CertificatePack(object):

    def __init__(self, certificate_authority=None, created_on=None, id=None, type=None, ty_pe=None, status=None, validation_method=None, validation_records=None, validity_days=None, hosts=None, certificates=None, primary_certificate=None):
        """
        :param certificate_authority: (Optional) 证书颁发机构
        :param created_on: (Optional) 创建时间
        :param id: (Optional) 证书包的唯一标识符
        :param type: (Optional) 证书包的类型，有效值universal/sni_custom/advanced
universal    通用
sni_custom   自定义
advanced     专用

        :param ty_pe: (Optional) 证书包的类型，有效值universal/sni_custom/advanced
universal    通用
sni_custom   自定义
advanced     专用
(值同type)

        :param status: (Optional) 证书包的状态，active/expired/deleted/pending/initializing
        :param validation_method: (Optional) 校验方式，http/txt
        :param validation_records: (Optional) 
        :param validity_days: (Optional) 有效期
        :param hosts: (Optional) 证书包的有效主机名的逗号分隔列表。必须包含域的顶级域名，不能包含超过50个主机，并且不能为空。
        :param certificates: (Optional) 
        :param primary_certificate: (Optional) 包中主证书的标识符
        """

        self.certificate_authority = certificate_authority
        self.created_on = created_on
        self.id = id
        self.type = type
        self.ty_pe = ty_pe
        self.status = status
        self.validation_method = validation_method
        self.validation_records = validation_records
        self.validity_days = validity_days
        self.hosts = hosts
        self.certificates = certificates
        self.primary_certificate = primary_certificate
