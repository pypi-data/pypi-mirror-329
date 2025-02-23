from typing import List, Union
from commonlib_reader.utils import get_code, get_code_param, query_sql
import re

# from commonlib_reader.utils import attributes_list_to_dict

_cache = {}
_cache["TagType"] = {}
_cache["TagCategory"] = {}
_cache["TagFormat"] = {}


class TagFormatElement:
    """A class representing the elements constructing a tag number.

    Attributes:
        description (str)
        name (str)
        IsValid (bool)
        IsRequired (bool)
        IsSelected (bool)

    """

    def __init__(self, data: dict):
        """
        Initializes a TagFormatElement object.

        Parameters:
            data (dict): Data containing different properties of a tag format element.
        """
        self._data = data

        self.description = data["Description"]
        self.name = data["Name"]
        self.IsValid = bool(data["IsValid"])
        self.IsRequired = bool(data["Required"])
        self.IsSelected = bool(data["SelectFlag"])

    def get_TagFormat(self) -> "TagFormat":
        tag_format_id = self._data["TagFormat_ID"]
        res = query_sql(f"Select * from tagformat where Id = '{tag_format_id}'")
        return TagFormat.get_tagformat(
            res[0]["Description"], res[0]["Scope"], res[0]["TagCategory"]
        )

    @staticmethod
    def get_TagFormatElements(
        tag_format: Union["TagFormat", str]
    ) -> List["TagFormatElement"]:
        if isinstance(tag_format, TagFormat):
            tag_format_id = tag_format.get_id()
        else:
            tag_format_id = tag_format

        # q = f"SELECT * FROM [TagFormatElement] WHERE IsValid = 1 AND IsReleaseReady = 1 AND SelectFlag = 'true' AND TagFormat_ID = '{tag_format_id}'"

        q = f"SELECT * FROM [TagFormatElement] WHERE IsValid = 1 AND IsReleaseReady = 1 AND TagFormat_ID = '{tag_format_id}'"
        sql_result = query_sql(q)
        return [TagFormatElement(x) for x in sql_result]


class TagFormat:
    """
    A class that represents the format of a tag number within the context of a Facility. Each tag number shall belong to a Tag Type.

    Attributes:
        inst_code (str): Installation code.
        description (str): Description of the tag format.
        tag_category (str): Tag category this format belongs to.
        syntax (str): The syntax structure of the tag format.
        regex (str): The regular expression pattern representing the tag format.
        regex_grouped (str): Grouped regular expression pattern for the tag format.
    """

    def __init__(self, data: dict, inst_code: str):
        """
        Initializes a TagFormat object.

        Parameters:
            data (dict): Data containing different properties of a tag format.
            inst_code (str): Installation code for this tag format.
        """
        self._data = data

        # Cache tagformatelements
        self._tfe = None

        # self._attributes = attributes_list_to_dict(self._data["attributes"])

        self.inst_code = inst_code
        self.description = data["description"]

        self.tag_category = ""
        self.syntax = ""
        self.regex = ""
        self.regex_grouped = ""

        for attr in self._data["attributes"]:
            if attr["definitionName"] == "TagCategory":
                self.tag_category = attr["displayValue"]
            elif attr["definitionName"] == "Syntax":
                self.syntax = attr["displayValue"]
            elif attr["definitionName"] == "Regex":
                self.regex = attr["displayValue"]
            elif attr["definitionName"] == "RegexGrouped":
                self.regex_grouped = attr["displayValue"]

    def __str__(self):
        return f"{self.description} - {self.tag_category}"

    def is_valid(self, tagNo: str):
        return re.fullmatch(self.regex, tagNo)

    def get_id(self) -> int:
        """Get tagformat identity.

        Returns:
            int: Numeric identity for TagFormat. Used to cross reference databases.
        """
        res = query_sql(
            f"SELECT Id from [TagFormat] where [TagFormat].[Identity] = '{self._data['identity']}'"
        )
        return res[0]["Id"]

    def get_tagformat_elements(self) -> List[TagFormatElement]:
        """Get TagFormatElement objects for this TagFormat.

        Returns:
            List[TagFormatElement]: List of TagFormatElement objects.
        """
        if self._tfe is None:
            self._tfe = TagFormatElement.get_TagFormatElements(self)

        return self._tfe

    def get_regex_grouped_named(self) -> str:
        """Substitute codes with descriptions in grouped regex

        Returns:
            str: Regex grouped string where generic regex group names are replaced with tag format element description.
        """
        regex_group_named = self.regex_grouped
        for e in self.get_tagformat_elements():
            regex_group_named = regex_group_named.replace(
                f"?<e{e.name}>", f"?<{e.description}>"
            )

        return regex_group_named

    def split_tag(self, tagNo: str) -> dict:
        # Change naming pattern for groups in commonlib-regex to match python re format
        py_pattern = re.sub(r"\(\?<(\w+)>", r"(?P<\1>", self.regex_grouped)
        matches = re.match(py_pattern, tagNo)

        # Tag format element descriptions may contain space and can not be used as group name in regex. Instead create dict where description is key.
        d = {}
        for e in self.get_tagformat_elements():
            group_name = f"e{e.name}"
            if group_name in matches.groupdict().keys():
                d[e.description] = matches.group(group_name)

        return d

    @staticmethod
    def get_tagformat(
        description: str, inst_code: str, tag_category: str
    ) -> "TagFormat":
        """
        Retrieve a tag format for a given description, installation code and tag category.

        Parameters:
            description (str): Description of the tag format to retrieve.
            inst_code (str): Installation code of the requested tag format.
            tag_category (str): Category of the requested tag format.

        Returns:
            TagFormat: The requested tag format object.
        """
        t = TagCategory.get_category(inst_code=inst_code, name=tag_category)
        return t[0].get_format(description)


