import hashlib

class Candidate:
    def __init__(self, url: str):
        self._url = url
        self._sha256 = hashlib.sha256()
        self._token = self._generate_token()
        self._html = self._generate_html()

    def _generate_token(self) -> str:
        """Generate token for verification"""

        self._sha256.update(self._url.encode())
        checksum = self._sha256.hexdigest()
        intermediate = f"{self._url}|{checksum}"
        self._sha256.update(intermediate.encode())
        return self._sha256.hexdigest()
    
    def _generate_html(self) -> str:
        """Generate html snippet to put on the webpage"""

        return """<!--- Ownership verification --->
<style>.hidden {{ display: none !important; }}</style>
<input id="ownership-token" type="text" class="hidden" value="{token}" readonly></input>
<!--- End Ownership verification --->""".format(token=self._token)
    
    def get_verification_html(self) -> str:
        """Get the html snippet for verification"""

        return self._html
    
    def get_verification_token(self) -> str:
        """Get the raw token for verification"""
        
        return self._token