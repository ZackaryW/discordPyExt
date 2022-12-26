import unittest
import contextlib
import cProfile
import pstats
import io

class xTestcase(unittest.TestCase):
    """
    a Testcase class extension
    """
    
    @contextlib.contextmanager
    def profiler(self, print_stats=False):
        """
        a context manager for profiling
        
        ex:
        with self.profiler():
            # do something
    
        """
        
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