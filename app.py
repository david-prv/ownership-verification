from ownership.candidate import Candidate
from ownership.checker import Checker
from ownership.results import GOOD_RESULT, BAD_RESULT
from typing import Any
import requests
import sys

def main() -> Any:
    if len(sys.argv) <= 1:
        print("Usage: python app.py <url> [verify]")
        return

    _url = sys.argv[1]
    _check = len(sys.argv) > 2 and str(sys.argv[2]).lower() == "verify"

    try:
        _candidate = Candidate(_url)

        # check if the given url contains the verification
        # snippet and verify the placed token to be valid
        if _check:
            print("checking... ", end="", flush=True)

            # verifier is just an html parser
            verifier = Checker(_candidate)
            verifier.feed(requests.get(_url).text)

            # append result to previous line
            print(GOOD_RESULT if verifier.verify_ownership() else BAD_RESULT)
            return
        
        # generate a new verification html snipped
        # that has to be placed on the webpage to verify
        print(_candidate.get_verification_html())
    except (ValueError, AssertionError) as err:
        print(BAD_RESULT)
        print(f"\nerror: {err}")

if __name__ == "__main__":
    main()