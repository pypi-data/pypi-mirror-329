from rest_framework import serializers
import requests
from plugin import InvenTreePlugin
from plugin.mixins import LabelPrintingMixin
from . import PLUGIN_VERSION
import requests
import io

class Gprinter(LabelPrintingMixin, InvenTreePlugin):
    """Gprinter plugin which provides a 'fake' label printer endpoint."""

    NAME = 'Gprinter Label Printer'
    SLUG = 'Gprinterlabelprinter'
    TITLE = 'Gprinter Label Printer'
    DESCRIPTION = 'A Gprinter plugin which provides a (fake) label printer interface'
    AUTHOR = 'InvenTree contributors'
    VERSION = '0.3.0'

    class PrintingOptionsSerializer(serializers.Serializer):
        """Serializer to return printing options."""
        amount = serializers.IntegerField(required=False, default=1)

    def print_label(self, **kwargs):
        # Test that the expected kwargs are present
        print(f'Printing Label: {kwargs["filename"]} (User: {kwargs["user"]})')

        pdf_data = kwargs['pdf_data']

        pdf_file_like = io.BytesIO(pdf_data)
    
        files = {
            'file': (f'{kwargs["filename"]}.pdf', pdf_file_like, 'application/pdf')
        }
        
        response = requests.post("http://192.168.31.198:6666/print_pdf", files=files)

        print("服务器返回结果：", response.text)