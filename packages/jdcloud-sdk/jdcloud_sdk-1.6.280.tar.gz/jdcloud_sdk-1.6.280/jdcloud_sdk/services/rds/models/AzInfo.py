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


class AzInfo(object):

    def __init__(self, laz=None, paz=None, azType=None):
        """
        :param laz: (Optional) 逻辑可用区
        :param paz: (Optional) 物理可用区
        :param azType: (Optional) 可用区类型，1为标准子网，2为边缘子网
        """

        self.laz = laz
        self.paz = paz
        self.azType = azType
