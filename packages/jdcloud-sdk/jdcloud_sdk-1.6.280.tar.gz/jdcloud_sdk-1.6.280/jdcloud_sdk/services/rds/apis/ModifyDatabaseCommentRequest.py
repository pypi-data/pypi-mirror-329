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

from jdcloud_sdk.core.jdcloudrequest import JDCloudRequest


class ModifyDatabaseCommentRequest(JDCloudRequest):
    """
    修改数据库备注，仅支持MySQL
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(ModifyDatabaseCommentRequest, self).__init__(
            '/regions/{regionId}/instances/{instanceId}/databases/{dbName}:modifyDatabaseComment', 'POST', header, version)
        self.parameters = parameters


class ModifyDatabaseCommentParameters(object):

    def __init__(self,regionId, instanceId, dbName, comment):
        """
        :param regionId: 地域代码，取值范围参见[《各地域及可用区对照表》](../Enum-Definitions/Regions-AZ.md)
        :param instanceId: RDS 实例ID，唯一标识一个RDS实例
        :param dbName: 库名称
        :param comment: 数据库的备注信息，支持中午，ASCII字符，最大长度64
        """

        self.regionId = regionId
        self.instanceId = instanceId
        self.dbName = dbName
        self.comment = comment

