import jsonpath
import requests

from typing import Dict, List


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
        self.lookup_path = "CodeSystem/$lookup?system=http://snomed.info/sct&version=http://snomed.info/sct/900000000000207008" # noqa
        self.lookup_base_url = f"{endpoint}/{self.lookup_path}"
        # Le "/" final évite une redirection qui ferait perdre le POST
        self.batch_url = f"{endpoint}/"

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

    def batch_lookup(self, sctids: List[str], size: int = 100) -> Dict[str, Dict]:
        """Renvoie les informations de plusieurs concepts SNOMED CT en regroupant les
        opérations $lookup dans un batch FHIR

        Args:
            sctids: SCTID des concepts, les doublons ne sont interrogés qu'une fois
            size: Nombre maximum d'opérations lookup par requête batch

        Returns:
            Dictionnaire avec pour chaque SCTID (clé) les informations correspondante
            du concept (valeur)
        """
        codes = list(dict.fromkeys(sctids))
        results = {}

        for i in range(0, len(codes), size):
            chunk = codes[i:i + size]
            bundle = {
                "resourceType": "Bundle",
                "type": "batch",
                "entry": [{"request": {"method": "GET",
                                       "url": f"{self.lookup_path}&code={sctid}"}}
                          for sctid in chunk]
            }
            response = requests.request(
                "POST", self.batch_url, json=bundle,
                headers={"Content-Type": "application/fhir+json"}
            )
            response.raise_for_status()

            # Les entrées de la réponse suivent l'ordre des entrées de la requête
            entries = response.json().get("entry", [])
            if len(entries) != len(chunk):
                raise requests.HTTPError(f"Réponse batch incomplète : {len(entries)} "
                                         f"entrée(s) pour {len(chunk)} lookup",
                                         response=response)
            for sctid, entry in zip(chunk, entries):
                status = entry["response"]["status"]
                if not status.startswith("2"):
                    raise requests.HTTPError(f"Lookup du concept {sctid} : {status}",
                                             response=response)
                results[sctid] = entry["resource"]

        return results

    def get_fsn(self, sctid: str) -> str:
        """Donne le FSN du concept `sctid`

        Args:
            sctid: SCTID du concept

        Returns:
            FSN du concept
        """
        return self._extract_fsn(self.lookup(sctid))

    def batch_get_fsn(self, sctids: List[str]) -> Dict[str, str]:
        """Donne le FSN de plusieurs concepts en regroupant les opérations $lookup
        dans un batch FHIR

        Args:
            sctids: SCTID des concepts

        Returns:
            Dictionnaire avec pour chaque SCTID (clé) le FSN du concept (valeur)
        """
        return {sctid: self._extract_fsn(json)
                for sctid, json in self.batch_lookup(sctids).items()}

    @staticmethod
    def _extract_fsn(json: Dict) -> str:
        """Extrait le FSN du résultat d'une opération $lookup

        Args:
            json: Résultat de l'opération $lookup

        Returns:
            FSN du concept
        """
        p = list(
            jsonpath.query("$.parameter[?@name == 'designation'].part[?@valueCoding.code == '900000000000003001']", json).pointers() # noqa
        )[0]

        return next(filter(lambda x: x["name"] == "value", p.resolve_parent(json)[0]))["valueString"] # noqa
