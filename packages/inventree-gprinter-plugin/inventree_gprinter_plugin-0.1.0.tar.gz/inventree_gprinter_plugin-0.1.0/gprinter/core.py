import usb.core
import usb.util
from rest_framework import serializers
from PIL import Image
import math
from pdf2image import convert_from_bytes
from InvenTree.settings import BASE_DIR
from plugin import InvenTreePlugin
from plugin.mixins import LabelPrintingMixin

from . import PLUGIN_VERSION

def pdf_to_image(pdf_data, dpi=140):
    """
    用 pdf2image 将 PDF 指定页转换为 PIL Image。
    - page_number: 要转换的页码，从 1 开始
    - dpi: 分辨率，自己可根据打印需求调整
    """
    # pdf2image 的 convert_from_path，会返回一个 Image list，每页一个 PIL Image
    pages = convert_from_bytes(pdf_data, dpi=dpi)
    return pages[0]  # 返回 PIL Image 对象

def get_image_data(pil_image):
    """
    使用 PIL 读取图像、先转灰度，再用带抖动的方式转成 1-bit 黑白图。
    然后逐行构造打印机使用的位图数据（每字节对应 8 个像素）。
    """
    # 1) 打开图像并转为灰度
    img_gray = pil_image.convert('L')

    # 2) 将灰度图转换为 1-bit 图 (黑白二值)，PIL 默认使用 Floyd-Steinberg 抖动
    dithered_img = img_gray.convert('1', dither=Image.NONE)
    # 如果想关闭抖动，可用: dithered_img = img.convert('1', dither=Image.NONE)

    width, height = dithered_img.size
    width_in_bytes = math.ceil(width / 8)

    bitmap_data = []
    for y in range(height):
        row_data = []
        for byte_index in range(width_in_bytes):
            one_byte = 0
            mask = 0x80  # 从最高位 (binary 10000000) 开始
            # 计算该字节实际覆盖的像素起止
            start_x = byte_index * 8
            end_x = (byte_index + 1) * 8
            real_end_x = min(end_x, width)  # 若超出宽度，用 width 代替

            # 3. 遍历当前字节覆盖的所有有效像素
            for x in range(start_x, real_end_x):
                pixel = dithered_img.getpixel((x, y))  # 黑=0，白=255
                # 我们希望白=1，所以是 if pixel == 255 => (one_byte ^= mask)
                if pixel == 255:
                    one_byte ^= mask
                mask >>= 1

            # 4. 如果本字节覆盖的范围小于 8 (说明到了图像右边界)，
            #    剩下的 bit 都设为 1(白)，以免打印机边缘出现黑线。
            leftover_bits = end_x - real_end_x  # 实际少了多少像素
            while leftover_bits > 0 and mask != 0:
                one_byte ^= mask  # 补充剩余 bit = 1 (白)
                mask >>= 1
                leftover_bits -= 1

            row_data.append(one_byte)
        bitmap_data.append(row_data)

    return bitmap_data

def build_command_buffer(bitmap_data):
    """
    根据 TSC 指令拼接指令和位图数据，最终返回要发送的字节流。
    """
    height_in_dots = len(bitmap_data)
    width_in_bytes = len(bitmap_data[0]) if height_in_dots > 0 else 0

    # 将二维数组拍平成一维
    flat_data = [byte for row in bitmap_data for byte in row]

    # 拼接 TSC 命令的字符串部分
    command_str = (
        "SIZE 40 mm,15 mm\r\n"
        "CLS\r\n"
        f"BITMAP 5,5,{width_in_bytes},{height_in_dots},0,"
    ).encode("utf-8")

    command_barcode = (
        'PRINT 1\r\n'
        'END\r\n'
    ).encode("utf-8")

    # 最终要发送的字节流
    # 先拼接指令字符串，再拼接图像位图数据，最后拼接后续指令
    buffer = command_str + bytes(flat_data) + command_barcode
    return buffer

def print_data(data_buffer):
    """
    通过 PyUSB，将 data_buffer 写入到指定的 USB 打印机设备中。
    """
    # Node.js 里写的是 usb.findByIds(8137, 8214)
    # 8137 (0x1FC9), 8214 (0x2016)
    dev = usb.core.find(idVendor=0x0471, idProduct=0x0055)
    if dev is None:
        raise ValueError("找不到指定的 USB 打印机 (VID=0x0471, PID=0x0055).")

    try:
        # 如有需要先分离内核驱动
        if dev.is_kernel_driver_active(0):
            dev.detach_kernel_driver(0)

        # 设置配置，如出现“Resource busy”错误可检查这里或 detach_kernel_driver
        dev.set_configuration()

        # 获取接口
        cfg = dev.get_active_configuration()
        interface = cfg[(0, 0)]

        # 查找 OUT 端点
        out_endpoint = usb.util.find_descriptor(
            interface,
            custom_match=lambda e: (
                usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
            )
        )
        if out_endpoint is None:
            raise ValueError("没有找到 USB OUT 端点。")

        # 写数据到该端点
        # 一次性写出，如果长度过大，需要分段写
        out_endpoint.write(data_buffer)

    finally:
        # 释放资源
        usb.util.release_interface(dev, 0)
        usb.util.dispose_resources(dev)
        # 如果之前 detach 了内核驱动，这里可以考虑 attach 回去
        # dev.attach_kernel_driver(0)

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
        img = pdf_to_image(pdf_data, dpi=136)
        # 读取并生成位图数据
        data = get_image_data(img)

        # 拼接 TSC 指令和位图数据的字节流
        cmd_buffer = build_command_buffer(data)
        print(cmd_buffer)

        # 发送给打印机
        print_data(cmd_buffer)