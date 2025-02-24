from xmlbind import XmlRoot, XmlAttribute, XmlElement

from .fee import Fee


class TimeStandardRef(XmlRoot):
    time_standard_list_id: int = XmlAttribute(name="timestandardlistid", required=True)
    fee: Fee = XmlElement(name="FEE")
    marker: str = XmlAttribute(name="marker")
