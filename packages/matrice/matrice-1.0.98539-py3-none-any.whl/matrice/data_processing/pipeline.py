import time
import threading
import logging
from typing import Dict, Any, List, Optional
from queue import Queue, Empty


class PipelineStage:
    def __init__(
        self,
        stage_name: str,
        pull_queue: Optional[Queue],
        push_queue: Optional[Queue], 
        process_fn: callable,
        process_params: Dict[str, Any],
        num_threads: int,
    ) -> None:
        """Initialize a pipeline stage.

        Args:
            stage_name: Name of the stage
            pull_queue: Queue to pull samples from
            push_queue: Queue to push processed samples to
            process_fn: Function to process samples
            process_params: Parameters for the process function
            num_threads: Number of worker threads
        """
        self.stage_name = stage_name
        self.pull_queue = pull_queue
        self.push_queue = push_queue
        self.process_function = process_fn
        self.num_samples_processed = 0
        self.process_params = process_params or {}
        self.num_threads = max(1, num_threads)
        self.sleep_flag = True
        self.stop_flag = False
        self.workers: List[threading.Thread] = []
        self.current_partition_num = 0

    def _worker_loop(self) -> None:
        """Main worker thread loop that processes samples from pull queue."""
        while not self.stop_flag:
            if self.sleep_flag:
                logging.debug(f"Stage {self.stage_name} sleeping")
                time.sleep(10)
                continue
                
            try:
                processed_sample = None
                
                if self.pull_queue:
                    try:
                        sample = self.pull_queue.get(timeout=1)  # Reduced timeout for better responsiveness
                        if sample is not None:  # Handle None samples gracefully
                            processed_sample = self.process_function(sample, **self.process_params)
                            self._update_current_partition_from_sample(sample)
                        self.pull_queue.task_done()
                        self.num_samples_processed += 1
                    except Empty:
                        continue
                    except Exception as e:
                        logging.error(f"Error processing sample in {self.stage_name}: {e}", exc_info=True)
                        continue
                else:
                    processed_sample = self.process_function(**self.process_params)

                if self.push_queue and processed_sample is not None:
                    self.push_queue.put(processed_sample)

            except Exception as e:
                logging.error(f"Error in worker loop for {self.stage_name}: {e}", exc_info=True)
                time.sleep(10)  # Prevent tight error loops

    def start(self) -> None:
        """Start processing samples by launching worker threads."""
        if self.workers:
            logging.warning(f"Stage {self.stage_name} already has active workers")
            return
            
        self.sleep_flag = False
        self.stop_flag = False
        logging.info(f"Starting {self.num_threads} workers for stage {self.stage_name}")

        for i in range(self.num_threads):
            worker = threading.Thread(
                target=self._worker_loop,
                daemon=True,
                name=f"{self.stage_name}-worker-{i+1}"
            )
            self.workers.append(worker)
            worker.start()
            logging.debug(f"Started {worker.name}")

    def stop(self) -> None:
        """Stop processing by setting stop flag."""
        logging.info(f"Stopping stage {self.stage_name}")
        self.stop_flag = True
        self.sleep_flag = False

    def sleep(self) -> None:
        """Pause processing by setting sleep flag."""
        if not self.sleep_flag:
            logging.info(f"Sleeping stage {self.stage_name}")
            self.sleep_flag = True

    def wake_up(self) -> None:
        """Resume processing by clearing sleep flag."""
        if self.sleep_flag:
            logging.info(f"Waking up stage {self.stage_name}")
            self.sleep_flag = False

    def join(self) -> None:
        """Stop processing and wait for all workers to finish."""
        logging.info(f"Joining stage {self.stage_name}")
        for worker in self.workers:
            if worker.is_alive():
                worker.join()
        self.workers.clear()

    def _update_current_partition_from_sample(self, sample: Any) -> None:
        """Update current partition number from a sample."""
        if not sample:
            return
            
        if isinstance(sample, list) and sample:
            partition = sample[0].get("partition", 0) if isinstance(sample[0], dict) else 0
            self.current_partition_num = max(self.current_partition_num, partition)
        elif isinstance(sample, dict):
            self.current_partition_num = max(
                self.current_partition_num, sample.get("partition", 0)
            )


