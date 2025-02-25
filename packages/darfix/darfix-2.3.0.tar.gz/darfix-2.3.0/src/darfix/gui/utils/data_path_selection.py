from __future__ import annotations

import logging

from silx.gui import icons
from silx.gui import qt

from darfix.core.datapathfinder import DataPathFinder
from darfix.core.datapathfinder import UnsolvablePatternError
from darfix.core.datapathfinder import get_first_group
from darfix.core.datapathfinder import get_last_group
from darfix.gui.utils.data_path_completer import DataPathLineEditWithCompleter

_logger = logging.getLogger(__name__)


class DataPathSelection(qt.QGroupBox):
    """
    Widget to help user select HDF5 data paths
    """

    sigPatternChanged = qt.Signal(str)
    """"
    Emit when the data path (pattern) change. Can be an empty string in the case no pattern was defined
    """

    def __init__(
        self,
        parent: qt.QWidget | None = None,
        pattern: str | None = None,
        title: str = "data path",
        allowed_keywords: tuple = (),
        completer_display_dataset: bool = False,
    ) -> None:
        """
        :param pattern: data path pattern
        :param title: title to give to this QGroupBox
        :param allowed_keywords: keywords that can be used by the data path finder
        :param completer_display_dataset: if True then completer will not display path to dataset. Default: False.
        """
        super().__init__(parent)
        self.setLayout(qt.QGridLayout())

        if pattern is None:
            pattern = ""

        # callback to call to generate the first example
        self._dataPathFinder = DataPathFinder(
            file_=None,
            pattern=pattern,
        )
        self._defaultPattern = pattern
        self.setTitle(title)

        # pattern
        self._patternLabel = qt.QLabel(text="pattern")
        self.layout().addWidget(self._patternLabel, 0, 0, 1, 1)
        self._patternLabel.setSizePolicy(qt.QSizePolicy.Fixed, qt.QSizePolicy.Fixed)

        self._patternQLE = DataPathLineEditWithCompleter(
            allowed_keywords=allowed_keywords,
            completer_display_dataset=completer_display_dataset,
        )
        self._patternQLE.setText(pattern)
        self.layout().addWidget(self._patternQLE, 0, 1, 1, 2)
        self._patternQLE.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Fixed)
        self._dataPathStatus = qt.QLabel()
        self.layout().addWidget(self._dataPathStatus, 0, 3, 1, 1)
        self._dataPathStatus.setSizePolicy(qt.QSizePolicy.Fixed, qt.QSizePolicy.Fixed)

        # reset
        style = qt.QApplication.style()
        self._resetPB = qt.QPushButton(
            "reset", icon=style.standardIcon(qt.QStyle.SP_DialogResetButton)
        )
        self._resetPB.setSizePolicy(qt.QSizePolicy.Fixed, qt.QSizePolicy.Fixed)
        self.layout().addWidget(self._resetPB, 0, 4, 1, 1)

        # example solved from the first scan entry
        self._exampleLabel = qt.QLabel("example")
        self.layout().addWidget(self._exampleLabel, 1, 0, 1, 1)
        self._exampleQLE = qt.QLineEdit("")
        self._exampleQLE.setReadOnly(True)
        self._exampleQLE.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Fixed)
        self.layout().addWidget(self._exampleQLE, 1, 1, 1, 2)

        # connect signal / slot
        self._patternQLE.editingFinished.connect(self._updateDataFinderPattern)
        self._patternQLE.editingFinished.connect(self._patternChanged)
        self._resetPB.released.connect(self._resetPattern)

        # set up
        self._updateExample()

    def _patternChanged(self):
        self.sigPatternChanged.emit(self._patternQLE.text())

    def _updateStatusIcon(self):
        style = qt.QApplication.style()

        if self._dataPathFinder.file is None:
            icon = style.standardIcon(qt.QStyle.SP_TitleBarContextHelpButton)
            tooltip = "no file set"
        elif self._dataPathFinder.can_be_solved:
            icon = style.standardIcon(qt.QStyle.SP_DialogYesButton)
            tooltip = "data path is valid"
        else:
            tooltip = "data path is invalid"
            icon = style.standardIcon(qt.QStyle.SP_DialogNoButton)
        self._dataPathStatus.setPixmap(icon.pixmap(qt.QSize(16, 16)))
        self._dataPathStatus.setToolTip(tooltip)

    def _updateDataFinderPattern(self):
        try:
            self._dataPathFinder.pattern = self._patternQLE.text()
        except UnsolvablePatternError:
            # in the case the pattern cannot be solved.
            # Note: in this particular use case the '_dataPathStatus' will also display a specific icon.
            pass
        finally:
            self._updateExample()

    def _resetPattern(self):
        if self._defaultPattern is not None:
            self.setPattern(self._defaultPattern, store_as_default=False)
        self._updateExample()

    def setLabelExample(self, label: str):
        self._exampleLabel.setText(label)

    def setPattern(self, pattern: str | None, store_as_default: bool = False):
        # in the case we don't want metadata for example
        # we might want the pattern to be None
        if pattern is None:
            pattern = ""
        if not isinstance(pattern, str):
            raise TypeError(
                f"pattern should be an instance of str. Got {type(pattern)}"
            )
        self._patternQLE.setText(pattern)
        try:
            self._updateDataFinderPattern()
        except Exception as e:
            _logger.error(f"Failed to update data finder. Error is {e}")
        if store_as_default:
            self._defaultPattern = pattern
        self.sigPatternChanged.emit(self.getPattern())

    def getPattern(self) -> str:
        pattern = self._patternQLE.text()
        if pattern.replace(" ", "") == "":
            # make sure if the user just enter spaces processing will be run as expected
            pattern = ""
        return pattern

    def setDefaultPattern(self, pattern: str):
        "The default pattern is only used to reset the pattern use"
        self._defaultPattern = pattern

    def getDefaultPattern(self) -> str:
        return self._defaultPattern

    def setInputFile(self, file_path: str):
        """
        :param file_path: path to the file
        :param update_path: if true then will call callback to automatically determine the expected data path
        """
        try:
            self._dataPathFinder.file = file_path
        except Exception as e:
            _logger.error(f"Failed to update file path. Error is {e}")
        finally:
            self._patternQLE.completer().setFile(file_path)
            self._updateExample()

    def getInputFile(self) -> str | None:
        return self._dataPathFinder.file

    def _updateExample(self):
        missing_finder_information = []
        if self._dataPathFinder.file is None:
            missing_finder_information.append("no input file provided")
        if self._dataPathFinder.pattern is None:
            missing_finder_information.append("no pattern to search provided")
        missing_inputs = len(missing_finder_information) > 0
        tooltip = ""
        if not missing_inputs:
            first_scan = get_first_group(self._dataPathFinder.file)
            last_scan = get_last_group(self._dataPathFinder.file)
            try:
                example = self._dataPathFinder.format(
                    scan=first_scan, first_scan=first_scan, last_scan=last_scan
                )
            except Exception as e:
                err_mess = f"Failed to compute example. Error is {e}"
                _logger.error(err_mess)
                example = None
                tooltip = err_mess
            else:
                if example is None:
                    tooltip = f"Unable to find any dataset / group that could solve the pattern ({self._dataPathFinder.pattern}) with the current file ({self._dataPathFinder.file})"
        else:
            example = None
            tooltip = f"Missing input for the data path finder: {','.join(missing_finder_information)}"

        if example is None:
            self._exampleQLE.setText("")
        else:
            self._exampleQLE.setText(example)
        self._exampleQLE.setToolTip(tooltip)
        self._updateStatusIcon()

    def getExample(self) -> str:
        return self._exampleQLE.text()

    def _getWarningIcon(self):
        return icons.getQIcon("darfix:gui/icons/warning")

    def hideExample(self):
        self._exampleLabel.hide()
        self._exampleQLE.hide()

    # expose API
    def setPlaceholderText(self, text):
        self._patternQLE.setPlaceholderText(text)

    def setAvailableKeywords(self, keywords: tuple) -> None:
        self._dataPathFinder.allowed_keywords = keywords
        self._patternQLE.setAllowedKeywords(keywords=keywords)
