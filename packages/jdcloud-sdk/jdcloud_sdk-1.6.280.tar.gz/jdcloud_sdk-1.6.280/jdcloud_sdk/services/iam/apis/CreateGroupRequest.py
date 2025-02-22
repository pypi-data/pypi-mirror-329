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


class CreateGroupRequest(JDCloudRequest):
    """
    创建用户组, <br>
可访问<a href="https://docs.jdcloud.com/cn/iam/group-management">用户组管理</a>了解更多<br>

    """

    def __init__(self, parameters, header=None, version="v1"):
        super(CreateGroupRequest, self).__init__(
            '/group', 'POST', header, version)
        self.parameters = parameters


class CreateGroupParameters(object):

    def __init__(self,createGroupInfo):
        """
        :param createGroupInfo: 
        """

        self.createGroupInfo = createGroupInfo

