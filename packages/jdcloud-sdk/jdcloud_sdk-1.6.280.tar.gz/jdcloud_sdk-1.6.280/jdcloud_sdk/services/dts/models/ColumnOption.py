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


class ColumnOption(object):

    def __init__(self, typeName=None, mappingTypeDefault=None, mappingTypeOptional=None):
        """
        :param typeName: (Optional) 类型名称
        :param mappingTypeDefault: (Optional) 默认映射类型
        :param mappingTypeOptional: (Optional) 支持的映射类型
        """

        self.typeName = typeName
        self.mappingTypeDefault = mappingTypeDefault
        self.mappingTypeOptional = mappingTypeOptional
