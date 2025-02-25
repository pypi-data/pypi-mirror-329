from __future__ import annotations

from ewokscore.missing_data import MISSING_DATA
from ewoksorange.gui.orange_imports import Input
from silx.gui.colors import Colormap

from darfix.gui.zSumWidget import ZSumWidget
from darfix.tasks.zsum import ZSum

from .darfixwidget import OWDarfixWidgetOneThread


class ZSumWidgetOW(OWDarfixWidgetOneThread, ewokstaskclass=ZSum):
    """
    Widget that compute and display the Z-sum of a dataset
    """

    name = "z sum"
    icon = "icons/zsum.svg"
    want_main_area = True
    want_control_area = False

    _ewoks_inputs_to_hide_from_orange = ("indices", "dimension")

    # Inputs
    class Inputs:
        colormap = Input("colormap", Colormap)

    def __init__(self):
        super().__init__()

        self._widget = ZSumWidget(parent=self)
        self.mainArea.layout().addWidget(self._widget)
        # connect signal / slot
        self._widget.sigFilteringRequested.connect(self._filterStack)
        self._widget.sigResetFiltering.connect(self._resetFilterStack)

    @Inputs.colormap
    def setColormap(self, colormap):
        self._widget.setColormap(colormap)

    def handleNewSignals(self) -> None:
        dataset = self.get_task_input_value("dataset", None)
        if dataset is not None:
            self._widget.setDataset(dataset)
            self.open()
        return super().handleNewSignals()

    def task_output_changed(self):
        z_sum = self.get_task_output_value("zsum", MISSING_DATA)
        if z_sum is not MISSING_DATA:
            self._widget.setZSum(z_sum)

    def _filterStack(self, dim, val):
        self.set_default_input("indices", self._widget.indices)
        self.set_default_input("dimension", (dim, val))
        self.execute_ewoks_task()

    def _resetFilterStack(self):
        self.set_default_input("indices", None)
        self.set_default_input("dimension", None)
        self.execute_ewoks_task()
