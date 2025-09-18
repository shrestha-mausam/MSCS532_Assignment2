#!/usr/bin/env python3
"""
Mergesort Implementation with Performance Analysis

This module implements the Mergesort algorithm with detailed comments and
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
    
    This function merges two sorted subarrays into a single sorted array.
    It's the core "combine" step of the divide-and-conquer Mergesort algorithm.
    
    The merge process works by:
    1. Creating temporary arrays to hold the two sorted subarrays
    2. Comparing elements from both subarrays one by one
    3. Placing the smaller element in the correct position
    4. Copying any remaining elements from either subarray
    
    This function modifies the original array in-place, merging the sorted
    subarrays arr[left..mid] and arr[mid+1..right] into a single sorted
    subarray arr[left..right].
    
    Args:
        arr: List of integers containing the subarrays to be merged (modified in-place)
        left: Starting index of the first subarray
        mid: Ending index of the first subarray (also starting index of second subarray)
        right: Ending index of the second subarray
    """
    # STEP 1: Calculate sizes of the two subarrays to be merged
    n1 = mid - left + 1  # Size of left subarray (arr[left..mid])
    n2 = right - mid     # Size of right subarray (arr[mid+1..right])
    
    # STEP 2: Create temporary arrays to hold the subarrays
    # These temporary arrays will store copies of the subarrays
    # so we can merge them back into the original array
    left_arr = [0] * n1   # Temporary array for left subarray
    right_arr = [0] * n2  # Temporary array for right subarray
    
    # STEP 3: Copy data to temporary arrays
    # Copy elements from left subarray to left_arr
    for i in range(n1):
        left_arr[i] = arr[left + i]
    
    # Copy elements from right subarray to right_arr
    for j in range(n2):
        right_arr[j] = arr[mid + 1 + j]
    
    # STEP 4: Initialize indices for merging
    i = 0      # Initial index of first subarray (left_arr)
    j = 0      # Initial index of second subarray (right_arr)
    k = left   # Initial index of merged subarray (original arr)
    
    # STEP 5: Merge the temporary arrays back into arr[left..right]
    # Compare elements from both subarrays and place the smaller one
    while i < n1 and j < n2:
        # If element from left subarray is smaller or equal
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]  # Place left element
            i += 1                # Move to next element in left subarray
        else:
            arr[k] = right_arr[j] # Place right element
            j += 1                # Move to next element in right subarray
        k += 1  # Move to next position in merged array
    
    # STEP 6: Copy remaining elements of left_arr[], if any
    # This handles the case where right subarray is exhausted first
    while i < n1:
        arr[k] = left_arr[i]
        i += 1
        k += 1
    
    # STEP 7: Copy remaining elements of right_arr[], if any
    # This handles the case where left subarray is exhausted first
    while j < n2:
        arr[k] = right_arr[j]
        j += 1
        k += 1


def mergesort(arr: List[int], left: int, right: int) -> None:
    """
    Main Mergesort function that recursively sorts the array.
    
    Mergesort is a divide-and-conquer algorithm that works by:
    1. Dividing the input array into two equal halves
    2. Recursively sorting both halves
    3. Merging the two sorted halves into a single sorted array
    
    The key advantage of Mergesort is its consistent performance:
    - It always divides the array into equal halves
    - It guarantees O(n log n) performance regardless of input characteristics
    - It's a stable sorting algorithm (preserves relative order of equal elements)
    
    Time Complexity Analysis:
        - Best Case: O(n log n) - always divides array into equal halves
        - Average Case: O(n log n) - consistent performance regardless of input
        - Worst Case: O(n log n) - stable performance even with worst-case input
    
    Space Complexity: O(n) - requires additional space for temporary arrays
    
    Args:
        arr: List of integers to be sorted (modified in-place)
        left: Starting index of the subarray to sort
        right: Ending index of the subarray to sort
    """
    # Base case: if there's only one element or no elements, array is already sorted
    if left < right:
        # STEP 1: Find the middle point to divide the array into two halves
        # Using (left + right) // 2 could cause integer overflow for large arrays
        # So we use: left + (right - left) // 2
        mid = left + (right - left) // 2
        
        # STEP 2: Recursively sort first and second halves
        # This is the "divide" step - we split the problem into smaller subproblems
        mergesort(arr, left, mid)      # Sort left half (arr[left..mid])
        mergesort(arr, mid + 1, right)  # Sort right half (arr[mid+1..right])
        
        # STEP 3: Merge the sorted halves
        # This is the "conquer" step - we combine the solutions of subproblems
        merge(arr, left, mid, right)


def mergesort_wrapper(arr: List[int]) -> Tuple[List[int], float, float]:
    """
    Wrapper function for Mergesort that includes performance tracking.
    
    This function provides a clean interface for running Mergesort with
    performance measurement. It:
    1. Creates a copy of input data to avoid modifying original
    2. Tracks execution time and memory usage
    3. Returns sorted data along with performance metrics
    
    Unlike Quicksort, Mergesort doesn't need random seed setup since
    it doesn't use randomization in its algorithm.
    
    Args:
        arr: List of integers to be sorted (original is not modified)
    
    Returns:
        Tuple containing:
        - List[int]: Sorted copy of the input array
        - float: Execution time in seconds
        - float: Memory usage in MB
    """
    # Create a copy to avoid modifying the original array
    # This is important for testing multiple algorithms on the same data
    arr_copy = arr.copy()
    
    # Initialize performance tracker
    tracker = PerformanceTracker()
    
    # Start performance tracking (records start time and memory)
    tracker.start_tracking()
    
    # Perform the actual sorting operation
    mergesort(arr_copy, 0, len(arr_copy) - 1)
    
    # Stop tracking and get performance metrics
    execution_time, memory_usage = tracker.stop_tracking()
    
    # Return sorted data and performance metrics
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
    """
    Main function to demonstrate Mergesort with different datasets.
    
    This function serves as a standalone test runner for the Mergesort
    implementation. It loads multiple datasets, runs Mergesort on each,
    and displays detailed performance results including:
    - Execution time
    - Memory usage
    - Sorting verification
    - Sample of sorted data
    
    Unlike Quicksort, Mergesort shows consistent performance across
    all input types (sorted, reverse sorted, random).
    """
    print("Mergesort Algorithm Performance Analysis")
    print("=" * 50)
    
    # List of datasets to test - covers different input characteristics
    datasets = [
        "datasets/sorted_data.txt",        # Consistent performance
        "datasets/reverse_sorted_data.txt", # Consistent performance
        "datasets/random_data.txt"         # Consistent performance
    ]
    
    # Test Mergesort on each dataset
    for dataset_path in datasets:
        print(f"\nTesting with dataset: {dataset_path}")
        print("-" * 40)
        
        # Load dataset from file
        data = load_dataset(dataset_path)
        print(f"Dataset size: {len(data)} elements")
        print(f"First 10 elements: {data[:10]}")
        
        # Sort and measure performance
        sorted_data, exec_time, memory_usage = mergesort_wrapper(data)
        
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