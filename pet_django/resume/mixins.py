import re


class DisplayMixin:
    def __str__(self):
        for attr in self.__dict__:
            if re.match(r".*_name", attr):
                return self.__getattribute__(attr)
            elif re.match(r".*_experience", attr):
                if len(self.__getattribute__(attr).split()) > 3:
                    return " ".join(self.__getattribute__(attr).split()[:3]) + "..."
                return " ".join(self.__getattribute__(attr).split()[:3])
