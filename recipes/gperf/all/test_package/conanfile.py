#!/usr/bin/env python
# -*- coding: utf-8 -*-
from conans import ConanFile


class GperfTestConan(ConanFile):
    settings = "os_build"

    def test(self):
        self.run('gperf --version', run_environment=True)

