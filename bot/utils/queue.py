"""
Queue utility functions for the Twitch bot.
"""
import time
import logging
import threading
from queue import PriorityQueue, Queue, Empty, Full
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar, Union, Tuple

from bot.core.constants import MessagePriority

# Set up logger
logger = logging.getLogger(__name__)

# Generic type variable
T = TypeVar('T')

@dataclass(order=True)
class PriorityItem(Generic[T]):
    """Class for items in priority queue with comparison based on priority."""
    priority: int
    item: T = field(compare=False)
    timestamp: float = field(default_factory=time.time)

class PriorityMessageQueue:
    """
    Priority-based message queue for handling bot output messages.
    Messages with higher priority are processed first.
    """
    
    def __init__(self, maxsize: int = 100):
        """
        Initialise priority message queue.
        
        Args:
            maxsize: Maximum queue size (default: 100)
        """
        self.queue = PriorityQueue(maxsize=maxsize)
        self.lock = threading.RLock()
        self.running = False
        self.thread = None
    
    def start(self, handler: Callable[[str, MessagePriority], None]) -> None:
        """
        Start message processing thread.
        
        Args:
            handler: Function to handle messages (takes message and priority)
        """
        with self.lock:
            if self.running:
                return
            
            self.running = True
            self.handler = handler
            self.thread = threading.Thread(target=self._process_queue, daemon=True)
            self.thread.start()
            logger.info("Priority message queue started")
    
    def stop(self) -> None:
        """Stop message processing thread."""
        with self.lock:
            if not self.running:
                return
            
            self.running = False
            if self.thread and self.thread.is_alive():
                self.thread.join(timeout=1.0)
            logger.info("Priority message queue stopped")
    
    def put(self, message: str, priority: MessagePriority = MessagePriority.LOW) -> bool:
        """
        Add message to queue.
        
        Args:
            message: Message to add
            priority: Message priority (default: LOW)
        
        Returns:
            True if message added, False if queue full
        """
        try:
            item = PriorityItem(priority=priority.value, item=message)
            self.queue.put_nowait(item)
            return True
        except Full:
            logger.warning(f"Message queue full, dropping message: {message}")
            return False
    
    def _process_queue(self) -> None:
        """Process messages from queue."""
        while self.running:
            try:
                # Get message from queue with timeout to allow checking running flag
                item = self.queue.get(timeout=0.1)
                
                # Get priority enum from value
                priority = MessagePriority(item.priority)
                
                # Handle message
                try:
                    self.handler(item.item, priority)
                except Exception as e:
                    logger.error(f"Error handling message: {e}")
                
                # Mark task as done
                self.queue.task_done()
            
            except Empty:
                # Queue is empty, just continue
                continue
            except Exception as e:
                logger.error(f"Error processing message queue: {e}")
                # Sleep briefly to avoid tight loop on persistent error
                time.sleep(0.1)

