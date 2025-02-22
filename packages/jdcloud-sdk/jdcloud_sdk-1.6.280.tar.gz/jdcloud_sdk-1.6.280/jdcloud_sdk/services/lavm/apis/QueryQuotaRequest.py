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


class QueryQuotaRequest(JDCloudRequest):
    """
    查询资源配额。
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(QueryQuotaRequest, self).__init__(
            '/regions/{regionId}/quotas', 'POST', header, version)
        self.parameters = parameters


class QueryQuotaParameters(object):

    def __init__(self,regionId, resourceTypes):
        """
        :param regionId: 地域ID。
        :param resourceTypes: 资源名列表，可取值:
general_instance 通用型套餐实例
custom_image 自定义镜像

        """

        self.regionId = regionId
        self.resourceTypes = resourceTypes

