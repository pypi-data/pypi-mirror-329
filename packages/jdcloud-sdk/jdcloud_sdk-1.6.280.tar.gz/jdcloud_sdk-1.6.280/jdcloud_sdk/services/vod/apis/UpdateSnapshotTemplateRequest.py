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


class UpdateSnapshotTemplateRequest(JDCloudRequest):
    """
    修改截图模板
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(UpdateSnapshotTemplateRequest, self).__init__(
            '/snapshotTemplates/{templateId}', 'PUT', header, version)
        self.parameters = parameters


class UpdateSnapshotTemplateParameters(object):

    def __init__(self, templateId,):
        """
        :param templateId: 模板ID
        """

        self.templateId = templateId
        self.templateName = None
        self.snapshotType = None
        self.imageSampleConfig = None
        self.imageSpriteConfig = None

    def setTemplateName(self, templateName):
        """
        :param templateName: (Optional) 模板标题。长度不超过 128 个字节。UTF-8 编码。
        """
        self.templateName = templateName

    def setSnapshotType(self, snapshotType):
        """
        :param snapshotType: (Optional) 模板类型。取值范围：
  sample - 采样截图模板
  sprite - 雪碧图模板

        """
        self.snapshotType = snapshotType

    def setImageSampleConfig(self, imageSampleConfig):
        """
        :param imageSampleConfig: (Optional) 采样截图模板配置
        """
        self.imageSampleConfig = imageSampleConfig

    def setImageSpriteConfig(self, imageSpriteConfig):
        """
        :param imageSpriteConfig: (Optional) 雪碧图模板配置
        """
        self.imageSpriteConfig = imageSpriteConfig