class TagType:
    """
    A class that represents a tag type, which is pertinent to a tag category and
    associated with a particular facility.

    Attributes:
        inst_code (str): The facility code the tag type is associated with.
        name (str): The name of the tag type.
        description (str): A description of the tag type.
        is_valid (bool): A flag indicating whether the tag type is valid.
        tag_category (str): The category under which this tag type falls.
        STID_tag_Count (int): The number of STID tags associated with this tag type.
    """

    def __init__(self, data: dict, inst_code: str):
        """
        Initializes a TagType object with provided data and installation code.

        Parameters:
            data (dict): Data containing different properties of a tag type.
            inst_code (str): Installation code for which this tag type applies.
        """
        self._data = data
        self.inst_code = inst_code

        self.name = self._data["name"]
        self.description = self._data["description"]
        self.is_valid = self._data["isValid"]
        self.tag_category = ""

        for attr in self._data["attributes"]:
            if attr["definitionName"] == "STIDTagCount":
                self.STID_tag_Count = int(attr["displayValue"])
            elif attr["definitionName"] == "TagCategory":
                self.tag_category = attr["displayValue"]

    def __str__(self):
        return f"{self.name} - {self.description}"

    @staticmethod
    def get_tagtype(name: str, inst_code: str, tag_category: str) -> "TagType":
        """
        Retrieve a tag type object based on the name, installation code, and tag category.

        Parameters:
            name (str): Name of the tag type to retrieve.
            inst_code (str): Installation code specific to the tag type.
            tag_category (str): Category to which the tag type belongs.

        Returns:
            TagType: The TagType object matching the criteria.
        """
        t = TagCategory.get_category(inst_code=inst_code, name=tag_category)
        return t[0].get_type(name)

    @staticmethod
    def get_tagtype_no_cache(
        name: str, inst_code: str, tag_category: str = ""
    ) -> "TagType":
        """
        Retrieve tag types for the given name and installation code without using the cache. Optionally filter by tag category.

        Parameters:
            name (str): The name of the tag type to retrieve.
            inst_code (str): Installation code specific to the tag type.
            tag_category (str, optional): Optional category to filter the tag types.

        Returns:
            List[TagType]: A list of TagType objects matching the criteria.
        """

        params = {}
        params["scope"] = inst_code
        params["name"] = name

        tag_types = [
            TagType(x, inst_code=inst_code)
            for x in get_code_param("TagType", params=params)
        ]

        if tag_category:
            tag_types = [x for x in tag_types if x.tag_category == tag_category]

        return tag_types

    @staticmethod
    def get_master_tagtype(
        name: str, tag_category: str = "", technology: str = "Oil&Gas"
    ) -> "TagType":
        """
        Retrieve master tag types based on name, category, and technology. If name is empty,
        sorts by name and returns all. If name is provided, filters by name.

        Parameters:
            name (str): The name of the master tag type to retrieve. Can be empty to retrieve all.
            tag_category (str, optional): Category to filter the master tag types. Can be empty to not filter.
            technology (str, optional): Technology to filter the master tag types, defaults to 'Oil&Gas'.

        Returns:
            List[TagType]: A list of TagType objects matching the criteria.
        """
        return_value = []
        d = _get_master_type_data()
        for k in range(0, len(d)):
            for att in d[k]["attributes"]:
                if att["definitionName"] == "Technology":
                    currTechnology = att["displayValue"]
                    break

            include_technology = (
                technology is None
                or len(technology) == 0
                or currTechnology == technology
            )

            include_category = tag_category is None or len(tag_category) == 0
            if not include_category:
                for att in d[k]["attributes"]:
                    if (
                        att["definitionName"] == "TagCategory"
                        and att["displayValue"] == tag_category
                    ):
                        include_category = True
                        break

            if include_category and include_technology:
                return_value.append(TagType(d[k], currTechnology))

        if not name:
            return_value.sort(key=lambda x: x.name)
        else:
            return_value = [x for x in return_value if x.name == name]

        return return_value

    @staticmethod
    def get_master_tagtype_mappings(
        name: str, tag_category: str = "", technology: str = "Oil&Gas"
    ):
        """
        Retrieve mappings of the master tag types based on name, category,
        and technology. Raises a ValueError if no relevant mappings are found
        or if more than one master tag type is matching name, tag category and technology input.

        Parameters:
            name (str): The name of the master tag type to search for mappings.
            tag_category (str, optional): Category to filter the tag type mappings. Can be empty to not filter.
            technology (str, optional): Technology to filter the tag type mappings, defaults to 'Oil&Gas'.

        Returns:
            List: A list of mapped tag types.

        Raises:
            ValueError: If no master tag type is found, or if multiple master tag types are found.
        """
        mtt = TagType.get_master_tagtype(
            name=name, tag_category=tag_category, technology=technology
        )

        if len(mtt) == 0:
            raise ValueError("No master tag type found")

        if len(mtt) > 1:
            raise ValueError("Multiple master tag types found. Currently not supported")

        sql = f"""SELECT tt.scope Facility,tt.Name LocalTagType, tt.tagcategory LocalTagCategory FROM MasterTagType mtt 
                  inner join TagType tt on tt.MasterTagType_ID=mtt.id 
                  where mtt.tagcategory='{mtt[0].tag_category}' and mtt.Name ='{mtt[0].name}' and mtt.Technology='{mtt[0].inst_code}' and tt.isValid='True'
                  order by tt.name, tt.scope"""

        res = query_sql(sql=sql)
        mapped_types = []
        [
            mapped_types.extend(
                TagType.get_tagtype_no_cache(
                    x["LocalTagType"], x["Facility"], x["LocalTagCategory"]
                )
            )
            for x in res
        ]
        return mapped_types


