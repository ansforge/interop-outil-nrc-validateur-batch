import json
import pytest

from typing import Callable, Dict


def pytest_addoption(parser):
    parser.addoption("--endpoint", action="store")


@pytest.fixture
def batch_lookup_callback() -> Callable:
    """Fabrique le callback `responses` d'une requête batch de lookup : les codes de
    `concepts` renvoient leur réponse, les autres codes une erreur 404"""
    def factory(concepts: Dict[str, Dict]) -> Callable:
        def callback(request):
            entry = []
            for e in json.loads(request.body)["entry"]:
                code = e["request"]["url"].split("&code=")[-1]
                if code in concepts:
                    entry.append({"resource": concepts[code],
                                  "response": {"status": "200 OK"}})
                else:
                    entry.append({"resource": {"resourceType": "OperationOutcome"},
                                  "response": {"status": "404 Not Found"}})
            return 200, {}, json.dumps({"resourceType": "Bundle",
                                        "type": "batch-response", "entry": entry})

        return callback

    return factory
