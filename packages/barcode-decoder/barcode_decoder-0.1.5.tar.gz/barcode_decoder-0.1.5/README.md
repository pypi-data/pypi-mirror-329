# barcode-decoder
Barcode and QR decoder

Simple application for decoding barcodes and QR codes from various distributors and converting them to standardized output.

## Usage
### Installation
`pip install barcode_decoder`

### Command line usage
`$ barcode_decoder`

### Usage as library
```
from barcode_decoder import barcode_decoder

result = barcode_decoder.decode(barcode_string)
```

### Currently supported distributors:
- Farnell
- Mouser
- TME
- Wurth Elektronik

### Setting your scaner
You need to enable Code Identifier in your scanner settings.

### Testing
Application is tested using Gryphon D432

