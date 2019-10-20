from hypothesis_bio.blast6 import BLAST6_DEFAULT_HEADERS, BLAST6_HEADERS


def test_all_headers_is_dict():
    assert type(BLAST6_HEADERS) == dict


def test_default_headers_is_list():
    assert type(BLAST6_DEFAULT_HEADERS) == list
