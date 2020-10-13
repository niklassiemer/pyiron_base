# coding: utf-8
# Copyright (c) Max-Planck-Institut für Eisenforschung GmbH - Computational Materials Design (CM) Department
# Distributed under the terms of "New BSD License", see the LICENSE file.
from pyiron_base.job.generic import GenericJob
from pyiron_base.generic.parameters import GenericParameters
from pyiron_base.generic.inputlist import InputList

"""
Template class to define jobs
"""

__author__ = "Jan Janssen"
__copyright__ = (
    "Copyright 2020, Max-Planck-Institut für Eisenforschung GmbH - "
    "Computational Materials Design (CM) Department"
)
__version__ = "1.0"
__maintainer__ = "Jan Janssen"
__email__ = "janssen@mpie.de"
__status__ = "development"
__date__ = "May 15, 2020"


class TemplateJob(GenericJob):
    def __init__(self, project, job_name):
        super().__init__(project, job_name)
        self.input = GenericParameters(table_name="input")

    def to_hdf(self, hdf=None, group_name=None):
        super().to_hdf(
            hdf=hdf,
            group_name=group_name
        )
        with self.project_hdf5.open("input") as h5in:
            self.input.to_hdf(h5in)

    def from_hdf(self, hdf=None, group_name=None):
        super().from_hdf(
            hdf=hdf,
            group_name=group_name
        )
        with self.project_hdf5.open("input") as h5in:
            self.input.from_hdf(h5in)


class PythonTemplateJob(TemplateJob):
    def __init__(self, project, job_name):
        super().__init__(project, job_name)
        self.output = InputList(table_name="output")
        self._python_only_job = True

    def from_hdf(self, hdf=None, group_name=None):
        super().from_hdf(
            hdf=hdf,
            group_name=group_name
        )
        if hdf is None:
            hdf = self.project_hdf5
        self.output.from_hdf(hdf=hdf, group_name=None)

    def to_hdf(self, hdf=None, group_name=None):
        super().to_hdf(
            hdf=hdf,
            group_name=group_name
        )
        if hdf is None:
            hdf = self.project_hdf5
        self.output.to_hdf(hdf=hdf, group_name=None)

    def save_output(self):
        self.output.to_hdf(hdf=self.project_hdf5, group_name=None)
        self.status.finished=True

    def _check_if_input_should_be_written(self):
        return False
