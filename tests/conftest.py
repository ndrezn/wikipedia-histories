import pytest


def _scrub_content_encoding(response):
    headers = response.get("headers", {})
    headers.pop("Content-Encoding", None)
    headers.pop("content-encoding", None)
    return response


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "decode_compressed_response": True,
        "before_record_response": _scrub_content_encoding,
    }
