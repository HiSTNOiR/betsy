"""
Tests for the queue utility module.
"""
import unittest
from unittest.mock import patch, MagicMock
import threading
from queue import PriorityQueue, Queue, Empty, Full

from bot.utils.queue import (
    PriorityItem, PriorityMessageQueue, CommandQueue, DuelQueue
)
from bot.core.constants import MessagePriority

class TestPriorityItem(unittest.TestCase):
    """Tests for PriorityItem class."""
    
    def test_ordering(self):
        """Test item ordering based on priority."""
        # Lower priority value means higher priority
        item1 = PriorityItem(priority=1, item="high priority")
        item2 = PriorityItem(priority=2, item="medium priority")
        item3 = PriorityItem(priority=3, item="low priority")
        
        # Compare items
        self.assertLess(item1, item2)
        self.assertLess(item2, item3)
        self.assertGreater(item3, item1)
        
        # Same priority, different items (should be equal)
        item4 = PriorityItem(priority=1, item="another high priority")
        self.assertEqual(item1, item4)

class TestPriorityMessageQueue(unittest.TestCase):
    """Tests for PriorityMessageQueue class."""
    
    def setUp(self):
        """Set up for each test."""
        self.queue = PriorityMessageQueue()
        self.handler = MagicMock()
    
    def tearDown(self):
        """Clean up after each test."""
        if hasattr(self.queue, 'running') and self.queue.running:
            self.queue.stop()
    
    def test_init(self):
        """Test initialisation."""
        self.assertIsInstance(self.queue.queue, PriorityQueue)
        self.assertFalse(hasattr(self.queue, 'running') or self.queue.running)
        self.assertIsNone(self.queue.thread)
    
    def test_start_stop(self):
        """Test starting and stopping the queue."""
        # Start queue
        self.queue.start(self.handler)
        self.assertTrue(self.queue.running)
        self.assertIsNotNone(self.queue.thread)
        self.assertIs(self.queue.handler, self.handler)
        
        # Start again (should do nothing)
        thread = self.queue.thread
        self.queue.start(self.handler)
        self.assertIs(self.queue.thread, thread)
        
        # Stop queue
        self.queue.stop()
        self.assertFalse(self.queue.running)
    
    @patch('bot.utils.queue.PriorityQueue')
    def test_put(self, mock_queue):
        """Test adding messages to queue."""
        # Setup mock
        mock_instance = mock_queue.return_value
        
        # Put message (success)
        mock_instance.put_nowait.return_value = None
        result = self.queue.put("test message")
        self.assertTrue(result)
        
        # Check message was put with correct priority
        args, kwargs = mock_instance.put_nowait.call_args
        item = args[0]
        self.assertEqual(item.priority, MessagePriority.LOW.value)
        self.assertEqual(item.item, "test message")
        
        # Put message with custom priority
        result = self.queue.put("high priority message", MessagePriority.HIGH)
        args, kwargs = mock_instance.put_nowait.call_args
        item = args[0]
        self.assertEqual(item.priority, MessagePriority.HIGH.value)
        self.assertEqual(item.item, "high priority message")
        
        # Queue full
        mock_instance.put_nowait.side_effect = Full()
        result = self.queue.put("message")
        self.assertFalse(result)
    
    @patch('bot.utils.queue.PriorityQueue')
    def test_process_queue(self, mock_queue):
        """Test message processing."""
        # Setup
        self.queue.handler = self.handler
        
        # Mock queue get/empty behavior
        mock_instance = mock_queue.return_value
        mock_instance.get.side_effect = [
            PriorityItem(priority=MessagePriority.LOW.value, item="message1"),
            Empty(),  # Simulate queue empty to break the loop
        ]
        
        # Process queue
        self.queue.running = True
        self.queue._process_queue()
        
        # Check message was processed
        self.handler.assert_called_once_with("message1", MessagePriority.LOW)
        mock_instance.task_done.assert_called_once()

class TestCommandQueue(unittest.TestCase):
    """Tests for CommandQueue class."""
    
    def setUp(self):
        """Set up for each test."""
        self.queue = CommandQueue()
        self.handler = MagicMock()
    
    def tearDown(self):
        """Clean up after each test."""
        if hasattr(self.queue, 'running') and self.queue.running:
            self.queue.stop()
    
    def test_init(self):
        """Test initialisation."""
        self.assertIsInstance(self.queue.queue, Queue)
        self.assertFalse(hasattr(self.queue, 'running') or self.queue.running)
        self.assertIsNone(self.queue.thread)
    
    def test_start_stop(self):
        """Test starting and stopping the queue."""
        # Start queue
        self.queue.start(self.handler)
        self.assertTrue(self.queue.running)
        self.assertIsNotNone(self.queue.thread)
        self.assertIs(self.queue.handler, self.handler)
        
        # Start again (should do nothing)
        thread = self.queue.thread
        self.queue.start(self.handler)
        self.assertIs(self.queue.thread, thread)
        
        # Stop queue
        self.queue.stop()
        self.assertFalse(self.queue.running)
    
    @patch('bot.utils.queue.Queue')
    def test_put(self, mock_queue):
        """Test adding commands to queue."""
        # Setup mock
        mock_instance = mock_queue.return_value
        
        # Put command (success)
        mock_instance.put_nowait.return_value = None
        command = {"name": "test", "args": ["arg1", "arg2"]}
        result = self.queue.put(command)
        self.assertTrue(result)
        mock_instance.put_nowait.assert_called_with(command)
        
        # Queue full
        mock_instance.put_nowait.side_effect = Full()
        result = self.queue.put(command)
        self.assertFalse(result)
    
    @patch('bot.utils.queue.Queue')
    def test_process_queue(self, mock_queue):
        """Test command processing."""
        # Setup
        self.queue.handler = self.handler
        
        # Mock queue get/empty behavior
        mock_instance = mock_queue.return_value
        command = {"name": "test", "args": ["arg1", "arg2"]}
        mock_instance.get.side_effect = [
            command,
            Empty(),  # Simulate queue empty to break the loop
        ]
        
        # Process queue
        self.queue.running = True
        self.queue._process_queue()
        
        # Check command was processed
        self.handler.assert_called_once_with(command)
        mock_instance.task_done.assert_called_once()

