# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "mishkal-hebrew",
#     "nakdimon-onnx",
# ]
#
# [tool.uv.sources]
# mishkal-hebrew = { path = "../" }
# ///
"""
wget https://github.com/thewh1teagle/nakdimon-onnx/releases/download/v0.1.0/nakdimon.onnx
uv run examples/with_nakdimon.py
"""

from nakdimon_onnx import Nakdimon
from mishkal import phonemize
from mishkal.utils import remove_niqqud

nakdimon = Nakdimon("nakdimon.onnx")
text = """
כָּל עֶרֶב יָאִיר (הַשֵּׁם הַמָּלֵא וּמְקוֹם הָעֲבוֹדָה שֶׁלּוֹ שְׁמוּרִים בַּמַּעֲרֶכֶת) רָץ 20 קִילוֹמֶטֶר. הוּא מְסַפֵּר לִי שֶׁזֶּה מְנַקֶּה לוֹ אֶת הָרֹאשׁ אַחֲרֵי הָעֲבוֹדָה, "שָׁעָה וָחֵצִי בְּלִי עֲבוֹדָה, אִשָּׁה וִילָדִים" כְּמוֹ שֶׁהוּא מַגְדִּיר זֹאת. אֲבָל אַחֲרֵי הַמִּקְלַחַת הוּא מַתְחִיל בְּמָה שֶׁנִּתָּן לְכַנּוֹת הָעֲבוֹדָה הַשְּׁנִיָּה שֶׁלּוֹ: לִמְצֹא לוֹ קוֹלֵגוֹת חֲדָשׁוֹת לָעֲבוֹדָה, כִּי יָאִיר הוּא כַּנִּרְאֶה הַמֶּלֶךְ שֶׁל "חָבֵר מֵבִיא חָבֵר" בְּיִשְׂרָאֵל.
"""
text = remove_niqqud(text)
dotted_text = nakdimon.compute(text)
print(dotted_text)

print('Undotted: ', phonemize(text))
print('Dotted: ', phonemize(dotted_text))