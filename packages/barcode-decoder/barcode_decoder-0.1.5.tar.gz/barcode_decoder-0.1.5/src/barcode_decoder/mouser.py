from .scanner import CodeType
from .result import Result


def decode_mouser_barcode(code_type: CodeType, barcode):
    if code_type == CodeType.DataMatrix:
        return decode_datamatrix(barcode)


def decode_datamatrix(barcode):
    if barcode.startswith('>[)>06]') or barcode.startswith("[)>^06]") or barcode.startswith("[)>06]"):
        data = barcode.removesuffix('^D').split(']')
        result = Result(distributor="Mouser")
        order_invoice_position = None
        for param in data:
            if param.startswith('K'):
                result.order_number = {"number": param.removeprefix('K')}
            elif param.startswith('14K'):
                order_invoice_position = int(param.removeprefix('14K'))
                result.order_number["position"] = order_invoice_position
            elif param.startswith('1P'):
                result.mon = param.removeprefix('1P')
            elif param.startswith('Q'):
                result.quantity = float(param.removeprefix('Q'))
            elif param.startswith('11K'):
                result.invoice = {'number': param.removeprefix('11K'), 'position': order_invoice_position}
            elif param.startswith('4L'):
                result.coo = param.removeprefix('4L')
            elif param.startswith('1V'):
                result.manufacturer = param.removeprefix('1V')
        return result if result.is_valid() else None
