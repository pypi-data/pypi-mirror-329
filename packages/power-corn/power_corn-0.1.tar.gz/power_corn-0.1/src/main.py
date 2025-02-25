from .scripts import simplev7, get_power_info
from .modules.utilities import create_tables_if_not_exists


def main():
    create_tables_if_not_exists()
    simplev7.main()
    get_power_info.main()
