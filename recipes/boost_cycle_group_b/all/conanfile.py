from conans import ConanFile


class BoostCycleGroupBConan(ConanFile):
    name = "boost_cycle_group_b"
    short_paths = True
    python_requires = "boost_base/2.1.0@bincrafters/testing"
    python_requires_extend = "boost_base.BoostBaseConan"