class Pipeline:
    def __init__(self) -> None:
        self.producers: List[Dict[str, Any]] = []
        self.stages: Dict[str, PipelineStage] = {}
        self.pull_queues: Dict[str, Queue] = {}
        self.push_queues: Dict[str, Queue] = {}
        self.stop_callbacks: List[Dict[str, Any]] = []
        self.last_stage_queue: Queue = Queue()
        self.manage_stages_sleep_and_wake_up_thread: Optional[threading.Thread] = None
        self.producers_thread: Optional[threading.Thread] = None
        self.all_items: List[Any] = []
        self._is_running: bool = False

    def add_producer(
        self,
        process_fn: callable,
        process_params: Optional[Dict[str, Any]] = {},
        partition_num: int = 0,
    ) -> None:
        """Add a producer stage that generates data for the pipeline."""
        if not callable(process_fn):
            raise ValueError("process_fn must be callable")
            
        logging.info(f"Adding producer {process_fn.__name__} with params: {process_params}")
        self.producers.append({
            "partition_num": partition_num,
            "process_fn": process_fn,
            "process_params": process_params or {},
        })

    def start_producers(self) -> None:
        """Start all producer threads in order of partition number."""
        if not self.producers:
            logging.warning("No producers configured")
            return
            
        logging.info(f"Starting {len(self.producers)} producers")
        self.producers.sort(key=lambda x: x.get("partition_num", 0))
        
        for producer in self.producers:
            try:
                logging.info(
                    f"Starting producer {producer['process_fn'].__name__} "
                    f"with params: {producer['process_params']} "
                    f"for partition {producer['partition_num']}"
                )
                thread = threading.Thread(
                    target=producer["process_fn"],
                    kwargs=producer["process_params"],
                    daemon=True,
                    name=f"producer-{producer['partition_num']}"
                )
                thread.start()
                thread.join()
            except Exception as e:
                logging.error(f"Error starting producer: {e}", exc_info=True)

    def add_stage(
        self,
        stage_name: str,
        process_fn: callable,
        pull_queue: Optional[Queue] = None,
        push_queue: Optional[Queue] = None,
        process_params: Optional[Dict[str, Any]] = None,
        num_threads: int = 1,
        is_last_stage: bool = False,
    ) -> None:
        """Add a new processing stage to the pipeline."""
        if stage_name in self.stages:
            raise ValueError(f"Stage {stage_name} already exists")
            
        if not callable(process_fn):
            raise ValueError("process_fn must be callable")
            
        logging.info(f"Adding stage: {stage_name}")
        
        if is_last_stage:
            logging.info(f"Stage {stage_name} marked as last stage")
            if push_queue:
                raise ValueError("Last stage cannot have a push queue")
            push_queue = self.last_stage_queue

        stage = PipelineStage(
            stage_name=stage_name,
            pull_queue=pull_queue,
            push_queue=push_queue,
            process_fn=process_fn,
            process_params=process_params or {},
            num_threads=num_threads
        )
        self.stages[stage_name] = stage

        if pull_queue:
            self.pull_queues[stage_name] = pull_queue
        if push_queue and not is_last_stage:
            self.push_queues[stage_name] = push_queue

    def remove_stage(self, stage_name: str) -> None:
        """Remove a stage from the pipeline."""
        if stage_name not in self.stages:
            logging.warning(f"Stage {stage_name} does not exist")
            return
            
        logging.info(f"Removing stage: {stage_name}")
        stage = self.stages[stage_name]
        stage.stop()
        stage.join()
        
        del self.stages[stage_name]

    def start_stage(self, stage_name: str) -> None:
        """Start a specific stage."""
        if stage_name not in self.stages:
            logging.warning(f"Stage {stage_name} does not exist")
            return
            
        logging.info(f"Starting stage: {stage_name}")
        self.stages[stage_name].start()

    def sleep_stage(self, stage_name: str) -> None:
        """Pause a specific stage."""
        if stage_name not in self.stages:
            logging.warning(f"Stage {stage_name} does not exist")
            return
            
        logging.info(f"Pausing stage: {stage_name}")
        self.stages[stage_name].sleep()

    def start(self) -> None:
        """Start all pipeline stages and management threads."""
        if self._is_running:
            logging.warning("Pipeline already running")
            return
            
        logging.info("Starting pipeline")
        self._is_running = True
        
        self.manage_stages_sleep_and_wake_up_thread = threading.Thread(
            target=self.manage_stages_sleep_and_wake_up,
            daemon=True,
            name="stage-manager"
        )
        self.manage_stages_sleep_and_wake_up_thread.start()
        
        self.producers_thread = threading.Thread(
            target=self.start_producers,
            daemon=True,
            name="producers-manager"
        )
        self.producers_thread.start()
        
        for stage_name, stage in self.stages.items():
            logging.debug(f"Starting stage: {stage_name}")
            stage.start()

    def stop(self) -> None:
        """Stop all pipeline stages and execute callbacks."""
        if not self._is_running:
            logging.warning("Pipeline not running")
            return
            
        logging.info("Stopping pipeline")
        self._is_running = False
        
        for stage_name, stage in self.stages.items():
            logging.debug(f"Stopping stage: {stage_name}")
            stage.stop()
            stage.join()
            
        self.call_stop_callbacks()

    def add_stop_callback(
        self, 
        callback: callable, 
        process_params: Optional[Dict[str, Any]] = {}
    ) -> None:
        """Add a callback to execute when pipeline stops."""
        if not callable(callback):
            raise ValueError("callback must be callable")
            
        self.stop_callbacks.append({
            "callback": callback,
            "process_params": process_params or {}
        })

    def call_stop_callbacks(self) -> None:
        """Execute all registered stop callbacks."""
        items = self.get_all_items_from_last_stage()
        
        for callback in self.stop_callbacks:
            try:
                callback["callback"](
                    items,
                    **callback["process_params"]
                )
            except Exception as e:
                logging.error(
                    f"Error in stop callback: {e} with params: {callback['process_params']}",
                    exc_info=True
                )

    def get_all_items_from_last_stage(self) -> List[Any]:
        """Get all items from the last stage."""
        if not self.all_items:
            while not self.last_stage_queue.empty():
                try:
                    item = self.last_stage_queue.get(timeout=1)
                    self.all_items.append(item)
                    self.last_stage_queue.task_done()
                except Empty:
                    break
        return self.all_items

    def manage_stages_sleep_and_wake_up(self) -> None:
        """Manage stage execution by pausing/resuming based on partition progress."""
        while self._is_running:
            try:
                stages = list(self.stages.values())
                for i in range(len(stages) - 1):
                    current_stage = stages[i]
                    next_stage = stages[i + 1]

                    # Make sure both stages have a partition number more than 0: to indicate that it has started processing
                    if current_stage.current_partition_num and next_stage.current_partition_num:
                        partition_gap = current_stage.current_partition_num - next_stage.current_partition_num
                        
                        # Pause if current stage is too far ahead
                        if partition_gap > 1:
                            for stage in stages[:i+1]:
                                stage.sleep()
                        # Resume if current stage has caught up
                        elif current_stage.sleep_flag and partition_gap <= 1:
                            for stage in stages[:i+1]:
                                stage.wake_up()

                time.sleep(10)
            except Exception as e:
                logging.error(f"Error in stage management: {e}", exc_info=True)
                time.sleep(1)

    def wait_to_finish_processing_and_stop(self) -> None:
        """Wait for all processing to complete and stop the pipeline."""
        if not self._is_running:
            logging.warning("Pipeline not running")
            return
            
        logging.info("Waiting for pipeline completion")

        if self.producers_thread and self.producers_thread.is_alive():
            self.producers_thread.join()
            logging.info("Producers completed")
        
        for stage_name, stage in self.stages.items():
            if stage_name in self.pull_queues:
                logging.info(f"Waiting for {stage_name} queue")
                self.pull_queues[stage_name].join()
                logging.info(f"{stage_name} queue completed")
            stage.stop()
            stage.join()
            logging.info(f"{stage_name} completed")
            
        logging.info("Pipeline processing complete, stopping")
        self.stop()