class TagCategory:
    """
    A class representing a Facility specific category of tag types.

    Attributes:
        inst_code (str): Installation code for the facilitye the TagCategory is associated with.
        name (str): Name of the tag category.
        description (str): Description of the tag category.
        is_valid (bool): Flag indicating whether the tag category is considered valid.
        TagCategoryId (int): Unique identifier of the tag category.
        TagCategoryDlg (str): Additional dialog information associated with the tag category.
        IndividFlag (str): A flag indicating individual characteristics for the category.
        SapFlCategory (str): Corresponding SAP functional location category.
    """

    def __init__(self, data, inst_code):
        """
        Initializes a TagCategory object.

        Parameters:
            data (dict): Data containing different properties of a tag category.
            inst_code (str): Installation code for which this tag category applies.
        """
        self._data = data
        self.inst_code = inst_code

        self.name = self._data["name"]
        self.description = self._data["description"]
        self.is_valid = self._data["isValid"]

        for attr in self._data["attributes"]:
            if attr["definitionName"] == "TagCategoryId":
                self.TagCategoryId = int(attr["displayValue"])
            elif attr["definitionName"] == "TagCategoryDlg":
                self.TagCategoryDlg = attr["displayValue"]
            elif attr["definitionName"] == "IndividFlag":
                self.IndividFlag = attr["displayValue"]
            elif attr["definitionName"] == "SapFlCategory":
                self.SapFlCategory = attr["displayValue"]

        self._types = []
        self._formats = []

    def get_formats(self) -> List[TagFormat]:
        """Get tag formats for this specific tag category.

        Returns:
            List[TagType]: List of TagFormat objects belonging to this category.
        """
        if self._formats is None or len(self._formats) == 0:
            tag_formats = [
                TagFormat(x, self.inst_code) for x in _get_format_data(self.inst_code)
            ]
            self._formats = [x for x in tag_formats if x.tag_category == self.name]

        return self._formats

    def get_format(self, description: str) -> TagFormat:
        """Get single tag format for this specific tag category.

        Args:
            format (str): Description (name) of tag format.

        Returns:
            TagFormat: Tag format object
        """
        for curr_type in self.get_formats():
            if curr_type.description == description:
                return curr_type

        return None

    def get_types(self) -> List[TagType]:
        """Get tag types for this specific tag category.

        Returns:
            List[TagType]: List of TagType objects belonging to this category.
        """
        if self._types is None or len(self._types) == 0:
            tag_types = [
                TagType(x, self.inst_code) for x in _get_type_data(self.inst_code)
            ]
            self._types = [x for x in tag_types if x.tag_category == self.name]
            self._types.sort(key=lambda x: x.name)

        return self._types

    def get_type(self, type: str) -> Union[TagType, None]:
        """Get single type from this specific tag category.

        Args:
            type (str): Type name

        Returns:
            Union[TagType, None]: TagType if found, else None.
        """
        for curr_type in self.get_types():
            if curr_type.name == type:
                return curr_type

        return None

    def __str__(self):
        return f"{self.TagCategoryId}:{self.name} - {self.description}"

    @staticmethod
    def get_category(inst_code: str, name="") -> List["TagCategory"]:
        categories = _get_category_data(inst_code=inst_code)
        tc = [TagCategory(x, inst_code=inst_code) for x in categories]
        tc.sort(key=lambda x: x.TagCategoryId)
        if name is None:
            pass
        elif isinstance(name, str) and len(name) > 0:
            tc = [x for x in tc if x.name == name or x.description == name]

        return tc


