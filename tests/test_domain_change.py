import asyncio

import pytest

from src import wikipedia_histories


def test_get_history_with_default() -> None:
    data = wikipedia_histories.get_history("Andrei Broder", include_text=False)
    assert data != []


def test_get_history_with_other_domain() -> None:
    data = wikipedia_histories.get_history(
        "Andrei Broder", include_text=False, domain="fr.wikipedia.org"
    )
    assert data != []


def test_wrong_domain_raises_ConnectionError() -> None:
    data = wikipedia_histories.get_history(
        "Andrei Broder", include_text=False, domain="a11.wikipedia.org"
    )
    assert data == -1


def test_simple_extract_lang_code_from_domain() -> None:
    domain = "en.wikipedia.org"
    lang_code = wikipedia_histories.extract_lang_code_from_domain(domain)
    assert lang_code == "en"


def test_invalid_lang_code_returns_empty_string() -> None:
    domain = "a11.wikipedia.org"
    lang_code = wikipedia_histories.extract_lang_code_from_domain(domain)
    assert lang_code == ""


def test_complex_extract_lang_code_from_domain() -> None:
    domain = "zh-min-nan.wikipedia.org"
    lang_code = wikipedia_histories.extract_lang_code_from_domain(domain)
    assert lang_code == "zh-min-nan"


@pytest.mark.vcr
def test_get_text_with_default_language() -> None:
    # testing with only one revision id instead of all revisions
    # passed id corresponds to 1st version of English Andrei Broder page
    text = asyncio.run(wikipedia_histories.get_texts([31820970]))
    assert len(text) == 1
    assert text[0] is not None and text[0] != -1
    assert "Andrei Broder" in text[0]


@pytest.mark.vcr
def test_get_text_with_other_language() -> None:
    lang = "zh-min-nan"
    # use id of first version of an article from Min Nan wikipedia
    text = asyncio.run(wikipedia_histories.get_text(321061, lang_code=lang))
    assert text == (
        "Phoe-thai (Eng-gí: embryo) sī hoat-io̍k ê chá-kî kai-toāⁿ, "
        "tùi nn̄g he̍k-chiá siu-cheng-nn̄g kái-sí hun-lia̍t liáu-āu khái-sí, kàu i "
        "chú-iàu khì-koan hêng-sêng.\n"
    )


@pytest.mark.vcr
def test_invalid_language_code() -> None:
    lang = ""
    text = asyncio.run(wikipedia_histories.get_text(321061, lang_code=lang))
    assert text == -1


@pytest.mark.vcr
def test_get_text_raw_html() -> None:
    html_text = asyncio.run(wikipedia_histories.get_text(321061, lang_code="zh-min-nan", raw_html=True))
    assert "<p" in html_text


@pytest.mark.vcr
def test_integration() -> None:
    domain = "tr.wikipedia.org"
    data_tr = wikipedia_histories.get_history(
        "Crazy Mohan", include_text=False, domain=domain
    )
    data_en = wikipedia_histories.get_history("Crazy Mohan", include_text=False)
    assert data_tr != data_en
