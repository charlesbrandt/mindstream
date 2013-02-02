import sys, os
sys.path.append(os.path.dirname(os.getcwd()))
#print sys.path

from datetime import datetime

class TestMindstream:
    def setUp(self):
        """
        setup up any state specific to the execution
        of the given cls.
        """
        self.j = journal.Journal()
        self.j.load("zoobar/sample_log.txt")



    def test_union(self):
        tags = [ 'foo', 'bar' ]
        entries = self.j.union_tags(tags)
        print "%s entries found from union" % len(entries)
        assert len(entries) == 3

    def test_intersect(self):
        tags = [ 'foo', 'bar' ]
        entries = self.j.intersect_tags(tags)
        print "%s entries found from intersect" % len(entries)
        assert len(entries) == 2

    def test_newest_entries_from_file(self):
        k = journal.Journal("zoobar/sample_log2.txt")
        others = self.j.difference(k)
        assert len(others) == 1

        print others[0]
        print others[0].data
        assert others[0].data == "test entry\n\n"

