"""Initialize the alation_service subpackage of cdh_lava_core package"""

# allow absolute import from the root folder
# whatever its name is.
# from cdh_lava_core.az_storage_service import az_storage_queue


import sys  # don't remove required for error handling
import os


# Import from sibling directory ..\data_boot_camp_service
OS_NAME = os.name

sys.path.append("..")
if OS_NAME.lower() == "nt":
    print("data_boot_camp: windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..\\..")))
else:
    print("data_boot_camp: non windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../../..")))

__all__ = [
    "data_boot_camp"
    ]
