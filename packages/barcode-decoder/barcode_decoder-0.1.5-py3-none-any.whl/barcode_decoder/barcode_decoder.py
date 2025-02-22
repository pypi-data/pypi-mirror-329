from .digi_key import decode_digi_key_barcode
from .farnell import decode_farnell_barcode
from .mouser import decode_mouser_barcode
from .tme import decode_tme_barcode
from .wurth_elektronik import decode_wurth_elektronik
from .scanner import detect_code_type

_decoders = [decode_digi_key_barcode,
             decode_farnell_barcode,
             decode_mouser_barcode,
             decode_tme_barcode,
             decode_wurth_elektronik]


def decode(barcode: str):
    """Takes a scanned barcode and returns a decoded parameters in form of a list of dictionaries"""
    result = []
    barcode = barcode.upper().rstrip()
    code_type, code = detect_code_type(barcode)
    for decoder in _decoders:
        decoded = decoder(code_type, code)
        result.append(decoded)
    return result
