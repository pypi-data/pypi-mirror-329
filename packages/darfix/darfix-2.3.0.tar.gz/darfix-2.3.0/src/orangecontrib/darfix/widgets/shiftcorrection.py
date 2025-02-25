from ewoksorange.gui.orange_imports import Input
from ewoksorange.gui.orange_imports import Output
from silx.gui import qt
from silx.gui.colors import Colormap

from darfix import dtypes
from darfix.gui.shiftCorrectionWidget import ShiftCorrectionDialog
from darfix.tasks.shiftcorrection import ShiftCorrection

from .darfixwidget import OWDarfixWidgetOneThread


class ShiftCorrectionWidgetOW(OWDarfixWidgetOneThread, ewokstaskclass=ShiftCorrection):
    """
    Widget to make the shift correction of a dataset.
    """

    name = "shift correction"
    description = "A widget to perform shift correction"
    icon = "icons/shift_correction.svg"
    want_main_area = True
    want_control_area = False

    _ewoks_inputs_to_hide_from_orange = ("shift",)

    # Inputs
    class Inputs:
        colormap = Input("colormap", Colormap)

    # Outputs
    class Outputs:
        colormap = Output("colormap", Colormap)

    def __init__(self):
        super().__init__()
        qt.QLocale.setDefault(qt.QLocale("en_US"))

        self._widget = ShiftCorrectionDialog(parent=self)
        self.mainArea.layout().addWidget(self._widget)
        self._widget.okSignal.connect(self.execute_shift_correction)

    def handleNewSignals(self) -> None:
        dataset = self.get_task_input_value("dataset", None)
        if dataset is not None:
            self.setDataset(dataset, pop_up=True)

        # Do not call super().handleNewSignals() to prevent propagation

    def setDataset(self, dataset: dtypes.Dataset, pop_up=True):
        self._widget.setDataset(dataset)
        if pop_up:
            self.open()

    @Inputs.colormap
    def setColormap(self, colormap):
        self._widget.setStackViewColormap(colormap)

    def task_output_changed(self) -> None:
        self.Outputs.colormap.send(self._widget.mainWindow.getStackViewColormap())
        self.close()

    def execute_shift_correction(self):
        self.set_default_input("shift", self._widget.mainWindow.shift.tolist())
        self.execute_ewoks_task()