class TestDuelQueue(unittest.TestCase):
    """Tests for DuelQueue class."""
    
    def setUp(self):
        """Set up for each test."""
        self.queue = DuelQueue()
        self.handler = MagicMock()
    
    def tearDown(self):
        """Clean up after each test."""
        if hasattr(self.queue, 'running') and self.queue.running:
            self.queue.stop()
    
    def test_init(self):
        """Test initialisation."""
        self.assertIsInstance(self.queue.queue, Queue)
        self.assertFalse(hasattr(self.queue, 'running') or self.queue.running)
        self.assertIsNone(self.queue.thread)
        self.assertEqual(self.queue.active_duels, {})
    
    def test_start_stop(self):
        """Test starting and stopping the queue."""
        # Start queue
        self.queue.start(self.handler)
        self.assertTrue(self.queue.running)
        self.assertIsNotNone(self.queue.thread)
        self.assertIs(self.queue.handler, self.handler)
        
        # Start again (should do nothing)
        thread = self.queue.thread
        self.queue.start(self.handler)
        self.assertIs(self.queue.thread, thread)
        
        # Stop queue
        self.queue.stop()
        self.assertFalse(self.queue.running)
    
    @patch('bot.utils.queue.Queue')
    def test_put(self, mock_queue):
        """Test adding duels to queue."""
        # Setup mock
        mock_instance = mock_queue.return_value
        mock_instance.put_nowait.return_value = None
        
        # Put duel (success)
        duel = {"challenger_id": "user1", "opponent_id": "user2", "amount": 100}
        result = self.queue.put(duel)
        self.assertTrue(result)
        mock_instance.put_nowait.assert_called_with(duel)
        self.assertIn("user1", self.queue.active_duels)
        self.assertIs(self.queue.active_duels["user1"], duel)
        
        # Put duel (challenger already has active duel)
        duel2 = {"challenger_id": "user1", "opponent_id": "user3", "amount": 200}
        result = self.queue.put(duel2)
        self.assertFalse(result)
        
        # Put duel (missing challenger_id)
        duel3 = {"opponent_id": "user2", "amount": 100}
        result = self.queue.put(duel3)
        self.assertFalse(result)
        
        # Queue full
        mock_instance.put_nowait.side_effect = Full()
        duel4 = {"challenger_id": "user4", "opponent_id": "user5", "amount": 100}
        result = self.queue.put(duel4)
        self.assertFalse(result)
        self.assertNotIn("user4", self.queue.active_duels)
    
    def test_get_active_duel(self):
        """Test getting active duel."""
        # Setup
        duel = {"challenger_id": "user1", "opponent_id": "user2", "amount": 100}
        self.queue.active_duels = {"user1": duel}
        
        # Get active duel
        result = self.queue.get_active_duel("user1")
        self.assertIs(result, duel)
        
        # Get non-existent duel
        result = self.queue.get_active_duel("user3")
        self.assertIsNone(result)
    
    def test_remove_active_duel(self):
        """Test removing active duel."""
        # Setup
        duel = {"challenger_id": "user1", "opponent_id": "user2", "amount": 100}
        self.queue.active_duels = {"user1": duel}
        
        # Remove active duel
        result = self.queue.remove_active_duel("user1")
        self.assertTrue(result)
        self.assertNotIn("user1", self.queue.active_duels)
        
        # Remove non-existent duel
        result = self.queue.remove_active_duel("user3")
        self.assertFalse(result)
    
    @patch('bot.utils.queue.Queue')
    def test_process_queue(self, mock_queue):
        """Test duel processing."""
        # Setup
        self.queue.handler = self.handler
        
        # Mock queue get/empty behavior
        mock_instance = mock_queue.return_value
        duel = {"challenger_id": "user1", "opponent_id": "user2", "amount": 100}
        mock_instance.get.side_effect = [
            duel,
            Empty(),  # Simulate queue empty to break the loop
        ]
        
        # Add to active duels
        self.queue.active_duels = {"user1": duel}
        
        # Process queue
        self.queue.running = True
        self.queue._process_queue()
        
        # Check duel was processed
        self.handler.assert_called_once_with(duel)
        mock_instance.task_done.assert_called_once()
        
        # Test error handling
        mock_instance.get.side_effect = [duel]
        self.handler.side_effect = Exception("Test error")
        self.queue._process_queue()
        
        # Active duel should be removed on error
        self.assertNotIn("user1", self.queue.active_duels)

if __name__ == '__main__':
    unittest.main()