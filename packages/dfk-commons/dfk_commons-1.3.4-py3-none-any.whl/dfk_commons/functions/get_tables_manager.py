from dfk_commons.classes.TablesManager import TablesManager


def get_tables_manager(isProd, isDup = False):
    return TablesManager(isProd, isDup)
