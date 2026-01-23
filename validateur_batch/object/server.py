import jsonpath
import requests

from typing import List


class Server:
    """
    Classe regroupant les interactions avec le serveur de Terminologies FHIR de votre
    choix
    """

    def __init__(self, endpoint: str):
        """
        Args:
            endpoint: Endpoint de votre serveur de Terminologies FHIR
        """
        self.endpoint = endpoint
        self.ecl_base_url = f"{endpoint}/ValueSet/$expand?url=http://snomed.info/sct/900000000000207008?fhir_vs=ecl/" # noqa
        self.lookup_base_url = f"{endpoint}/CodeSystem/$lookup?system=http://snomed.info/sct&version=http://snomed.info/sct/900000000000207008" # noqa

    def ecl(self, ecl: str) -> List[str]:
        """Envoie une requête ECL au FTS

        Args:
            ecl: Requête ECL

        Returns:
            Liste des SCTID correspondant à la requête ECL
        """
        url = f"{self.ecl_base_url}{requests.utils.quote(ecl)}"
        response = requests.request("GET", url)
        response.raise_for_status()

        return [r.get("code", "")
                for r in response.json()["expansion"].get("contains", {})]

    def lookup(self, sctid: str) -> str:
        """Renvoie les informations d'un concept SNOMED CT

        Args:
            sctid: SCTID du concept

        Returns:
            Informations du concept `sctid`
        """
        url = f"{self.lookup_base_url}&code={sctid}"
        response = requests.request("GET", url)
        response.raise_for_status()

        return response.json()

    def get_fsn(self, sctid: str) -> str:
        """Donne le FSN du concept `sctid`

        args:
            sctid: SCTID du concept

        returns:
            FSN du concept
        """
        json = self.lookup(sctid)
        p = list(
            jsonpath.query("$.parameter[?@name == 'designation'].part[?@valueCoding.code == '900000000000003001']", json).pointers() # noqa
        )[0]

        return next(filter(lambda x: x["name"] == "value", p.resolve_parent(json)[0]))["valueString"] # noqa
