from silx.gui import qt


def missing_dataset_msg():
    """
    show a dialog to the user notifying that the current widget has no dataset
    (and as a consequence cannot process)
    """
    msg = qt.QMessageBox()
    msg.setIcon(qt.QMessageBox.Critical)
    msg.setText("No dataset defined. Unable to process")
    msg.setWindowTitle("Missing dataset")
    msg.exec()
