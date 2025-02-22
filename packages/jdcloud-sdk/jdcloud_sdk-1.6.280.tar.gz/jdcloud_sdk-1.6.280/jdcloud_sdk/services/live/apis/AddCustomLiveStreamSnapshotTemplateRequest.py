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


class AddCustomLiveStreamSnapshotTemplateRequest(JDCloudRequest):
    """
    添加直播截图模板
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(AddCustomLiveStreamSnapshotTemplateRequest, self).__init__(
            '/snapshotCustoms:template', 'POST', header, version)
        self.parameters = parameters


class AddCustomLiveStreamSnapshotTemplateParameters(object):

    def __init__(self, format, fillType, snapshotInterval, saveMode, saveBucket, template):
        """
        :param format: 截图格式
- 取值: jpg, png
- 不区分大小写

        :param fillType: 截图与设定的宽高不匹配时的处理规则
  1: 拉伸
  2: 留黑
  3: 留白
  4: 高斯模糊
- 1是按照设定宽高拉伸
- 2,3,4是等比例的缩放多余或不足处按调置处理

        :param snapshotInterval: 截图周期
- 取值范围 [5,3600]
- 单位: 秒

        :param saveMode: 存储模式
  1: 覆盖存储
  2: 顺序存储

        :param saveBucket: 存储桶
        :param template: 截图模板自定义名称:
- 取值要求: 数字、大小写字母或短横线("-")、下划线("_"),
  首尾不能有特殊字符("-")
  最大长度50个字符
- <b>注意: 不能与已定义命名重复</b>

        """

        self.format = format
        self.width = None
        self.height = None
        self.fillType = fillType
        self.snapshotInterval = snapshotInterval
        self.saveMode = saveMode
        self.saveBucket = saveBucket
        self.saveEndpoint = None
        self.template = template

    def setWidth(self, width):
        """
        :param width: (Optional) 截图宽度
- 取值: [8,8192]
- 如果(width,height)只设置其中之一,则按所设置参数项等比缩放另一项输出截图
- 如果(width,height)都不设置，则按源流大小输出截图

        """
        self.width = width

    def setHeight(self, height):
        """
        :param height: (Optional) 截图高度
- 取值: [8,8192]
- 如果(width,height)只设置其中之一,则按所设置参数项等比缩放另一项输出截图
- 如果(width,height)都不设置，则按源流大小输出截图

        """
        self.height = height

    def setSaveEndpoint(self, saveEndpoint):
        """
        :param saveEndpoint: (Optional) 存储地址
        """
        self.saveEndpoint = saveEndpoint

