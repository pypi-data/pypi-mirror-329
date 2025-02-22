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

import os
import re

import jieba
import pycantonese
from pycantonese.jyutping.characters import _get_words_characters_to_jyutping
from pypinyin import load_phrases_dict, load_single_dict
from pypinyin.contrib.tone_convert import to_finals, to_initials

from .constants import CMUDICT, IPA_EN, IPA_ZH, POSTNASALS


def g2p_ch(ch):
    """
    Convert a single English character to phonemes.
    """
    ch = ch.lower()
    assert len(ch) == 1
    # In abbreviations, "A" should be pronounced as "EY1", not "AH0".
    return CMUDICT[ch][1] if ch == "a" else CMUDICT[ch][0]


def g2p_abbr(word):
    """
    Convert an English abbreviation to phonemes.
    """
    return [phone for ch in word for phone in g2p_ch(ch)]


def load_dict():
    """
    Load dictionary.
    """
    # from pypinyin.constants import PINYIN_DICT
    # print(hex(ord("为")), PINYIN_DICT[ord("为")])
    dirname = os.path.dirname(__file__)
    for line in open(f"{dirname}/dict/single.txt", encoding="utf-8"):
        char, pinyins = line.strip().split(maxsplit=1)
        load_single_dict({ord(char): pinyins})
    for line in open(f"{dirname}/dict/phrases.txt", encoding="utf-8"):
        word, pinyins = line.strip().split(maxsplit=1)
        jieba.add_word(word, freq=None, tag=None)
        pinyins = pinyins.split()
        assert len(word) == len(pinyins)
        load_phrases_dict({word: [[pinyin] for pinyin in pinyins]})


def parse_jyutping(jyutping):
    """
    Parse an jyutping (for Cantonese Chinese) into initial, final and tone.
    """
    jyutping = pycantonese.parse_jyutping(jyutping)
    assert len(jyutping) == 1
    initial = jyutping[0].onset
    final = jyutping[0].nucleus + jyutping[0].coda
    tone = jyutping[0].tone
    return initial, final, tone


def parse_pinyin(pinyin, strict=False):
    """
    Parse a pinyin (for Mandarin Chinese) into initial, final and tone.
    """
    if pinyin[:-1] in POSTNASALS:
        initial = ""
        final = pinyin[:-1]
    else:
        initial = to_initials(pinyin, strict=strict)
        final = to_finals(pinyin, strict=strict)
    tone = pinyin[-1]
    return initial, final, tone


def convert_jyut(word):
    """
    Convert the word into jyutping.
    """
    words_to_jyutping, chars_to_jyutping = _get_words_characters_to_jyutping()
    try:
        jyutping = words_to_jyutping[word]
    except KeyError:
        jyutping = ""
        for char in word:
            try:
                jyutping += chars_to_jyutping[char]
            except KeyError:
                jyutping = None
                break
    if jyutping is not None:
        jyutping = re.findall(r"[\D]+\d|\D", jyutping)
    return jyutping


def apply_tone(phones, tone):
    if isinstance(phones, str):
        phones = [phones]
    return [phone.replace("0", tone) for phone in phones]


def pinyin2ipa(initial, final, tone):
    tone = IPA_ZH["tones"][tone]
    pinyin = initial + final
    if pinyin in IPA_ZH["interjections"]:
        return apply_tone(IPA_ZH["interjections"][pinyin], tone)
    if pinyin in IPA_ZH["syllabic_consonants"]:
        return apply_tone(IPA_ZH["syllabic_consonants"][pinyin], tone)

    phones = []
    if initial != "":
        phones.append(IPA_ZH["initials"][initial])
    if initial in {"zh", "ch", "sh", "r", "z", "c", "s"} and final == "i":
        phones.extend(apply_tone(IPA_ZH["finals"]["-i"], tone))
    else:
        phones.extend(apply_tone(IPA_ZH["finals"][final], tone))
    return phones


def phone2ipa(phone):
    if phone[-1].isdigit():
        phone, stress = phone[:-1], phone[-1]
        return IPA_EN[stress] + IPA_EN[phone]
    return IPA_EN[phone]
