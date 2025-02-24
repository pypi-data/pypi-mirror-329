from xmlbind import XmlRoot, XmlAttribute


class PointTable(XmlRoot):
    name: str = XmlAttribute(name="name", required=True)
    point_table_id: int = XmlAttribute(name="pointtableid")
    version: str = XmlAttribute(name="version", required=True)
