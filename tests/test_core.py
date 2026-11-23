"""Tests for MCPStreamingGateway."""
import unittest
from mcp_streaming_bidirectional_gateway.core import MCPStreamingGateway, FrameType

class TestMCPStreamingGateway(unittest.TestCase):
    def setUp(self):
        self.gw = MCPStreamingGateway()

    def test_streaming_flow(self):
        ch = self.gw.open_stream("s1")
        f1 = self.gw.send_chunk("s1", "data_1")
        f2 = self.gw.send_progress("s1", 50.0, "halfway")
        self.assertEqual(f1.seq, 1)
        self.assertEqual(f2.seq, 2)

    def test_interrupt(self):
        self.gw.open_stream("s2")
        self.gw.interrupt("s2", "emergency stop")
        with self.assertRaises(InterruptedError):
            self.gw.send_chunk("s2", "data_after_interrupt")
