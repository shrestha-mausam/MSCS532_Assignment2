#!/usr/bin/env python3
"""
Quicksort Implementation with Performance Analysis

This module implements the Quicksort algorithm with detailed comments and
performance tracking capabilities including execution time and memory usage.

Author: Mausam Shrestha
Date: 2025  
"""

import time
import psutil
import os
import sys
from typing import List, Tuple, Optional


class PerformanceTracker:
    """
    Class to track performance metrics during sorting operations.
    
    This class provides a clean interface for measuring:
    - Execution time (start to finish)
    - Memory usage (before and after sorting)
    
    It uses psutil to get accurate memory measurements and time module
    for precise timing measurements.
    """
    
    def __init__(self):
        """Initialize the performance tracker with default values."""
        # Timing variables - will be set when tracking starts/stops
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        
        # Memory tracking variables - will be set when tracking starts/stops
        self.start_memory: Optional[float] = None
        self.end_memory: Optional[float] = None
        
        # Get reference to current process for memory monitoring
        self.process = psutil.Process(os.getpid())
    
    def start_tracking(self) -> None:
        """
        Start tracking performance metrics.
        
        Records the current time and memory usage as baseline measurements.
        These values will be used to calculate the difference when tracking stops.
        """
        # Record current timestamp for execution time calculation
        self.start_time = time.time()
        
        # Record current memory usage in MB (RSS = Resident Set Size)
        # RSS represents the amount of physical memory currently used by the process
        self.start_memory = self.process.memory_info().rss / 1024 / 1024  # Convert bytes to MB
    
    def stop_tracking(self) -> Tuple[float, float]:
        """
        Stop tracking and return execution time and memory usage.
        
        Calculates the difference between start and end measurements
        to determine how much time and memory the operation consumed.
        
        Returns:
            Tuple[float, float]: (execution_time_in_seconds, memory_usage_in_MB)
        """
        # Record final timestamp
        self.end_time = time.time()
        
        # Record final memory usage in MB
        self.end_memory = self.process.memory_info().rss / 1024 / 1024  # Convert bytes to MB
        
        # Calculate the differences
        execution_time = self.end_time - self.start_time
        memory_usage = self.end_memory - self.start_memory
        
        return execution_time, memory_usage


def partition(arr: List[int], low: int, high: int) -> int:
    """
    Partition function for Quicksort algorithm.
    
    This is the core partitioning logic of Quicksort. It:
    1. Selects a random pivot element to avoid worst-case performance
    2. Moves the pivot to the end of the subarray
    3. Rearranges elements so all elements <= pivot are on the left
    4. Places the pivot in its final sorted position
    5. Returns the pivot's final index
    
    The partitioning process ensures that after completion:
    - All elements to the left of pivot are <= pivot
    - All elements to the right of pivot are > pivot
    - The pivot is in its correct sorted position
    
    Args:
        arr: List of integers to be partitioned (modified in-place)
        low: Starting index of the subarray to partition
        high: Ending index of the subarray to partition
    
    Returns:
        int: The index where the pivot element ends up after partitioning
    """
    import random
    
    # STEP 1: Choose a random pivot to avoid worst-case performance
    # This randomization helps prevent O(n²) behavior on sorted/reverse-sorted data
    pivot_index = random.randint(low, high)
    pivot = arr[pivot_index]
    
    # STEP 2: Move pivot to the end of the subarray
    # This simplifies the partitioning logic by keeping pivot out of the way
    arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
    
    # STEP 3: Initialize partition index
    # 'i' tracks the position where the next smaller element should go
    # It starts at (low - 1) because we haven't found any smaller elements yet
    i = low - 1
    
    # STEP 4: Traverse through all elements in the subarray (except pivot)
    for j in range(low, high):
        # If current element is smaller than or equal to pivot
        if arr[j] <= pivot:
            # Increment the partition index
            i += 1
            # Swap current element with element at partition index
            # This ensures all smaller elements are moved to the left
            arr[i], arr[j] = arr[j], arr[i]
    
    # STEP 5: Place pivot in its correct position
    # After the loop, 'i+1' is the correct position for the pivot
    # All elements at positions <= i are <= pivot
    # All elements at positions > i+1 are > pivot
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    
    # Return the final position of the pivot
    return i + 1