def _get_category_data(inst_code: str) -> List[dict]:
    """Get code table of tag categories for a facility from commonlibapi.

    Args:
        inst_code (str): STID installation code.

    Returns:
        List[dict]: Data for each tag category.
    """
    global _cache

    if inst_code not in _cache["TagCategory"].keys():
        _cache["TagCategory"][inst_code] = get_code("TagCategory", scope=inst_code)

    return _cache["TagCategory"][inst_code]


def _get_type_data(inst_code: str) -> List[dict]:
    """Get code table of tag types for an installation from commonlibapi.

    Args:
        inst_code (str): STID installation code.

    Returns:
        List[dict]: Data for each tag type.
    """
    global _cache

    if inst_code not in _cache["TagType"].keys():
        _cache["TagType"][inst_code] = get_code("TagType", scope=inst_code)

    return _cache["TagType"][inst_code]


def _get_master_type_data(scope="") -> List[dict]:
    """Get code table of master tag types from commonlibapi.

    Returns:
        List[dict]: Data for each tag type.
    """
    global _cache

    if "MasterTagType" not in _cache.keys():
        _cache["MasterTagType"] = get_code("MasterTagType")

    return _cache["MasterTagType"]


def _get_format_data(inst_code: str) -> List[dict]:
    """Get code table of tag formats for an installation from commonlibapi.

    Args:
        inst_code (str): STID installation code.

    Returns:
        List[dict]: Data for each format.
    """
    global _cache

    if inst_code not in _cache["TagFormat"].keys():
        _cache["TagFormat"][inst_code] = get_code("TagFormat", scope=inst_code)

    return _cache["TagFormat"][inst_code]
