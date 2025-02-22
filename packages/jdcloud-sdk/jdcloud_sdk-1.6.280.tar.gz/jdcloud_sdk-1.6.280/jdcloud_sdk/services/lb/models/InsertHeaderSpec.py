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


class InsertHeaderSpec(object):

    def __init__(self, valueType, key, value, ):
        """
        :param valueType:  http header的value类型：1.系统值类型；2.自定义值类型
        :param key:  新增http header的key，必填，最长40个字符，不区分大小写，支持大小写字母、数字、下划线（_）和短划线（-），不允许使用系统header+部分http标准header，同一个key在插入/删除中只能出现一次，具体不允许的key如下：
1.alb系统的header key：X-Forwarded-For、X-Forwarded-Client-Port、X-Forwarded-Host、X-Forwarded-Port、X-Forwarded-Proto、X-Forwarded-LBIP
2.部分http标准header：connection、upgrade、content-length、transfer-encoding、keep-alive、te、host、cookie

        :param value:  新增http header的value，必填，取值包括两种：
1.引用alb系统定义的header值：X-Forwarded-For、X-Forwarded-Client-Port、X-Forwarded-Host、X-Forwarded-Port、X-Forwarded-Proto、X-Forwarded-LBIP
2.客户自定义的header值，输入限制：最长128个字符，ASCII码值ch >= 32 && ch < 127范围内的可打印字符，字母区分大小写，开头和结尾不能为空格
        """

        self.valueType = valueType
        self.key = key
        self.value = value
