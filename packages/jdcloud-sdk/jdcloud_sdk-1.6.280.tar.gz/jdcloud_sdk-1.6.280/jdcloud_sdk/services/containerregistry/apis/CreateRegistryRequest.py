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


class CreateRegistryRequest(JDCloudRequest):
    """
    通过参数创建注册表。

    """

    def __init__(self, parameters, header=None, version="v1"):
        super(CreateRegistryRequest, self).__init__(
            '/regions/{regionId}/registries', 'POST', header, version)
        self.parameters = parameters


class CreateRegistryParameters(object):

    def __init__(self, regionId, registryName, ):
        """
        :param regionId: Region ID
        :param registryName: 用户定义的registry名称。<br> DNS兼容registry名称规则如下：
 <br> 不可为空，且不能超过32字符 <br> 以小写字母开始和结尾，支持使用小写字母、数字、中划线(-)

        """

        self.regionId = regionId
        self.registryName = registryName
        self.description = None

    def setDescription(self, description):
        """
        :param description: (Optional) 注册表描述，<a href="https://www.jdcloud.com/help/detail/3870/isCatalog/1">参考公共参数规范</a>。

        """
        self.description = description

