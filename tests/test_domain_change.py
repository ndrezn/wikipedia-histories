import wikipedia_histories


def test_get_history_with_default() -> None:
    data = wikipedia_histories.get_history("Andrei Broder", include_text=False)
    assert data != []


def test_get_history_with_other_domain() -> None:
    data = wikipedia_histories.get_history(
        "Andrei Broder", include_text=False, domain="fr.wikipedia.org"
    )
    assert data != []