class CommandQueue:
    """
    Queue for processing commands.
    Commands are processed in FIFO order.
    """
    
    def __init__(self, maxsize: int = 100):
        """
        Initialise command queue.
        
        Args:
            maxsize: Maximum queue size (default: 100)
        """
        self.queue = Queue(maxsize=maxsize)
        self.lock = threading.RLock()
        self.running = False
        self.thread = None
    
    def start(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """
        Start command processing thread.
        
        Args:
            handler: Function to handle commands (takes command dict)
        """
        with self.lock:
            if self.running:
                return
            
            self.running = True
            self.handler = handler
            self.thread = threading.Thread(target=self._process_queue, daemon=True)
            self.thread.start()
            logger.info("Command queue started")
    
    def stop(self) -> None:
        """Stop command processing thread."""
        with self.lock:
            if not self.running:
                return
            
            self.running = False
            if self.thread and self.thread.is_alive():
                self.thread.join(timeout=1.0)
            logger.info("Command queue stopped")
    
    def put(self, command: Dict[str, Any]) -> bool:
        """
        Add command to queue.
        
        Args:
            command: Command dictionary
        
        Returns:
            True if command added, False if queue full
        """
        try:
            self.queue.put_nowait(command)
            return True
        except Full:
            logger.warning(f"Command queue full, dropping command: {command}")
            return False
    
    def _process_queue(self) -> None:
        """Process commands from queue."""
        while self.running:
            try:
                # Get command from queue with timeout to allow checking running flag
                command = self.queue.get(timeout=0.1)
                
                # Handle command
                try:
                    self.handler(command)
                except Exception as e:
                    logger.error(f"Error handling command: {e}")
                
                # Mark task as done
                self.queue.task_done()
            
            except Empty:
                # Queue is empty, just continue
                continue
            except Exception as e:
                logger.error(f"Error processing command queue: {e}")
                # Sleep briefly to avoid tight loop on persistent error
                time.sleep(0.1)

class DuelQueue:
    """
    Queue for handling duel requests.
    """
    
    def __init__(self, maxsize: int = 20):
        """
        Initialise duel queue.
        
        Args:
            maxsize: Maximum queue size (default: 20)
        """
        self.queue = Queue(maxsize=maxsize)
        self.lock = threading.RLock()
        self.running = False
        self.thread = None
        self.active_duels: Dict[str, Dict[str, Any]] = {}  # challenger_id -> duel_info
    
    def start(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """
        Start duel processing thread.
        
        Args:
            handler: Function to handle duels (takes duel dict)
        """
        with self.lock:
            if self.running:
                return
            
            self.running = True
            self.handler = handler
            self.thread = threading.Thread(target=self._process_queue, daemon=True)
            self.thread.start()
            logger.info("Duel queue started")
    
    def stop(self) -> None:
        """Stop duel processing thread."""
        with self.lock:
            if not self.running:
                return
            
            self.running = False
            if self.thread and self.thread.is_alive():
                self.thread.join(timeout=1.0)
            logger.info("Duel queue stopped")
    
    def put(self, duel: Dict[str, Any]) -> bool:
        """
        Add duel to queue.
        
        Args:
            duel: Duel dictionary
        
        Returns:
            True if duel added, False if queue full or challenger already has active duel
        """
        challenger_id = duel.get('challenger_id')
        if not challenger_id:
            logger.warning("Duel missing challenger_id, dropping duel")
            return False
        
        with self.lock:
            # Check if challenger already has active duel
            if challenger_id in self.active_duels:
                logger.warning(f"Challenger {challenger_id} already has active duel, dropping duel")
                return False
            
            # Add to active duels
            self.active_duels[challenger_id] = duel
        
        try:
            self.queue.put_nowait(duel)
            return True
        except Full:
            with self.lock:
                # Remove from active duels if queue is full
                if challenger_id in self.active_duels:
                    del self.active_duels[challenger_id]
            
            logger.warning(f"Duel queue full, dropping duel: {duel}")
            return False
    
    def get_active_duel(self, challenger_id: str) -> Optional[Dict[str, Any]]:
        """
        Get active duel for challenger.
        
        Args:
            challenger_id: Challenger's user ID
        
        Returns:
            Duel dictionary or None if no active duel
        """
        with self.lock:
            return self.active_duels.get(challenger_id)
    
    def remove_active_duel(self, challenger_id: str) -> bool:
        """
        Remove active duel for challenger.
        
        Args:
            challenger_id: Challenger's user ID
        
        Returns:
            True if duel removed, False if no active duel
        """
        with self.lock:
            if challenger_id in self.active_duels:
                del self.active_duels[challenger_id]
                return True
            return False
    
    def _process_queue(self) -> None:
        """Process duels from queue."""
        while self.running:
            try:
                # Get duel from queue with timeout to allow checking running flag
                duel = self.queue.get(timeout=0.1)
                
                # Handle duel
                try:
                    self.handler(duel)
                except Exception as e:
                    logger.error(f"Error handling duel: {e}")
                    
                    # Remove from active duels if error occurs
                    challenger_id = duel.get('challenger_id')
                    if challenger_id:
                        self.remove_active_duel(challenger_id)
                
                # Mark task as done
                self.queue.task_done()
            
            except Empty:
                # Queue is empty, just continue
                continue
            except Exception as e:
                logger.error(f"Error processing duel queue: {e}")
                # Sleep briefly to avoid tight loop on persistent error
                time.sleep(0.1)

class TaskQueue:
    """
    Generic task queue for background tasks.
    """
    
    def __init__(self, maxsize: int = 100):
        """
        Initialise task queue.
        
        Args:
            maxsize: Maximum queue size (default: 100)
        """
        self.queue = Queue(maxsize=maxsize)
        self.lock = threading.RLock()
        self.running = False
        self.thread = None
    
    def start(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """
        Start task processing thread.
        
        Args:
            handler: Function to handle tasks (takes task dict)
        """
        with self.lock:
            if self.running:
                return
            
            self.running = True
            self.handler = handler
            self.thread = threading.Thread(target=self._process_queue, daemon=True)
            self.thread.start()
            logger.info("Task queue started")
    
    def stop(self) -> None:
        """Stop task processing thread."""
        with self.lock:
            if not self.running:
                return
            
            self.running = False
            if self.thread and self.thread.is_alive():
                self.thread.join(timeout=1.0)
            logger.info("Task queue stopped")
    
    def put(self, task: Dict[str, Any]) -> bool:
        """
        Add task to queue.
        
        Args:
            task: Task dictionary
        
        Returns:
            True if task added, False if queue full
        """
        try:
            self.queue.put_nowait(task)
            return True
        except Full:
            logger.warning(f"Task queue full, dropping task: {task}")
            return False
    
    def _process_queue(self) -> None:
        """Process tasks from queue."""
        while self.running:
            try:
                # Get task from queue with timeout to allow checking running flag
                task = self.queue.get(timeout=0.1)
                
                # Handle task
                try:
                    self.handler(task)
                except Exception as e:
                    logger.error(f"Error handling task: {e}")
                
                # Mark task as done
                self.queue.task_done()
            
            except Empty:
                # Queue is empty, just continue
                continue
            except Exception as e:
                logger.error(f"Error processing task queue: {e}")
                # Sleep briefly to avoid tight loop on persistent error
                time.sleep(0.1)