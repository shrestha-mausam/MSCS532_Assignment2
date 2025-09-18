#!/usr/bin/env python3
"""
Mergesort Implementation with Performance Analysis

This module implements the Mergesort algorithm with detailed comments and
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


def merge(arr: List[int], left: int, mid: int, right: int) -> None:
    """
    Merge function for Mergesort algorithm.
    
    This function merges two sorted subarrays of arr[]. The first subarray is
    arr[left..mid] and the second subarray is arr[mid+1..right]. After merging,
    the entire array from left to right becomes sorted.
    
    Args:
        arr: List of integers containing the subarrays to be merged
        left: Starting index of the first subarray
        mid: Ending index of the first subarray (also starting index of second subarray)
        right: Ending index of the second subarray
    """
    # Calculate sizes of the two subarrays to be merged
    n1 = mid - left + 1  # Size of left subarray
    n2 = right - mid     # Size of right subarray
    
    # Create temporary arrays to hold the subarrays
    left_arr = [0] * n1
    right_arr = [0] * n2
    
    # Copy data to temporary arrays
    for i in range(n1):
        left_arr[i] = arr[left + i]
    
    for j in range(n2):
        right_arr[j] = arr[mid + 1 + j]
    
    # Merge the temporary arrays back into arr[left..right]
    i = 0  # Initial index of first subarray
    j = 0  # Initial index of second subarray
    k = left  # Initial index of merged subarray
    
    # Compare elements from both subarrays and merge them
    while i < n1 and j < n2:
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1
    
    # Copy remaining elements of left_arr[], if any
    while i < n1:
        arr[k] = left_arr[i]
        i += 1
        k += 1
    
    # Copy remaining elements of right_arr[], if any
    while j < n2:
        arr[k] = right_arr[j]
        j += 1
        k += 1


def mergesort(arr: List[int], left: int, right: int) -> None:
    """
    Main Mergesort function that recursively sorts the array.
    
    Mergesort is a divide-and-conquer algorithm that divides the input array
    into two halves, calls itself for the two halves, and then merges the
    two sorted halves.
    
    Time Complexity:
        - Best Case: O(n log n) - always divides array into equal halves
        - Average Case: O(n log n) - consistent performance regardless of input
        - Worst Case: O(n log n) - stable performance even with worst-case input
    
    Space Complexity: O(n) - requires additional space for temporary arrays
    
    Args:
        arr: List of integers to be sorted
        left: Starting index of the subarray
        right: Ending index of the subarray
    """
    if left < right:
        # Find the middle point to divide the array into two halves
        mid = left + (right - left) // 2
        
        # Recursively sort first and second halves
        mergesort(arr, left, mid)      # Sort left half
        mergesort(arr, mid + 1, right)  # Sort right half
        
        # Merge the sorted halves
        merge(arr, left, mid, right)


def mergesort_wrapper(arr: List[int]) -> Tuple[List[int], float, float]:
    """
    Wrapper function for Mergesort that includes performance tracking.
    
    Args:
        arr: List of integers to be sorted
    
    Returns:
        Tuple containing:
        - Sorted list
        - Execution time in seconds
        - Memory usage in MB
    """
    # Create a copy to avoid modifying the original array
    arr_copy = arr.copy()
    
    # Initialize performance tracker
    tracker = PerformanceTracker()
    
    # Start performance tracking
    tracker.start_tracking()
    
    # Perform the sorting
    mergesort(arr_copy, 0, len(arr_copy) - 1)
    
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
    """Main function to demonstrate Mergesort with different datasets."""
    print("Mergesort Algorithm Performance Analysis")
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
        sorted_data, exec_time, memory_usage = mergesort_wrapper(data)
        
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