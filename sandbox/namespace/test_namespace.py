from .namespace import Namespace

def test_can_create_instance():
    ns = Namespace()

def test_attributes_passed_to_constructor():
    attributes = {"name":"Jacob"}
    ns = Namespace(**attributes)
    assert ns.name == "Jacob"

def test_can_set_attribute():
    ns = Namespace()
    ns.property = "house"
    assert ns.property == "house"

def test_can_access_dictionary():
    ns = Namespace()
    ns.property = "land"
    assert ns["property"] == "land"
    ns["color"] = "green"
    assert ns.color == "green"
