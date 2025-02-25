from typing import Sequence

import numpy
from ewokscore import Task

from darfix.dtypes import Dataset


class ShiftCorrection(
    Task,
    input_names=["dataset"],
    optional_input_names=["shift"],
    output_names=["dataset"],
):
    def run(self):
        input_dataset: Dataset = self.inputs.dataset
        shift: Sequence[float] = self.get_input_value("shift", (0, 0))

        dataset = input_dataset.dataset
        indices = input_dataset.indices

        frames = numpy.arange(dataset.get_data(indices=indices).shape[0])
        new_image_dataset = dataset.apply_shift(
            numpy.outer(shift, frames), indices=indices
        )

        self.outputs.dataset = Dataset(
            dataset=new_image_dataset,
            indices=input_dataset.indices,
            bg_indices=input_dataset.bg_indices,
            bg_dataset=input_dataset.bg_dataset,
        )
