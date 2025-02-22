import unittest
from src.barcode_decoder.digi_key import decode_digi_key_barcode
from src.barcode_decoder.scanner import CodeType


class TestDigiKeyBarcodeDecoder(unittest.TestCase):
    def test_datamatrix_string_decode(self):
        str1 = '[)>^06]pSAM14954CT-ND]1PLSHM-110-01-L-DH-A-S-K-TR]kPO22000140]1K74797379]10K88169536]11K1]4LCR]Q3]11ZPICK]12Z9597381]13Z213254]20Z0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
        decoded = decode_digi_key_barcode(CodeType.DataMatrix, str1.upper())
        self.assertEqual(decoded.distributor, "DigiKey")
        self.assertEqual(decoded.order_number['number'], 'PO22000140')
        self.assertEqual(decoded.invoice, None)
        self.assertEqual(decoded.don, 'SAM14954CT-ND')
        self.assertEqual(decoded.mon, 'LSHM-110-01-L-DH-A-S-K-TR')
        self.assertEqual(decoded.quantity, 3)
        self.assertEqual(decoded.LOT, None)
        self.assertEqual(decoded.date_code, None)
        self.assertEqual(decoded.manufacturer, None)

    def test_datamatrix_string2_decode(self):
        str1 = '[)>^06]j88EFC224.BD844ABB.8A542FF7.7F3C82260D83]P455-2290-ND]1P03ZR-8M-P]9D2017.11]14Z171101]1T278565]4LCN]11ZPREPACK]15Z1.0.1]12Z1678834]q50]13Z0]20Z000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
        decoded = decode_digi_key_barcode(CodeType.DataMatrix, str1.upper())
        self.assertEqual(decoded.distributor, "DigiKey")
        self.assertEqual(decoded.invoice, None)
        self.assertEqual(decoded.don, '455-2290-ND')
        self.assertEqual(decoded.mon, '03ZR-8M-P')
        self.assertEqual(decoded.quantity, 50)
        self.assertEqual(decoded.LOT, '278565')
        self.assertEqual(decoded.date_code, '2017.11')
        self.assertEqual(decoded.manufacturer, None)


if __name__ == '__main__':
    unittest.main()
