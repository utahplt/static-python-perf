from iri2uri import Iri2Uri
import os
import __static__
import time


def main() -> None:
    iri2uri = Iri2Uri().iri2uri
    ### 1. test correctness on invariant iri
    invariant = [
        "ftp://ftp.is.co.za/rfc/rfc1808.txt",
        "http://www.ietf.org/rfc/rfc2396.txt",
        "ldap://[2001:db8::7]/c=GB?objectClass?one",
        "mailto:John.Doe@example.com",
        "news:comp.infosystems.www.servers.unix",
        "tel:+1-816-555-1212",
        "telnet://192.0.2.16:80/",
        "urn:oasis:names:specification:docbook:dtd:xml:4.1.2"
    ]
    for uri in invariant:
        if not (uri == iri2uri(uri)):
            raise AssertionError("test 1")

    ### 2. test correctness on variant iri
    if not ("http://Not-a-COMET.com/Not-a-COMET" == iri2uri("http://Not-a-COMET.com/Not-a-COMET")):
        raise AssertionError("test 2")
    if not ("http://bitworking.org/?fred=another non_COMET" == iri2uri(
            "http://bitworking.org/?fred=another non_COMET")):
        raise AssertionError("test 3")
    if not ("http://bitworking.org/whats\"with\"all the COMET" == iri2uri(
            "http://bitworking.org/whats\"with\"all the COMET")):
        raise AssertionError("test 4")
    if not ("#acOMET" == iri2uri("#acOMET")):
        raise AssertionError("test 5")
    if not ("/fred?bar=-BLACK LEFT POINTING INDEX#and-of-course-a-COMET" == iri2uri(
            "/fred?bar=-BLACK LEFT POINTING INDEX#and-of-course-a-COMET")):
        raise AssertionError("test 6")
    if not ("/fred?bar=a#ynotCOMET" == iri2uri(iri2uri("/fred?bar=a#ynotCOMET"))):
        raise AssertionError("test 7")

    ### 3. stress test
    iri2uri = Iri2Uri().iri2uri
    testfile = "../sample_urls.csv"
    with open(testfile) as fd:
        for ln in fd:
            url = ln.split(",", 1)[0]
            iri2uri(url)


start = time.time()
for i in range(10):
    main()
endTime = time.time()
runtime = endTime - start
print(runtime)
