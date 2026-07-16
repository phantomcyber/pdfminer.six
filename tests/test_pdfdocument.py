from nose.tools import assert_equal, raises

from helpers import absolute_sample_path
from pdfminer.pdfdocument import LITERAL_XREF, PDFDocument, PDFXRefStream
from pdfminer.pdfparser import PDFParser
from pdfminer.pdftypes import PDFObjectNotFound, PDFStream


class StubXRefParser:
    def __init__(self, stream):
        self.stream = stream

    def nexttoken(self):
        return (0, None)

    def nextobject(self):
        return (0, self.stream)


class TestPdfDocument(object):

    def test_xref_stream_counts_are_bounded_by_decoded_entries(self):
        stream = PDFStream({
            'Type': LITERAL_XREF,
            'Size': 2000000,
            'Index': [10, 1000000, 20, 1000000],
            'W': [1, 1, 1],
        }, b'\x01\x02\x00\x02\x03\x00')
        xref = PDFXRefStream()

        xref.load(StubXRefParser(stream))

        assert_equal(xref.ranges, [(10, 2)])
        assert_equal(list(xref.get_objids()), [10, 11])

    @raises(PDFObjectNotFound)
    def test_get_zero_objid_raises_pdfobjectnotfound(self):
        with open(absolute_sample_path('simple1.pdf'), 'rb') as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            doc.getobj(0)

    def test_encrypted_no_id(self):
        # Some documents may be encrypted but not have an /ID key in
        # their trailer. Tests
        # https://github.com/pdfminer/pdfminer.six/issues/594
        path = absolute_sample_path('encryption/encrypted_doc_no_id.pdf')
        with open(path, 'rb') as fp:
            parser = PDFParser(fp)
            doc = PDFDocument(parser)
            assert_equal(doc.info,
                         [{'Producer': b'European Patent Office'}])
