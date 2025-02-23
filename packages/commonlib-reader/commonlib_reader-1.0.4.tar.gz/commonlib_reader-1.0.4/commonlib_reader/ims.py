from typing import List, Union
from commonlib_reader.utils import attributes_list_to_dict, get_code


class IMS:
    _ims_codes = []

    """Class for IMS objects.

    properties:
    Facility (str) - Name of facility
    IMSType (str) - Type of IMS
    Alias (str) - Facility name aliases
    isValid (bool) - True if IMS is in operation
    """

    def __init__(self, data: Union[str, dict]):
        """Instance constructor for IMS object. End-users should use static method IMS.from_facility()

        Args:
            data (str,dict): Facility name or data dictionary to populate instance data attributes.

        Raises:
            ValueError: If input data is not a dict.
        """
        if isinstance(data, str):
            data = IMS.from_facility(data)._data

        if not isinstance(data, dict):
            raise ValueError("Input data must be a dict from codetable")

        self._data = data
        self._attributes = attributes_list_to_dict(self._data["attributes"])

        self.isValid = data["isValid"]

        self.Facility = ""
        self.IMSType = ""
        self.Alias = ""

        for attr in self._data["attributes"]:
            self.__setattr__(attr["definitionName"], attr["displayValue"])

    @staticmethod
    def from_facility(facility: str) -> "IMS":
        """Get IMS instance from STID code.

        Args:
            facility (str): Facility code

        Raises:
            ValueError: Not able to instantiate IMS object from input facility code.

        Returns:
            IMS: IMS instance
        """
        if facility is None or len(facility) == 0:
            raise ValueError(
                "Facility must be provided. Empty strings are not allowed."
            )
        ims = IMS.get_ims_list(facility=facility)
        if len(ims) == 1:
            return ims[0]

        raise ValueError(f"Not able to get IMS object for facility {facility}")

    @classmethod
    def _get_ims_codes(cls) -> List["IMS"]:
        """Get list of IMS instance of entries in code library ApplicationIMS. Caches locally in memory.

        Returns:
            List[IMS]: list of IMS instance from entries in code library ApplicationIMS.
        """
        if cls._ims_codes is None or len(cls._ims_codes) == 0:
            cls._ims_codes = get_code("ApplicationIMS")

        return [IMS(x) for x in cls._ims_codes]

    @staticmethod
    def get_ims_list(facility: str = "") -> List["IMS"]:
        """Get list of IMS objects.

        Args:
            facility (str, optional): Facility. Defaults to "", which will get list of all entries defined in lib.

        Returns:
            List[IMS]: list of IMS objects
        """
        i = IMS._get_ims_codes()
        if len(facility) > 0:
            return [x for x in i if x.Facility == facility]

        return i

    @staticmethod
    def get_source(facility: str) -> str:
        """Get IMS name for a facility.

        Args:
            facility (str): Name of facility.

        Raises:
            ValueError: If facility input is invalid, i.e., empty.

        Returns:
            str: Name of IMS
        """

        l_ims = IMS.from_facility(facility=facility)
        return l_ims.Alias

    @staticmethod
    def get_type(facility: str) -> str:
        """Get IMS type for a facility.

        Args:
            facility (str): Name of facility

        Raises:
            ValueError: If facility input is invalid, i.e., empty.

        Returns:
            str: Type of IMS
        """
        l_ims = IMS.from_facility(facility=facility)
        return l_ims.IMSType
