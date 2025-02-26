import os
import shutil
import zipfile

from lxml import etree
import cairosvg
import uuid

import milgeo.utils.milsymbol as milsymbol

def create_kmz_archive(folder_kmz_path: str, folder_path: str, base_file_name: str, part_number: int) -> None:
    kmz_file_name: str = f"{base_file_name}-part-{part_number}.kmz"
    kmz_file_path: str = f"{folder_path}/{kmz_file_name}"
    with open(kmz_file_path, 'wb') as kmz_file:
        with zipfile.ZipFile(kmz_file, 'w') as kmz:
            for root, _, files in os.walk(folder_kmz_path):
                for file in files:
                    kmz.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), folder_kmz_path))
    # remove temporary folder
    shutil.rmtree(folder_kmz_path)
    
def save_kml_document(kml: etree._Element, folder_kmz_path: str, base_file_name: str, part_number: int) -> None:
    kml_string: bytes = etree.tostring(kml, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    chunk_file_name: str = f"{base_file_name}-part-{part_number}.kml"
    full_path: str = f"{folder_kmz_path}/{chunk_file_name}"
    with open(full_path, 'wb') as file:
        file.write(kml_string)

def generate_svg(sidc: str) -> str:
    return milsymbol.milsymbol.ms.Symbol.new(sidc).asSVG() # type: ignore

DEFAULT_SVG_SIDC = "10011500000000000000"
def save_svg_as_png(sidc_text: str, png_file_name: str, default_sidc: str = DEFAULT_SVG_SIDC) -> None:
    try:
        symbol_svg = generate_svg(sidc_text)
    except Exception as e:
        print(f"Error while creating symbol for SIDC {sidc_text}: {e}")
        try:
            symbol_svg = generate_svg(default_sidc)
        except Exception as e:
            print(f"Error while creating symbol for provided default SIDC {default_sidc}: {e}")
            symbol_svg = generate_svg(DEFAULT_SVG_SIDC)
    cairosvg.svg2png(bytestring=symbol_svg.encode('utf-8'), write_to=png_file_name)

def add_style_to_document(document: etree._Element, unique_image_id: uuid.UUID) -> None:
    style_id = f"{unique_image_id}-style"
    style = etree.SubElement(document, "Style", id=style_id)
    icon_style = etree.SubElement(style, "IconStyle")
    icon = etree.SubElement(icon_style, "Icon")
    href = etree.SubElement(icon, "href")
    href.text = f'files/{unique_image_id}.png'

def add_style_url_to_placemark(geometry_element: etree._Element, unique_image_id: uuid.UUID) -> None:
    style_url = etree.SubElement(geometry_element, "styleUrl")
    style_url.text = f"#{unique_image_id}-style"