def quicksort(arr: List[int], low: int, high: int) -> None:
    """
    Main Quicksort function that recursively sorts the array.
    
    Quicksort is a divide-and-conquer algorithm that works by:
    1. Selecting a 'pivot' element from the array
    2. Partitioning the array around the pivot (elements < pivot go left, > pivot go right)
    3. Recursively sorting the left and right subarrays
    4. Combining results (no explicit combine step needed - elements are in place)
    
    The algorithm modifies the input array in-place, making it memory efficient.
    
    Time Complexity Analysis:
        - Best Case: O(n log n) - when pivot divides array into equal halves
        - Average Case: O(n log n) - expected performance with random pivot selection
        - Worst Case: O(n²) - when pivot is always the smallest or largest element
    
    Space Complexity: O(log n) - due to recursive call stack depth
    
    Args:
        arr: List of integers to be sorted (modified in-place)
        low: Starting index of the subarray to sort
        high: Ending index of the subarray to sort
    """
    # Base case: if there's only one element or no elements, array is already sorted
    if low < high:
        # STEP 1: Partition the array around a pivot
        # This rearranges elements so pivot is in correct position
        # and returns the pivot's final index
        pivot_index = partition(arr, low, high)
        
        # STEP 2: Recursively sort the left subarray (elements < pivot)
        # Sort from start of subarray to position just before pivot
        quicksort(arr, low, pivot_index - 1)
        
        # STEP 3: Recursively sort the right subarray (elements > pivot)
        # Sort from position just after pivot to end of subarray
        quicksort(arr, pivot_index + 1, high)
        
        # No explicit combine step needed - elements are already in correct positions


def quicksort_wrapper(arr: List[int]) -> Tuple[List[int], float, float]:
    """
    Wrapper function for Quicksort that includes performance tracking.
    
    This function provides a clean interface for running Quicksort with
    performance measurement. It:
    1. Sets up reproducible random seed for consistent results
    2. Creates a copy of input data to avoid modifying original
    3. Tracks execution time and memory usage
    4. Returns sorted data along with performance metrics
    
    Args:
        arr: List of integers to be sorted (original is not modified)
    
    Returns:
        Tuple containing:
        - List[int]: Sorted copy of the input array
        - float: Execution time in seconds
        - float: Memory usage in MB
    """
    import random
    
    # Set seed for reproducible results across multiple runs
    # This ensures that the same random pivot selections are made each time
    random.seed(42)
    
    # Create a copy to avoid modifying the original array
    # This is important for testing multiple algorithms on the same data
    arr_copy = arr.copy()
    
    # Initialize performance tracker
    tracker = PerformanceTracker()
    
    # Start performance tracking (records start time and memory)
    tracker.start_tracking()
    
    # Perform the actual sorting operation
    quicksort(arr_copy, 0, len(arr_copy) - 1)
    
    # Stop tracking and get performance metrics
    execution_time, memory_usage = tracker.stop_tracking()
    
    # Return sorted data and performance metrics
    return arr_copy, execution_time, memory_usage


def load_dataset(filename: str) -> List[int]:
    """
    Load dataset from a text file.
    
    This utility function reads a dataset file where each line contains
    a single integer value. It handles common file I/O errors gracefully
    and provides informative error messages.
    
    Args:
        filename: Path to the dataset file
    
    Returns:
        List[int]: List of integers from the dataset
        
    Raises:
        SystemExit: If file is not found or contains invalid data
    """
    try:
        # Open file in read mode and process each line
        with open(filename, 'r') as file:
            # Read all lines, strip whitespace, filter empty lines,
            # and convert each line to an integer
            data = [int(line.strip()) for line in file if line.strip()]
        return data
        
    except FileNotFoundError:
        # Handle case where file doesn't exist
        print(f"Error: Dataset file '{filename}' not found.")
        sys.exit(1)
        
    except ValueError as e:
        # Handle case where file contains non-integer data
        print(f"Error: Invalid data format in '{filename}': {e}")
        sys.exit(1)


def main():
    """
    Main function to demonstrate Quicksort with different datasets.
    
    This function serves as a standalone test runner for the Quicksort
    implementation. It loads multiple datasets, runs Quicksort on each,
    and displays detailed performance results including:
    - Execution time
    - Memory usage
    - Sorting verification
    - Sample of sorted data
    """
    print("Quicksort Algorithm Performance Analysis")
    print("=" * 50)
    
    # List of datasets to test - covers different input characteristics
    datasets = [
        "datasets/sorted_data.txt",        # Best case for Quicksort
        "datasets/reverse_sorted_data.txt", # Worst case for Quicksort
        "datasets/random_data.txt"         # Average case for Quicksort
    ]
    
    # Test Quicksort on each dataset
    for dataset_path in datasets:
        print(f"\nTesting with dataset: {dataset_path}")
        print("-" * 40)
        
        # Load dataset from file
        data = load_dataset(dataset_path)
        print(f"Dataset size: {len(data)} elements")
        print(f"First 10 elements: {data[:10]}")
        
        # Sort and measure performance
        sorted_data, exec_time, memory_usage = quicksort_wrapper(data)
        
        # Display comprehensive results
        print(f"Sorting completed!")
        print(f"Execution time: {exec_time:.6f} seconds")
        print(f"Memory usage: {memory_usage:.2f} MB")
        print(f"First 10 sorted elements: {sorted_data[:10]}")
        
        # Verify that sorting was performed correctly
        # Check that each element is <= the next element (ascending order)
        is_sorted = all(sorted_data[i] <= sorted_data[i+1] for i in range(len(sorted_data)-1))
        print(f"Sorting verification: {'✓ PASSED' if is_sorted else '✗ FAILED'}")


if __name__ == "__main__":
    main()