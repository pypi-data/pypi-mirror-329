from .barcode_decoder import decode


def pretty_print(decoded_barcode):
    print('==============================')
    for result in decoded_barcode:
        if result:
            print('----')
            print(result)


def main():
    print("Barcode Decoder, press Enter to exit")
    while True:
        barcode = input("Barcode? ")
        if len(barcode) <= 1:
            break
        results = decode(barcode)
        pretty_print(results)


if __name__ == '__main__':
    main()
