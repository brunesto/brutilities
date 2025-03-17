from io import StringIO
from src.trs import *


input1="""
bla bla bla
"""
expected1="""
bli bli bli
"""

def test_in_between():
    output = StringIO()
    replacements={"bla":"bli"}
    tr_strings_stream(StringIO(input1), output, replacements,buffer_size=6)
    assert output.getvalue()==expected1


def test_small_buffer():
    output = StringIO()
    replacements={"bla":"bli"}
    tr_strings_stream(StringIO(input1), output, replacements,buffer_size=2)
    assert output.getvalue()==expected1


