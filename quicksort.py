#!/usr/bin/env python3
"""
Quicksort Implementation with Performance Analysis

This module implements the Quicksort algorithm with detailed comments and
performance tracking capabilities including execution time and memory usage.

Author: Assignment 2 - Sorting Algorithms Analysis
Date: 2024
"""

import time
import psutil
import os
import sys
from typing import List, Tuple, Optional


class PerformanceTracker:
    """Class to track performance metrics during sorting operations."""
    
    def __init__(self):
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.start_memory: Optional[float] = None
        self.end_memory: Optional[float] = None
        self.process = psutil.Process(os.getpid())
    
    def start_tracking(self) -> None:
        """Start tracking performance metrics."""
        self.start_time = time.time()
        self.start_memory = self.process.memory_info().rss / 1024 / 1024  # MB
    
    def stop_tracking(self) -> Tuple[float, float]:
        """Stop tracking and return execution time and memory usage."""
        self.end_time = time.time()
        self.end_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        
        execution_time = self.end_time - self.start_time
        memory_usage = self.end_memory - self.start_memory
        
        return execution_time, memory_usage


def partition(arr: List[int], low: int, high: int) -> int:
    """
    Partition function for Quicksort algorithm.
    
    This function uses a randomized pivot selection to avoid worst-case
    performance on already sorted data. It places the pivot at its correct
    position in sorted array, and places all smaller elements to left of pivot
    and all greater elements to right of pivot.
    
    Args:
        arr: List of integers to be partitioned
        low: Starting index of the subarray
        high: Ending index of the subarray
    
    Returns:
        int: The index of the pivot element after partitioning
    """
    import random
    
    # Choose a random pivot to avoid worst-case performance
    pivot_index = random.randint(low, high)
    pivot = arr[pivot_index]
    
    # Move pivot to the end
    arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
    
    # Index of smaller element (indicates right position of pivot)
    i = low - 1
    
    # Traverse through all elements in the subarray
    for j in range(low, high):
        # If current element is smaller than or equal to pivot
        if arr[j] <= pivot:
            # Increment index of smaller element
            i += 1
            # Swap elements at positions i and j
            arr[i], arr[j] = arr[j], arr[i]
    
    # Place pivot in its correct position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    
    return i + 1


def quicksort(arr: List[int], low: int, high: int) -> None:
    """
    Main Quicksort function that recursively sorts the array.
    
    Quicksort is a divide-and-conquer algorithm that works by selecting a 'pivot'
    element from the array and partitioning the other elements into two sub-arrays,
    according to whether they are less than or greater than the pivot.
    
    Time Complexity:
        - Best Case: O(n log n) - when pivot divides array into equal halves
        - Average Case: O(n log n) - expected performance with random data
        - Worst Case: O(n²) - when pivot is always the smallest or largest element
    
    Space Complexity: O(log n) - due to recursive call stack
    
    Args:
        arr: List of integers to be sorted
        low: Starting index of the subarray
        high: Ending index of the subarray
    """
    if low < high:
        # Partition the array and get pivot index
        pivot_index = partition(arr, low, high)
        
        # Recursively sort elements before and after partition
        quicksort(arr, low, pivot_index - 1)  # Sort left subarray
        quicksort(arr, pivot_index + 1, high)  # Sort right subarray


def quicksort_wrapper(arr: List[int]) -> Tuple[List[int], float, float]:
    """
    Wrapper function for Quicksort that includes performance tracking.
    
    Args:
        arr: List of integers to be sorted
    
    Returns:
        Tuple containing:
        - Sorted list
        - Execution time in seconds
        - Memory usage in MB
    """
    import random
    
    # Set seed for reproducible results
    random.seed(42)
    
    # Create a copy to avoid modifying the original array
    arr_copy = arr.copy()
    
    # Initialize performance tracker
    tracker = PerformanceTracker()
    
    # Start performance tracking
    tracker.start_tracking()
    
    # Perform the sorting
    quicksort(arr_copy, 0, len(arr_copy) - 1)
    
    # Stop tracking and get metrics
    execution_time, memory_usage = tracker.stop_tracking()
    
    return arr_copy, execution_time, memory_usage


def load_dataset(filename: str) -> List[int]:
    """
    Load dataset from a file.
    
    Args:
        filename: Path to the dataset file
    
    Returns:
        List of integers from the dataset
    """
    try:
        with open(filename, 'r') as file:
            # Read all lines and convert to integers
            data = [int(line.strip()) for line in file if line.strip()]
        return data
    except FileNotFoundError:
        print(f"Error: Dataset file '{filename}' not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Invalid data format in '{filename}': {e}")
        sys.exit(1)


def main():
    """Main function to demonstrate Quicksort with different datasets."""
    print("Quicksort Algorithm Performance Analysis")
    print("=" * 50)
    
    # List of datasets to test
    datasets = [
        "datasets/sorted_data.txt",
        "datasets/reverse_sorted_data.txt", 
        "datasets/random_data.txt"
    ]
    
    for dataset_path in datasets:
        print(f"\nTesting with dataset: {dataset_path}")
        print("-" * 40)
        
        # Load dataset
        data = load_dataset(dataset_path)
        print(f"Dataset size: {len(data)} elements")
        print(f"First 10 elements: {data[:10]}")
        
        # Sort and measure performance
        sorted_data, exec_time, memory_usage = quicksort_wrapper(data)
        
        # Display results
        print(f"Sorting completed!")
        print(f"Execution time: {exec_time:.6f} seconds")
        print(f"Memory usage: {memory_usage:.2f} MB")
        print(f"First 10 sorted elements: {sorted_data[:10]}")
        
        # Verify sorting is correct
        is_sorted = all(sorted_data[i] <= sorted_data[i+1] for i in range(len(sorted_data)-1))
        print(f"Sorting verification: {'✓ PASSED' if is_sorted else '✗ FAILED'}")


if __name__ == "__main__":
    main()