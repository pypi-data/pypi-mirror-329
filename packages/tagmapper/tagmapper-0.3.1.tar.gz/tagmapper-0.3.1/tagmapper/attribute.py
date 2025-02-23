class Attribute:
    """
    Attribute class
    """

    def __init__(self, data):
        if not isinstance(data, dict):
            raise ValueError("Input data must be a dict")

        self.name = ""
        if "attribute_name" in data.keys():
            self.name = data["attribute_name"]
        elif "Attribute_Name" in data.keys():
            self.name = data["Attribute_Name"]

        self.tag = ""
        if "TAG_ID" in data.keys():
            self.tag = data["TAG_ID"]
        elif "Tag_Id" in data.keys():
            self.tag = data["Tag_Id"]

        self.source = ""
        if "source" in data.keys():
            self.source = data["source"]
        elif "Attribute_Source_Name" in data.keys():
            self.source = data["Attribute_Source_Name"]

    def __str__(self):
        return f"{self.name} : {self.tag}"
