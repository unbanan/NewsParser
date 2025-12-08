import xml.etree.ElementTree as ET
import html
from Extraction.Record import Record

class XMLParser:
    def __init__(self):
        pass
    
    @staticmethod
    def _dfs(v, records) -> None:
        for child in v:
            if child.tag == "item":
                records.append(child)
            else:
                XMLParser._dfs(child, records)

    @staticmethod
    def make_record(child) -> Record:
        title = child.find("title").text
        if title:
            title = html.unescape(title)
        
        description = child.find("description").text
        if description:
            description = html.unescape(description)
        
        return Record(
            title=title,
            link=child.find("link").text,
            description=description,
            pubDate=child.find("pubDate").text,
            guid=child.find("guid").text,
            categories=[category.text for category in child.findall("category")],
        )

    @staticmethod
    def parse(file_path: str) -> list[Record]:
        tree = ET.parse(file_path)
        root = tree.getroot()
        records = []
        XMLParser._dfs(root, records)
        extracted_records = []
        for record in records:
            extracted_records.append(XMLParser.make_record(record))
                
        return extracted_records
