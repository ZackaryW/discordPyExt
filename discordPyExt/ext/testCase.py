import unittest
import contextlib
import cProfile
import pstats
import io

class TestCaseX(unittest.TestCase):
    @contextlib.contextmanager
    def profiler(self, print_stats=False):
        pr = cProfile.Profile()
        pr.enable()
        yield
        pr.disable()
        
        sortby = 'cumulative'
        s = io.StringIO()
        self.last_profiler = pstats.Stats(pr, stream=s).sort_stats(sortby)
        self.last_profiler.print_stats()
        
        if print_stats:
            print(s.getvalue())