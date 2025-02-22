# Copyright (c) 2024, Zhendong Peng (pzd17@tsinghua.org.cn)
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

import g2p_en
import wordsegment

from .constants import CMUDICT
from .utils import g2p_abbr, g2p_ch


class G2pEn:
    def __init__(self):
        wordsegment.load()
        self.g2p_e = g2p_en.G2p()

    def convert(self, word):
        # 大写单词长度小于等于 3，按字母念
        if word.isupper() and len(word) <= 3 and "'" not in word:
            # e.g. "IT" => "I T"
            return g2p_abbr(word)
        # 单词在 CMU dict 中，按照 CMU dict 念
        if word.lower() in CMUDICT:
            return CMUDICT[word.lower()][0]
        # 小写 oov 长度小于等于 3，大写 oov 长度小于等于 4，按字母念
        # e.g. tts => t t s, WFST => W F S T
        if (word.islower() and len(word) <= 3) or (word.isupper() and len(word) <= 4):
            return g2p_abbr(word)
        # 其他 OOV 先转小写，用 wordsegment 分词
        # e.g. wifi => wifi, autojs => auto js
        bpes = wordsegment.segment(word.lower())
        # 无法分词则让 g2p_en 预测
        if len(bpes) == 1:
            try:
                return self.g2p_e(bpes[0])
            except TypeError:
                return []
        # 分词结果递归做 g2p
        phones = []
        for bpe in bpes:
            phones.extend(g2p_ch(bpe) if len(bpe) == 1 else self.convert(bpe))
        return [phone for phone in phones if phone.strip() != ""]


convert = G2pEn().convert
