from commonlib_reader.utils import get_code

# from commonlib_reader.utils import attributes_list_to_dict


class Unit:
    _units = []

    def __init__(self, data: dict):
        self.name = ""
        self.description = ""

        self.identity = ""
        self.quantity = ""

        if isinstance(data, str):
            s = [x for x in Unit.get_units() if x.name == data]
            if len(s) > 0:
                data = s[0]._data
            else:
                raise ValueError(f"No unit named {data} found.")

        if isinstance(data, dict):
            self._data = data
            # self._attributes = attributes_list_to_dict(self._data["attributes"])

            for key in data.keys():
                if key == "attributes":
                    for attr in data["attributes"]:
                        self.__setattr__(attr["definitionName"], attr["displayValue"])
                else:
                    self.__setattr__(key, data[key])

    @classmethod
    def get_units(cls):
        """Get list of Unit objects of entries in code library. Caches locally in memory.

        Returns:
            List[IMS]: list of Unit objects from entries in code library.
        """
        if cls._units is None or len(cls._units) == 0:
            cls._units = get_code("UnitOfMeasure")

        return [Unit(x) for x in cls._units]
