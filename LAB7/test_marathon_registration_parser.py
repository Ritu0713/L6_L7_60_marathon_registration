from hypothesis import given, strategies as st
from marathon_registration_parser import format_bib_name, parse_finish_time, average_split

@given(st.text() | st.none())
def test_format_bib_name_no_crash(s):
    try:
        format_bib_name(s)
    except Exception as e:
        assert False, f"format_bib_name crashed with: {e}"

@given(st.text() | st.none())
def test_parse_finish_time_no_crash(s):
    try:
        parse_finish_time(s)
    except Exception as e:
        assert False, f"parse_finish_time crashed with: {e}"

@given(st.text() | st.none())
def test_average_split_no_crash(s):
    try:
        average_split(s)
    except Exception as e:
        assert False, f"average_split crashed with: {e}"
