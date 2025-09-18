#!/usr/bin/env python3
"""
Comprehensive Performance Analysis Script

This script runs both Quicksort and Mergesort algorithms on various datasets
and provides detailed performance analysis including execution time, memory usage,
and comparative analysis.

Author: Mausam Shrestha
Date: 2025
"""

import time
import psutil
import os
import sys
import glob
from typing import List, Dict, Tuple
import json

# Import our sorting algorithms
from quicksort import quicksort_wrapper
from mergesort import mergesort_wrapper


class PerformanceAnalyzer:
    """
    Class to analyze and compare performance of sorting algorithms.
    
    This class provides comprehensive performance analysis capabilities for
    comparing Quicksort and Mergesort algorithms. It handles:
    - Dataset discovery and loading
    - Algorithm execution and performance measurement
    - Result collection and analysis
    - Report generation and data export
    
    The analyzer is designed to work with multiple datasets and provides
    detailed insights into algorithm performance characteristics.
    """
    
    def __init__(self):
        """Initialize the performance analyzer with empty results storage."""
        # Dictionary to store analysis results for each dataset
        # Format: {'dataset_name': {'quicksort': {...}, 'mergesort': {...}}}
        self.results = {}
    
    def analyze_dataset(self, dataset_path: str) -> Dict:
        """
        Analyze performance of both algorithms on a single dataset.
        
        This method performs a comprehensive analysis of a single dataset by:
        1. Loading the dataset from file
        2. Running both Quicksort and Mergesort on the same data
        3. Measuring execution time and memory usage for each algorithm
        4. Verifying that sorting was performed correctly
        5. Comparing performance between the two algorithms
        6. Returning detailed results for further analysis
        
        Args:
            dataset_path: Path to the dataset file to analyze
            
        Returns:
            Dict: Comprehensive results including timing, memory, and comparison data
        """
        # Display analysis header with visual separators
        print(f"\nAnalyzing dataset: {dataset_path}")
        print("=" * 60)
        
        # Load dataset from file with error handling
        try:
            with open(dataset_path, 'r') as file:
                # Read all lines, strip whitespace, filter empty lines,
                # and convert each line to an integer
                data = [int(line.strip()) for line in file if line.strip()]
        except FileNotFoundError:
            print(f"Error: Dataset file '{dataset_path}' not found.")
            return {}
        except ValueError as e:
            print(f"Error: Invalid data format in '{dataset_path}': {e}")
            return {}
        
        # Extract dataset information for display and storage
        dataset_name = os.path.basename(dataset_path).replace('.txt', '')
        dataset_size = len(data)
        
        # Display dataset information
        print(f"Dataset: {dataset_name}")
        print(f"Size: {dataset_size} elements")
        print(f"First 10 elements: {data[:10]}")
        
        # Initialize result structure to store all performance metrics
        results = {
            'dataset_name': dataset_name,
            'dataset_size': dataset_size,
            'quicksort': {},  # Will be populated with quicksort results
            'mergesort': {}   # Will be populated with mergesort results
        }
        
        # Test Quicksort Algorithm
        print(f"\nTesting Quicksort...")
        print("-" * 30)
        try:
            # Call the quicksort wrapper which handles performance tracking
            # Returns: (sorted_array, execution_time, memory_usage)
            sorted_data_qs, exec_time_qs, memory_qs = quicksort_wrapper(data)
            
            # Store successful results in our results dictionary
            results['quicksort'] = {
                'execution_time': exec_time_qs,
                'memory_usage': memory_qs,
                'success': True
            }
            
            # Display performance results
            print(f"✓ Quicksort completed in {exec_time_qs:.6f} seconds")
            print(f"✓ Memory usage: {memory_qs:.2f} MB")
            
            # Verify that the sorting was performed correctly
            # Check that each element is <= the next element (ascending order)
            is_sorted = all(sorted_data_qs[i] <= sorted_data_qs[i+1] for i in range(len(sorted_data_qs)-1))
            print(f"✓ Sorting verification: {'PASSED' if is_sorted else 'FAILED'}")
            
        except Exception as e:
            # Handle any errors that occur during quicksort execution
            print(f"✗ Quicksort failed: {e}")
            results['quicksort'] = {
                'execution_time': None,
                'memory_usage': None,
                'success': False,
                'error': str(e)
            }
        
        # Test Mergesort Algorithm
        print(f"\nTesting Mergesort...")
        print("-" * 30)
        try:
            # Call the mergesort wrapper which handles performance tracking
            # Returns: (sorted_array, execution_time, memory_usage)
            sorted_data_ms, exec_time_ms, memory_ms = mergesort_wrapper(data)
            
            # Store successful results in our results dictionary
            results['mergesort'] = {
                'execution_time': exec_time_ms,
                'memory_usage': memory_ms,
                'success': True
            }
            
            # Display performance results
            print(f"✓ Mergesort completed in {exec_time_ms:.6f} seconds")
            print(f"✓ Memory usage: {memory_ms:.2f} MB")
            
            # Verify that the sorting was performed correctly
            # Check that each element is <= the next element (ascending order)
            is_sorted = all(sorted_data_ms[i] <= sorted_data_ms[i+1] for i in range(len(sorted_data_ms)-1))
            print(f"✓ Sorting verification: {'PASSED' if is_sorted else 'FAILED'}")
            
        except Exception as e:
            # Handle any errors that occur during mergesort execution
            print(f"✗ Mergesort failed: {e}")
            results['mergesort'] = {
                'execution_time': None,
                'memory_usage': None,
                'success': False,
                'error': str(e)
            }
        
        # Compare Performance Between Algorithms
        if results['quicksort']['success'] and results['mergesort']['success']:
            print(f"\nPerformance Comparison:")
            print("-" * 30)
            
            # Extract performance metrics for comparison
            time_diff = results['quicksort']['execution_time'] - results['mergesort']['execution_time']
            memory_diff = results['quicksort']['memory_usage'] - results['mergesort']['memory_usage']
            
            # Determine which algorithm was faster
            faster_algorithm = "Quicksort" if time_diff < 0 else "Mergesort"
            time_advantage = abs(time_diff)
            
            # Display comparison results
            print(f"Faster algorithm: {faster_algorithm} (by {time_advantage:.6f} seconds)")
            print(f"Time difference: {time_diff:.6f} seconds")
            print(f"Memory difference: {memory_diff:.2f} MB")
            
            # Calculate and display speedup ratio (avoid division by zero)
            if results['mergesort']['execution_time'] > 0:
                speedup = results['quicksort']['execution_time'] / results['mergesort']['execution_time']
                print(f"Speedup ratio (QS/MS): {speedup:.2f}x")
        
        return results
    
    def analyze_all_datasets(self) -> None:
        """
        Analyze performance on all available datasets.
        
        This method performs comprehensive analysis by:
        1. Discovering all dataset files in the datasets directory
        2. Running analysis on each dataset individually
        3. Collecting all results for summary generation
        4. Generating a comprehensive summary report
        5. Saving detailed results to JSON for further analysis
        """
        # Display analysis header
        print("Comprehensive Sorting Algorithm Performance Analysis")
        print("=" * 70)
        
        # Step 1: Find all dataset files using glob pattern matching
        dataset_files = glob.glob("datasets/*.txt")
        dataset_files.sort()  # Sort for consistent ordering
        
        # Check if any datasets were found
        if not dataset_files:
            print("No dataset files found in the 'datasets' directory.")
            return
        
        # Display discovered datasets
        print(f"Found {len(dataset_files)} dataset files:")
        for file in dataset_files:
            print(f"  - {file}")
        
        # Step 2: Initialize results storage
        all_results = {}
        
        # Step 3: Analyze each dataset individually
        for dataset_file in dataset_files:
            results = self.analyze_dataset(dataset_file)
            if results:
                # Store results using dataset name as key
                all_results[results['dataset_name']] = results
        
        # Step 4: Generate comprehensive summary report
        self.generate_summary_report(all_results)
        
        # Step 5: Save detailed results to JSON file
        self.save_results_to_json(all_results)
    
    def generate_summary_report(self, results: Dict) -> None:
        """
        Generate a comprehensive summary report of all performance tests.
        
        This method creates a detailed summary by:
        1. Grouping results by dataset type (sorted, reverse sorted, random)
        2. Analyzing performance within each category
        3. Displaying comparative results for each dataset
        4. Highlighting performance winners and speedup ratios
        
        Args:
            results: Dictionary containing all analysis results
        """
        # Display report header
        print(f"\n{'='*70}")
        print("PERFORMANCE SUMMARY REPORT")
        print(f"{'='*70}")
        
        # Step 1: Group results by dataset type for organized analysis
        sorted_results = []      # Pre-sorted ascending data
        reverse_results = []    # Reverse sorted data
        random_results = []     # Random data
        
        # Categorize each dataset based on its name
        for dataset_name, data in results.items():
            if 'sorted' in dataset_name and 'reverse' not in dataset_name:
                sorted_results.append(data)
            elif 'reverse' in dataset_name:
                reverse_results.append(data)
            elif 'random' in dataset_name:
                random_results.append(data)
        
        # Step 2: Analyze each category separately
        categories = [
            ("SORTED DATA", sorted_results),      # Best case for Quicksort
            ("REVERSE SORTED DATA", reverse_results),  # Worst case for Quicksort
            ("RANDOM DATA", random_results)       # Average case for both
        ]
        
        for category_name, category_results in categories:
            # Skip empty categories
            if not category_results:
                continue
                
            # Display category header
            print(f"\n{category_name} ANALYSIS:")
            print("-" * 50)
            
            # Step 3: Analyze each dataset in the category
            for result in category_results:
                dataset_name = result['dataset_name']
                size = result['dataset_size']
                
                print(f"\nDataset: {dataset_name} (Size: {size})")
                
                # Check if both algorithms completed successfully
                if result['quicksort']['success'] and result['mergesort']['success']:
                    # Extract performance metrics
                    qs_time = result['quicksort']['execution_time']
                    ms_time = result['mergesort']['execution_time']
                    qs_mem = result['quicksort']['memory_usage']
                    ms_mem = result['mergesort']['memory_usage']
                    
                    # Display performance results
                    print(f"  Quicksort:  {qs_time:.6f}s, {qs_mem:.2f}MB")
                    print(f"  Mergesort:  {ms_time:.6f}s, {ms_mem:.2f}MB")
                    
                    # Determine winner and calculate speedup
                    faster = "Quicksort" if qs_time < ms_time else "Mergesort"
                    speedup = max(qs_time, ms_time) / min(qs_time, ms_time)
                    print(f"  Winner: {faster} ({speedup:.2f}x faster)")
                else:
                    # Handle failed analyses
                    print("  Analysis failed - check individual results above")
    
    def save_results_to_json(self, results: Dict) -> None:
        """
        Save detailed results to a JSON file for further analysis.
        
        This method exports all performance data to a JSON file, allowing
        for external analysis, visualization, or integration with other tools.
        The JSON format preserves all timing, memory, and comparison data.
        
        Args:
            results: Dictionary containing all analysis results
        """
        filename = "performance_results.json"
        try:
            # Open file in write mode and save results with pretty formatting
            with open(filename, 'w') as file:
                json.dump(results, file, indent=2)  # indent=2 for readable formatting
            print(f"\nDetailed results saved to: {filename}")
        except Exception as e:
            # Handle any file I/O errors
            print(f"Error saving results to JSON: {e}")


def main():
    """
    Main function to run comprehensive performance analysis.
    
    This function serves as the entry point for the performance analysis script.
    It creates a PerformanceAnalyzer instance and runs the complete analysis
    workflow on all available datasets.
    
    The analysis includes:
    - Dataset discovery and loading
    - Algorithm execution and performance measurement
    - Comprehensive result analysis and reporting
    - Data export for further analysis
    """
    # Create analyzer instance
    analyzer = PerformanceAnalyzer()
    
    # Run comprehensive analysis on all datasets
    analyzer.analyze_all_datasets()


if __name__ == "__main__":
    main()