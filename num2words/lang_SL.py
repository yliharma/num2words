# -*- coding: utf-8 -*-
# Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.
# Copyright (c) 2013, Savoir-faire Linux inc.  All Rights Reserved.
# Copyright (c) 2015, Blaz Bregar. All Rights Reserved.

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA

# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from .lang_EU import Num2Word_EU

class Num2Word_SL(Num2Word_EU):
    def set_high_numwords(self, high):
        max = 3 + 6*len(high)

        for word, n in zip(high, range(max, 3, -6)):
            self.cards[10**n] = word + "iljard"
            self.cards[10**(n-3)] = word + "iljon"


    def setup(self):
        self.negword = "minus "
        self.pointword = "celih"
        self.errmsg_nonnum = "Only numbers may be converted to words."
        self.errmsg_toobig = "Number is too large to convert to words."
        self.exclude_title = []

        lows = ["non", "okt", "sept", "sext", "quint", "quadr", "tr", "b", "m"]
        units = ["", "un", "duo", "tre", "quattuor", "quin", "sex", "sept",
                 "okto", "novem"]
        tens = ["dez", "vigint", "trigint", "quadragint", "quinquagint",
                "sexagint", "septuagint", "oktogint", "nonagint"]
        self.high_numwords = ["zent"]+self.gen_high_numwords(units, tens, lows)
        self.mid_numwords = [(1000, "tisoč "), (900, "devetsto"), (800, "osemsto"), 
                             (700, "sedemsto"), (600, "šesto"), (500, "petsto"), (400, "štiristo"), (300, "tristo"), 
                             (200, "dvesto"), (100, "sto"),
                             (90, "devetdeset"), (80, "osemdeset"), (70, "sedemdeset"),
                             (60, "šestdeset"), (50, "petdeset"), (40, "štirideset"),
                             (30, "trideset")]
        self.low_numwords = ["dvajset", "devetnajst", "osemnajst", "sedemnajst",
                             "šestnajst", "petnajst", "štirinajst", "trinajst",
                             "dvanajst", "enajst", "deset", "devet", "osem", "sedem",
                             "šest", "pet", "štiri", "tri", "dva", "ena",
                             "nič"]
        self.ords = { "ena"    : "prvi",
                      "dve"    : "drugi",
                      "acht"    : "ach",
                      "sieben"  : "sieb",
                      "ig"      : "igs" }
        self.ordflag = False


    def merge(self, curr, next):
        ctext, cnum, ntext, nnum = curr + next

        if cnum == 1:
            if nnum < 10**6 or self.ordflag:
                return next
            ctext = ""

        if nnum > cnum:
            if nnum >= 10**6:
                if cnum > 1:
                    if ntext.endswith("d") or self.ordflag:
                        ntext += ""
                    else:
                        ntext += "ov"
                ctext += " "
            val = cnum * nnum
        else:
            if nnum < 10 < cnum < 100:
                if nnum == 1:
                    ntext = "ena"
                ntext, ctext =  ctext, ntext + "in"
            elif cnum >= 10**6:
                ctext += " "
            val = cnum + nnum

        word = ctext + ntext
        return (word, val)
            

    def to_ordinal(self, value):
        self.verify_ordinal(value)
        self.ordflag = True
        outword = self.to_cardinal(value)
        self.ordflag = False
        for key in self.ords:
            if outword.endswith(key):
                outword = outword[:len(outword) - len(key)] + self.ords[key]
                break
        return outword + "te"


    # Is this correct??
    def to_ordinal_num(self, value):
        self.verify_ordinal(value)
        return str(value) + "te"


    def to_currency(self, val, longval=True, old=False):
        if old:
            return self.to_splitnum(val, hightxt="evro/a/v", lowtxt="stotin/a/i/ov",
                                    jointxt="in",longval=longval)
        return super(Num2Word_SL, self).to_currency(val, jointxt="in",
                                                    longval=longval)

    def to_year(self, val, longval=True):
        if not (val//100)%10:
            return self.to_cardinal(val)
        return self.to_splitnum(val, hightxt="hundert", longval=longval)


            
n2w = Num2Word_SL()
to_card = n2w.to_cardinal
to_ord = n2w.to_ordinal
to_ordnum = n2w.to_ordinal_num


def main():
    for val in [ 1, 11, 12, 21, 31, 33, 71, 80, 81, 91, 99, 100, 101, 102, 155,
             180, 300, 308, 832, 1000, 1001, 1061, 1100, 1500, 1701, 3000,
             8280, 8291, 150000, 500000, 1000000, 2000000, 2000001,
             -21212121211221211111, -2.121212, -1.0000100]:
        n2w.test(val)

    n2w.test(1325325436067876801768700107601001012212132143210473207540327057320957032975032975093275093275093270957329057320975093272950730)
    print n2w.to_currency(112121)
    print n2w.to_year(2000)

if __name__ == "__main__":
    main()

