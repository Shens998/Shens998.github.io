# -*- coding: utf-8 -*-
"""Exercise identity validation and preserve-good-snapshot failure handling."""
from pathlib import Path
from unittest.mock import patch
from contextlib import redirect_stderr
import io
from email.message import Message
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import update_scholar as updater

def sample(name='Shi Shen', affiliation='Beijing Normal University', values=(200,150,20,15,30,25)):
    cells=''.join('<td class="gsc_rsb_std">'+str(value)+'</td>' for value in values)
    return '<div id="gsc_prf_in">'+name+'</div><div class="gsc_prf_il">'+affiliation+'</div><table id="gsc_rsb_st"><thead><th>All</th><th>Since 2021</th></thead><tbody><tr>'+cells+'</tr></tbody></table>'
class ScholarTests(unittest.TestCase):
    def test_columns_and_since_year(self):
        data=updater.parse_snapshot(sample())
        self.assertEqual(data['metrics']['citations'],{'all':200,'since':150})
        self.assertEqual(data['metrics']['h_index'],{'all':20,'since':15})
        self.assertEqual(data['metrics']['i10_index'],{'all':30,'since':25})
        self.assertEqual(data['since_year'],2021)
    def test_chinese_identity_and_formatted_numbers(self):
        data=updater.parse_snapshot(sample('沈石','北京师范大学',('2,000','1,500',20,15,30,25)))
        self.assertEqual(data['metrics']['citations']['all'],2000)
    def test_invalid_identity_and_captcha_rejected(self):
        for content in (sample('Someone Else'),sample(affiliation='Other University'),'<html>CAPTCHA</html>'):
            with self.subTest(content=content):
                with self.assertRaises(ValueError):updater.parse_snapshot(content)
    def test_invalid_recent_column_rejected(self):
        with self.assertRaises(ValueError):updater.parse_snapshot(sample(values=(100,200,20,15,30,25)))
    def test_declared_response_encoding(self):
        response=io.BytesIO((sample()+'<p>café</p>').encode('iso-8859-1'))
        response.headers=Message();response.headers['Content-Type']='text/html; charset=iso-8859-1'
        self.assertEqual(updater.parse_snapshot(updater.read_document(response))['metrics']['h_index']['all'],20)
    def test_oversized_response_rejected(self):
        response=io.BytesIO(b'x'*2_000_001)
        with self.assertRaises(ValueError):updater.read_document(response)
    def test_fetch_failure_preserves_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'assets').mkdir();snapshot=root/'assets/scholar.json';snapshot.write_text('{"sentinel":"preserve"}')
            before=snapshot.read_bytes()
            with patch.object(updater,'ROOT',root),patch.object(updater,'urlopen',side_effect=OSError('offline')),patch.object(sys,'argv',['update_scholar.py']),redirect_stderr(io.StringIO()):
                self.assertEqual(updater.main(),2)
            self.assertEqual(snapshot.read_bytes(),before)
if __name__=='__main__':unittest.main()
