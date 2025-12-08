from Constants import Constants
import pendulum

def form_xml_file_name() -> str:
    import os
    os.makedirs(Constants.XML_DIR, exist_ok=True)
    return os.path.join(Constants.XML_DIR, f"{Constants.XML_PREFIX}{pendulum.now().format('YYYY-MM-DD_HH-mm-ss')}.xml")