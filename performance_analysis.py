#!/usr/bin/env python3
"""
Comprehensive Performance Analysis Script

This script runs both Quicksort and Mergesort algorithms on various datasets
and provides detailed performance analysis including execution time, memory usage,
and comparative analysis.

Author: Assignment 2 - Sorting Algorithms Analysis
Date: 2024
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
    """Class to analyze and compare performance of sorting algorithms."""
    
    def __init__(self):
        self.results = {}
    
    def analyze_dataset(self, dataset_path: str) -> Dict:
        """
        Analyze performance of both algorithms on a single dataset.
        
        Args:
            dataset_path: Path to the dataset file
            
        Returns:
            Dictionary containing performance metrics for both algorithms
        """
        print(f"\nAnalyzing dataset: {dataset_path}")
        print("=" * 60)
        
        # Load dataset
        try:
            with open(dataset_path, 'r') as file:
                data = [int(line.strip()) for line in file if line.strip()]
        except FileNotFoundError:
            print(f"Error: Dataset file '{dataset_path}' not found.")
            return {}
        except ValueError as e:
            print(f"Error: Invalid data format in '{dataset_path}': {e}")
            return {}
        
        dataset_name = os.path.basename(dataset_path).replace('.txt', '')
        dataset_size = len(data)
        
        print(f"Dataset: {dataset_name}")
        print(f"Size: {dataset_size} elements")
        print(f"First 10 elements: {data[:10]}")
        
        results = {
            'dataset_name': dataset_name,
            'dataset_size': dataset_size,
            'quicksort': {},
            'mergesort': {}
        }
        
        # Test Quicksort
        print(f"\nTesting Quicksort...")
        print("-" * 30)
        try:
            sorted_data_qs, exec_time_qs, memory_qs = quicksort_wrapper(data)
            results['quicksort'] = {
                'execution_time': exec_time_qs,
                'memory_usage': memory_qs,
                'success': True
            }
            print(f"✓ Quicksort completed in {exec_time_qs:.6f} seconds")
            print(f"✓ Memory usage: {memory_qs:.2f} MB")
            
            # Verify sorting
            is_sorted = all(sorted_data_qs[i] <= sorted_data_qs[i+1] for i in range(len(sorted_data_qs)-1))
            print(f"✓ Sorting verification: {'PASSED' if is_sorted else 'FAILED'}")
            
        except Exception as e:
            print(f"✗ Quicksort failed: {e}")
            results['quicksort'] = {
                'execution_time': None,
                'memory_usage': None,
                'success': False,
                'error': str(e)
            }
        
        # Test Mergesort
        print(f"\nTesting Mergesort...")
        print("-" * 30)
        try:
            sorted_data_ms, exec_time_ms, memory_ms = mergesort_wrapper(data)
            results['mergesort'] = {
                'execution_time': exec_time_ms,
                'memory_usage': memory_ms,
                'success': True
            }
            print(f"✓ Mergesort completed in {exec_time_ms:.6f} seconds")
            print(f"✓ Memory usage: {memory_ms:.2f} MB")
            
            # Verify sorting
            is_sorted = all(sorted_data_ms[i] <= sorted_data_ms[i+1] for i in range(len(sorted_data_ms)-1))
            print(f"✓ Sorting verification: {'PASSED' if is_sorted else 'FAILED'}")
            
        except Exception as e:
            print(f"✗ Mergesort failed: {e}")
            results['mergesort'] = {
                'execution_time': None,
                'memory_usage': None,
                'success': False,
                'error': str(e)
            }
        
        # Compare performance
        if results['quicksort']['success'] and results['mergesort']['success']:
            print(f"\nPerformance Comparison:")
            print("-" * 30)
            time_diff = results['quicksort']['execution_time'] - results['mergesort']['execution_time']
            memory_diff = results['quicksort']['memory_usage'] - results['mergesort']['memory_usage']
            
            faster_algorithm = "Quicksort" if time_diff < 0 else "Mergesort"
            time_advantage = abs(time_diff)
            
            print(f"Faster algorithm: {faster_algorithm} (by {time_advantage:.6f} seconds)")
            print(f"Time difference: {time_diff:.6f} seconds")
            print(f"Memory difference: {memory_diff:.2f} MB")
            
            # Calculate speedup ratio
            if results['mergesort']['execution_time'] > 0:
                speedup = results['quicksort']['execution_time'] / results['mergesort']['execution_time']
                print(f"Speedup ratio (QS/MS): {speedup:.2f}x")
        
        return results
    
    def analyze_all_datasets(self) -> None:
        """Analyze performance on all available datasets."""
        print("Comprehensive Sorting Algorithm Performance Analysis")
        print("=" * 70)
        
        # Find all dataset files
        dataset_files = glob.glob("datasets/*.txt")
        dataset_files.sort()
        
        if not dataset_files:
            print("No dataset files found in the 'datasets' directory.")
            return
        
        print(f"Found {len(dataset_files)} dataset files:")
        for file in dataset_files:
            print(f"  - {file}")
        
        all_results = {}
        
        # Analyze each dataset
        for dataset_file in dataset_files:
            results = self.analyze_dataset(dataset_file)
            if results:
                all_results[results['dataset_name']] = results
        
        # Generate summary report
        self.generate_summary_report(all_results)
        
        # Save detailed results to JSON
        self.save_results_to_json(all_results)
    
    def generate_summary_report(self, results: Dict) -> None:
        """Generate a summary report of all performance tests."""
        print(f"\n{'='*70}")
        print("PERFORMANCE SUMMARY REPORT")
        print(f"{'='*70}")
        
        # Group results by dataset type
        sorted_results = []
        reverse_results = []
        random_results = []
        
        for dataset_name, data in results.items():
            if 'sorted' in dataset_name and 'reverse' not in dataset_name:
                sorted_results.append(data)
            elif 'reverse' in dataset_name:
                reverse_results.append(data)
            elif 'random' in dataset_name:
                random_results.append(data)
        
        # Analyze each category
        categories = [
            ("SORTED DATA", sorted_results),
            ("REVERSE SORTED DATA", reverse_results),
            ("RANDOM DATA", random_results)
        ]
        
        for category_name, category_results in categories:
            if not category_results:
                continue
                
            print(f"\n{category_name} ANALYSIS:")
            print("-" * 50)
            
            for result in category_results:
                dataset_name = result['dataset_name']
                size = result['dataset_size']
                
                print(f"\nDataset: {dataset_name} (Size: {size})")
                
                if result['quicksort']['success'] and result['mergesort']['success']:
                    qs_time = result['quicksort']['execution_time']
                    ms_time = result['mergesort']['execution_time']
                    qs_mem = result['quicksort']['memory_usage']
                    ms_mem = result['mergesort']['memory_usage']
                    
                    print(f"  Quicksort:  {qs_time:.6f}s, {qs_mem:.2f}MB")
                    print(f"  Mergesort:  {ms_time:.6f}s, {ms_mem:.2f}MB")
                    
                    faster = "Quicksort" if qs_time < ms_time else "Mergesort"
                    speedup = max(qs_time, ms_time) / min(qs_time, ms_time)
                    print(f"  Winner: {faster} ({speedup:.2f}x faster)")
                else:
                    print("  Analysis failed - check individual results above")
    
    def save_results_to_json(self, results: Dict) -> None:
        """Save detailed results to a JSON file."""
        filename = "performance_results.json"
        try:
            with open(filename, 'w') as file:
                json.dump(results, file, indent=2)
            print(f"\nDetailed results saved to: {filename}")
        except Exception as e:
            print(f"Error saving results to JSON: {e}")


def main():
    """Main function to run comprehensive performance analysis."""
    analyzer = PerformanceAnalyzer()
    analyzer.analyze_all_datasets()


if __name__ == "__main__":
    main()