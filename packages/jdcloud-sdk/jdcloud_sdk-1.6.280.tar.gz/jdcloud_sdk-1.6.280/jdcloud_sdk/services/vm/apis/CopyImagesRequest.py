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


class CopyImagesRequest(JDCloudRequest):
    """
    
镜像复制。

详细操作说明请参考帮助文档：[镜像复制](https://docs.jdcloud.com/cn/virtual-machines/copy-image)

## 接口说明
- 调用该接口可以复制私有或共享镜像。
- 复制私有镜像时，只允许镜像拥有者进行复制。
- 复制共享镜像时，允许共享的用户将镜像复制为私有镜像。
- 支持同地域复制镜像。
- 只支持云盘系统盘的镜像。
- 不支持带有加密快照的镜像。

    """

    def __init__(self, parameters, header=None, version="v1"):
        super(CopyImagesRequest, self).__init__(
            '/regions/{regionId}/images:copyImages', 'POST', header, version)
        self.parameters = parameters


class CopyImagesParameters(object):

    def __init__(self,regionId, sourceImageIds, destinationRegion, ):
        """
        :param regionId: 地域ID。
        :param sourceImageIds: 要复制的私有镜像ID列表，最多支持10个。
        :param destinationRegion: 目标地域。
        """

        self.regionId = regionId
        self.sourceImageIds = sourceImageIds
        self.destinationRegion = destinationRegion
        self.name = None
        self.description = None

    def setName(self, name):
        """
        :param name: (Optional) 复制出新镜像的名称，长度为1\~32个字符，只允许中文、数字、大小写字母、英文下划线（\_）、连字符（-）及点（.）。
指定该参数时，所有复制出的镜像都设置相同的名称。
不指定该参数时，复制的镜像使用源镜像名称。

        """
        self.name = name

    def setDescription(self, description):
        """
        :param description: (Optional) 复制出新镜像的描述，不超过256个字符。
指定该参数时，所有复制出的镜像都设置相同的描述。
不指定该参数时，复制的镜像使用系统生成的描述信息。

        """
        self.description = description

