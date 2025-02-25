from enum import Enum

class IonType(str, Enum):
    ION_TYPE_AUTO_REGISTERED = "ION_TYPE_AUTO_REGISTERED"
    ION_TYPE_POST_REGISTERED = "ION_TYPE_POST_REGISTERED"
    ION_TYPE_PURE_SERVER = "ION_TYPE_PURE_SERVER"

    def __str__(self):
        return self.value