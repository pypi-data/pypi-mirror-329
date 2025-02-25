from __future__ import annotations

from ewokscore.variable import Variable
from ewoksorange.bindings.owwidgets import OWEwoksWidgetOneThread
from ewoksorange.bindings.owwidgets import ow_build_opts

from darfix import dtypes


def unpackDataset(dataset: Variable | dtypes.Dataset) -> dtypes.Dataset:
    """
    util function to handle compatibility between widgets
    """
    # Temp fix until https://gitlab.esrf.fr/workflow/ewoks/ewoksorange/-/merge_requests/169 is merged
    if isinstance(dataset, Variable):
        return dataset.value

    return dataset


class OWDarfixWidgetOneThread(OWEwoksWidgetOneThread, **ow_build_opts):
    """A base widget to put behaviour common to all Orange Darfix widgets."""

    def get_task_inputs(self):
        task_inputs = super().get_task_inputs()

        if "dataset" in task_inputs:
            task_inputs["dataset"] = unpackDataset(dataset=task_inputs.get("dataset"))
        return task_inputs
