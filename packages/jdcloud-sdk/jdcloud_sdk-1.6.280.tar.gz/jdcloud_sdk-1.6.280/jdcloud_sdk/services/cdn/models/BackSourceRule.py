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


class BackSourceRule(object):

    def __init__(self, matchMode=None, before=None, after=None, priority=None):
        """
        :param matchMode: (Optional) 匹配方式,取值：全站(all)与url(url)
        :param before: (Optional) 待改写回源URL,1、选择全站时该项不允许填写，匹配方式为全站时为“^/(.\*)”，选择URL路径时需以/开头;2、若为(/.\*)即与全站等效,请选择全站:all匹配方式；3、\*与\*、\*与.\*不能连续；4、URL匹配方式：仅支持 “-”、“\”、“/”、“.”、字母、数字、通配符\*。
        :param after: (Optional) 目标回源URL,URL匹配方式：仅支持“-”、“\”、“/”、“.”、字母、数字、$。
        :param priority: (Optional) 优先级，1-50,不可重复
        """

        self.matchMode = matchMode
        self.before = before
        self.after = after
        self.priority = priority
