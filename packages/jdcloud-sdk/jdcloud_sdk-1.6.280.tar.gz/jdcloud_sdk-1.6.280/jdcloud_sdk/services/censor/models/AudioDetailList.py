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


class AudioDetailList(object):

    def __init__(self, audio_time=None, audio_pass_time=None, audio_review_time=None, audio_block_time=None):
        """
        :param audio_time: (Optional) 总时长,单位为分钟
        :param audio_pass_time: (Optional) 正常时长,单位为分钟
        :param audio_review_time: (Optional) 疑似时长，单位为分钟
        :param audio_block_time: (Optional) 违规时长，单位为分钟
        """

        self.audio_time = audio_time
        self.audio_pass_time = audio_pass_time
        self.audio_review_time = audio_review_time
        self.audio_block_time = audio_block_time
