from darfix.tasks.copy import DataCopy
from orangecontrib.darfix.widgets.darfixwidget import OWDarfixWidgetOneThread


class DataCopyWidgetOW(OWDarfixWidgetOneThread, ewokstaskclass=DataCopy):
    """
    Widget that creates a new dataset from a given one, and copies its data.
    """

    name = "data copy"
    icon = "icons/copy.svg"
    want_main_area = False
