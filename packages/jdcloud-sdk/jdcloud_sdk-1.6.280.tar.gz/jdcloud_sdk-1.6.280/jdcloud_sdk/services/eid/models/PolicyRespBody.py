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


class PolicyRespBody(object):

    def __init__(self, verifyCode=None, eid=None, tokenTime=None, tokenActTime=None, isStrategy=None, cltDevice=None, cltManMachine=None, cltAppList=None, tk=None):
        """
        :param verifyCode: (Optional) 
        :param eid: (Optional) 
        :param tokenTime: (Optional) 
        :param tokenActTime: (Optional) 
        :param isStrategy: (Optional) 
        :param cltDevice: (Optional) 
        :param cltManMachine: (Optional) 
        :param cltAppList: (Optional) 
        :param tk: (Optional) 
        """

        self.verifyCode = verifyCode
        self.eid = eid
        self.tokenTime = tokenTime
        self.tokenActTime = tokenActTime
        self.isStrategy = isStrategy
        self.cltDevice = cltDevice
        self.cltManMachine = cltManMachine
        self.cltAppList = cltAppList
        self.tk = tk
