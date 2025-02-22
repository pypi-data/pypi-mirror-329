import unittest
from src.barcode_decoder.mouser import (decode_mouser_barcode)
from src.barcode_decoder.scanner import CodeType


class TestMouserBarcodeDecoder(unittest.TestCase):
    def test_string_decode(self):
        str1 = '>[)>06]K21105000]14K004]1PDR331-513AE]q4]11K060439500]4LCN]1VBourns'
        decoded = decode_mouser_barcode(CodeType.DataMatrix, str1.upper())
        self.assertEqual(decoded.distributor, "Mouser")
        self.assertEqual(decoded.order_number['number'], '21105000')
        self.assertEqual(decoded.order_number['position'], 4)
        self.assertEqual(decoded.invoice['number'], '060439500')
        self.assertEqual(decoded.invoice['position'], 4)
    #    self.assertEqual(decoded['distributor_order_number']['don'], None)
        self.assertEqual(decoded.mon, 'DR331-513AE')
        self.assertEqual(decoded.quantity, 4)
        self.assertEqual(decoded.manufacturer, 'BOURNS')

    def test_string2_decode(self):
        barcode_str = '>[)>06]K21105000]14K019]1PB82432C1105J000]q2]11K060439500]4LHU]1VEPCOS / TDK'
        decoded = decode_mouser_barcode(CodeType.DataMatrix, barcode_str.upper())
        self.assertEqual(decoded.distributor, "Mouser")
        self.assertEqual(decoded.order_number['number'], '21105000')
        self.assertEqual(decoded.order_number['position'], 19)
        self.assertEqual(decoded.invoice['number'], '060439500')
        self.assertEqual(decoded.invoice['position'], 19)
    #    self.assertEqual(decoded['distributor_order_number']['don'], None)
        self.assertEqual(decoded.mon, 'B82432C1105J000')
        self.assertEqual(decoded.quantity, 2)
        self.assertEqual(decoded.manufacturer, 'EPCOS / TDK')

    def test_string3_decode(self):
        barcode_str = '>[)>06]K21105000]14K016]1PTYA2520123R3M-10]q5]11K060439500]4LCN]1VLaird Performance Materials'
        decoded = decode_mouser_barcode(CodeType.DataMatrix, barcode_str.upper())
        self.assertEqual(decoded.distributor, "Mouser")
        self.assertEqual(decoded.order_number['number'], '21105000')
        self.assertEqual(decoded.order_number['position'], 16)
        self.assertEqual(decoded.invoice['number'], '060439500')
        self.assertEqual(decoded.invoice['position'], 16)
    #    self.assertEqual(decoded['distributor_order_number']['don'], None)
        self.assertEqual(decoded.mon, 'TYA2520123R3M-10')
        self.assertEqual(decoded.quantity, 5)
        self.assertEqual(decoded.manufacturer, 'LAIRD PERFORMANCE MATERIALS')

    def test_string4_decode(self):
        barcode_str = '[)>^06]K26161557]14K054]1PPESD3V3S2UT,215]q40]11K069009053]4LCN]1VNexperia^d'
        decoded = decode_mouser_barcode(CodeType.DataMatrix, barcode_str.upper())
        self.assertEqual(decoded.distributor, "Mouser")
        self.assertEqual(decoded.order_number['number'], '26161557')
        self.assertEqual(decoded.order_number['position'], 54)
        self.assertEqual(decoded.invoice['number'], '069009053')
        self.assertEqual(decoded.invoice['position'], 54)
    #    self.assertEqual(decoded['distributor_order_number']['don'], None)
        self.assertEqual(decoded.mon, 'PESD3V3S2UT,215')
        self.assertEqual(decoded.quantity, 40)
        self.assertEqual(decoded.manufacturer, 'NEXPERIA')

    def test_string5_decode(self):
        barcode_str = '[)>^06]k28614977]14K002]1PEMIF03-SIM02M8]Q15]11K073216369]4LCN]1VSTMicro^d'
        decoded = decode_mouser_barcode(CodeType.DataMatrix, barcode_str.upper())
        self.assertEqual(decoded.distributor, "Mouser")
        self.assertEqual(decoded.order_number['number'], '28614977')
        self.assertEqual(decoded.order_number['position'], 2)
        self.assertEqual(decoded.invoice['number'], '073216369')
        self.assertEqual(decoded.invoice['position'], 2)
    #    self.assertEqual(decoded['distributor_order_number']['don'], None)
        self.assertEqual(decoded.mon, 'EMIF03-SIM02M8')
        self.assertEqual(decoded.quantity, 15)
        self.assertEqual(decoded.coo, 'CN')
        self.assertEqual(decoded.manufacturer, 'STMICRO')

    def test_datamatrix_string6_decode(self):
        barcode_str = '[)>06]K20070071]14K019]1PERJ-UP3F3302V]q10]11K058646908]4LJP]1VPanasonic'
        decoded = decode_mouser_barcode(CodeType.DataMatrix, barcode_str.upper())
        self.assertEqual(decoded.distributor, "Mouser")
        self.assertEqual(decoded.order_number['number'], '20070071')
        self.assertEqual(decoded.order_number['position'], 19)
        self.assertEqual(decoded.invoice['number'], '058646908')
        self.assertEqual(decoded.invoice['position'], 19)
    #    self.assertEqual(decoded['distributor_order_number']['don'], None)
        self.assertEqual(decoded.mon, 'ERJ-UP3F3302V')
        self.assertEqual(decoded.quantity, 10)
        self.assertEqual(decoded.coo, 'JP')
        self.assertEqual(decoded.manufacturer, 'PANASONIC')


if __name__ == '__main__':
    unittest.main()
