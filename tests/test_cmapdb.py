from nose.tools import assert_raises

from pdfminer.cmapdb import CMapDB


class TestCMapDB:
    def test_rejects_path_shaped_cmap_names(self):
        for name in ('../payload', r'..\payload', 'nested/payload'):
            with assert_raises(CMapDB.CMapNotFound):
                CMapDB._load_data(name)
