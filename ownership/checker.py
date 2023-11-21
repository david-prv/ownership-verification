from ownership.candidate import Candidate
from html.parser import HTMLParser

class Checker(HTMLParser):
    def __init__(self, web: Candidate):
        self._web = web
        self._found_token = None
        super().__init__()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Overrides HTMLParser.handle_starttag to search for token"""

        if tag.lower() == "input" and "id" in dict(attrs):
            _id = [x for x in attrs if x[0] == "id" and x[1] == "ownership-token"]
            _value = [x for x in attrs if x[0] == "value"]

            if len(_id) > 1 or len(_value) > 1:
                raise ValueError("Multiple tokens found")
            
            if len(_id) < 1 or len(_value) < 1:
                raise ValueError("Could not find token")
            
            self._found_token = _value[0][1]

    def verify_ownership(self) -> bool:
        """Verify parsed token with candidate token"""
        
        assert self._found_token != None

        real_token = self._web.get_verification_token()
        return self._found_token == real_token