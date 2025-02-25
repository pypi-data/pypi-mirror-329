from __future__ import annotations

from ewokscore import Task

from darfix.dtypes import Dataset


class RockingCurves(
    Task,
    input_names=["dataset"],
    optional_input_names=["int_thresh", "method"],
    output_names=["dataset", "maps"],
):
    def run(self):
        input_dataset: Dataset = self.inputs.dataset
        int_thresh: float | None = (
            float(self.inputs.int_thresh) if self.inputs.int_thresh else None
        )
        method: str | None = self.get_input_value("method", None)

        dataset = input_dataset.dataset
        indices = input_dataset.indices
        new_image_dataset, maps = dataset.apply_fit(
            indices=indices, int_thresh=int_thresh, method=method
        )

        self.outputs.dataset = Dataset(
            dataset=new_image_dataset,
            indices=indices,
            bg_indices=input_dataset.bg_indices,
            bg_dataset=input_dataset.bg_dataset,
        )
        self.outputs.maps = maps
