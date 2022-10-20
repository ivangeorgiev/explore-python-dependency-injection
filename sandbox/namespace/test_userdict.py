from collections import UserDict

def test_userdict():
    d = UserDict({"name": "Johhny"})
    assert "name" in d
    assert d.name == "Johnny"
    