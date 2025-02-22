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


class ErrorInfo(object):

    def __init__(self, code=None, message=None, status=None):
        """
        :param code: (Optional) 错误码，默认正确为0
        :param message: (Optional) 错误信息，默认为""
        :param status: (Optional) 错误状态信息，默认为""
        """

        self.code = code
        self.message = message
        self.status = status
