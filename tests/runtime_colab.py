from unittest import TestCase

class TestColab(TestCase):

    def test_print_mem(self):
        import defia_runtime as DR

        DR.print_memory_usage()




