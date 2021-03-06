# coding: utf-8
# Copyright (c) Max-Planck-Institut für Eisenforschung GmbH - Computational Materials Design (CM) Department
# Distributed under the terms of "New BSD License", see the LICENSE file.

import os
import unittest
from pyiron_base.project.generic import Project


class TestCopyTo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file_location = os.path.dirname(os.path.abspath(__file__))
        cls.project = Project(os.path.join(cls.file_location, "testing_copyto"))

    @classmethod
    def tearDownClass(cls):
        file_location = os.path.dirname(os.path.abspath(__file__))
        project = Project(os.path.join(file_location, "testing_copyto"))
        sub_project = project.open("sub_project_ex")
        sub_project.remove(enable=True)
        sub_project = project.open("sub_project")
        sub_project.remove(enable=True)

    def test_copy_to_job(self):
        job_ser = self.project.create.job.SerialMasterBase("sequence_single")
        ham = self.project.create.job.ScriptJob("job_single")
        ham.copy_to(job_ser)
        self.assertTrue(job_ser['job_single/input/custom_dict'])
        job_ser.remove()

        job = self.project.create.job.ScriptJob("job_script")

        with open('foo.py', 'w') as f:
            f.write("print(42)\n")

        job.script_path = "foo.py"
        job.save()
        copy = job.copy_to(job.project_hdf5, "job_copy")
        self.assertEqual(job.script_path, copy.script_path,
                         "Script path not equal after copy.")

        jobc = self.project.inspect(job.id)
        copyc = jobc.copy_to(jobc.project_hdf5, "job_core_copy")
        self.assertEqual(jobc.load_object().script_path, copyc.load_object().script_path,
                         "Script path not equal after JobCore copy.")

        os.remove("foo.py")

    def test_copy_to_project(self):
        sub_project = self.project.copy()
        sub_project = sub_project.open("sub_project")
        ham = self.project.create_job("ScriptJob", "job_single_pr")
        ham.copy_to(project=sub_project)

    def test_copy_to_job_ex(self):
        job_ser = self.project.create.job.SerialMasterBase("sequence_single_ex")
        ham = self.project.create.job.ScriptJob("job_single_ex")
        ham.to_hdf()
        ham.copy_to(job_ser)
        self.assertTrue(job_ser['job_single_ex/input/custom_dict'])
        ham.remove()
        job_ser.remove()

    def test_copy_to_project_ex(self):
        sub_project = self.project.copy()
        sub_project = sub_project.open("sub_project_ex")
        ham = self.project.create_job("ScriptJob", "job_single_pr_ex")
        ham.to_hdf()
        ham.copy_to(project=sub_project)
        ham.remove()
        os.remove(
            os.path.join(
                self.file_location, "testing_copyto/sub_project_ex/job_single_pr_ex.h5"
            )
        )


if __name__ == "__main__":
    unittest.main()
