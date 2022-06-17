import asyncio

import wikipedia_histories


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


def test_get_text_with_default_language() -> None:
    # testing with only one revision id instead of all revisions
    # passed id corresponds to 1st version of English Andrei Broder page
    text = asyncio.run(wikipedia_histories.get_texts([31820970]))
    assert text == [
        "Andrei Broder is a Research Fellow and Vice President of Emerging"
        " Search Technology for Yahoo. He previously has worked for AltaVista "
        "as the vice president of research, and for IBM Research as a Distinguished"
        " Engineer & CTO.\nHe has done research into the internet, and internet "
        "searching. He is credited with being one of the first people to develop"
        " a Captcha, while working for AltaVista.\nHe earned his PhD from Stanford"
        " University in 1985, where his advisor was Donald Knuth.\n"
        "This biographical article relating to a computer specialist is a stub."
        " You can help Wikipedia by expanding it."
    ]


def test_get_text_with_other_language() -> None:
    lang = "zh-min-nan"
    # use id of first version of an article from Min Nan wikipedia
    text = asyncio.run(wikipedia_histories.get_text(321061, lang_code=lang))
    assert text == (
        "Phoe-thai (Eng-gí: embryo) sī hoat-io̍k ê chá-kî kai-toāⁿ, "
        "tùi nn̄g he̍k-chiá siu-cheng-nn̄g kái-sí hun-lia̍t liáu-āu khái-sí, kàu i "
        "chú-iàu khì-koan hêng-sêng.\n"
    )


def test_invalid_language_code() -> None:
    lang = ""
    text = asyncio.run(wikipedia_histories.get_text(321061, lang_code=lang))
    assert text == -1
