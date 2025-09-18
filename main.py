#!/usr/bin/env python3
"""
Main Orchestrator for Sorting Algorithms Performance Analysis

This is the main entry point that runs both Quicksort and Mergesort algorithms
on all available datasets, performs comprehensive performance analysis, and
displays detailed comparison tables in the terminal.

Author: Mausam Shrestha
Date: 2025
"""

import os
import sys
import glob
import time
from typing import List, Dict, Tuple
from tabulate import tabulate

# Import our sorting algorithms and performance analyzer
from quicksort import quicksort_wrapper
from mergesort import mergesort_wrapper


class SortingAlgorithmAnalyzer:
    """
    Main analyzer class that orchestrates the entire performance analysis.
    
    This class serves as the central coordinator for running comprehensive
    performance tests on both Quicksort and Mergesort algorithms across
    multiple datasets. It handles dataset discovery, performance tracking,
    result collection, and formatted output generation.
    
    Key Responsibilities:
    - Discover and load all available datasets
    - Run both algorithms on each dataset
    - Track execution time and memory usage
    - Generate comprehensive comparison tables
    - Provide detailed performance insights
    """
    
    def __init__(self):
        """Initialize the analyzer with empty results storage."""
        # Dictionary to store results for each dataset
        # Format: {'dataset_name': {'quicksort': {...}, 'mergesort': {...}}}
        self.results = {}
        
        # List to store discovered dataset file paths
        self.datasets = []
    
    def discover_datasets(self) -> List[str]:
        """
        Discover all available dataset files in the datasets directory.
        
        This method scans the 'datasets/' directory for all .txt files,
        which represent our test datasets. It provides user feedback about
        what datasets were found and handles the case where no datasets exist.
        
        Returns:
            List[str]: Sorted list of dataset file paths
        """
        # Use glob to find all .txt files in the datasets directory
        # This pattern matches any file ending with .txt
        dataset_files = glob.glob("datasets/*.txt")
        
        # Sort files alphabetically for consistent ordering
        dataset_files.sort()
        
        # Check if any datasets were found
        if not dataset_files:
            print("❌ No dataset files found in the 'datasets' directory.")
            print("   Please ensure datasets are generated first.")
            return []
        
        # Provide user feedback about discovered datasets
        print(f"📁 Found {len(dataset_files)} dataset files:")
        for file in dataset_files:
            print(f"   - {file}")
        
        return dataset_files
    
    def load_dataset(self, filename: str) -> List[int]:
        """
        Load dataset from a text file and convert to list of integers.
        
        This method reads a dataset file where each line contains a single
        integer value. It handles common file reading errors and data
        conversion issues gracefully.
        
        Args:
            filename (str): Path to the dataset file
            
        Returns:
            List[int]: List of integers from the dataset, empty list on error
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
            print(f"❌ Error: Dataset file '{filename}' not found.")
            return []
            
        except ValueError as e:
            # Handle case where file contains non-integer data
            print(f"❌ Error: Invalid data format in '{filename}': {e}")
            return []
    
    def analyze_single_dataset(self, dataset_path: str) -> Dict:
        """
        Analyze performance of both algorithms on a single dataset.
        
        This is the core analysis method that:
        1. Loads a dataset from file
        2. Runs both Quicksort and Mergesort on the same data
        3. Measures execution time and memory usage for each
        4. Verifies that sorting was performed correctly
        5. Compares performance between the two algorithms
        6. Returns comprehensive results for further analysis
        
        Args:
            dataset_path (str): Path to the dataset file to analyze
            
        Returns:
            Dict: Comprehensive results including timing, memory, and comparison data
        """
        # Extract dataset name from file path for display purposes
        dataset_name = os.path.basename(dataset_path).replace('.txt', '')
        
        # Display analysis header with visual separators
        print(f"\n🔍 Analyzing dataset: {dataset_name}")
        print("=" * 60)
        
        # Load dataset from file
        data = self.load_dataset(dataset_path)
        if not data:
            # Return empty dict if dataset loading failed
            return {}
        
        # Display dataset information
        dataset_size = len(data)
        print(f"📊 Dataset size: {dataset_size:,} elements")
        print(f"📋 First 10 elements: {data[:10]}")
        
        # Initialize result structure to store all performance metrics
        result = {
            'dataset_name': dataset_name,
            'dataset_size': dataset_size,
            'quicksort': {'success': False},  # Will be updated with actual results
            'mergesort': {'success': False}   # Will be updated with actual results
        }
        
        # Test Quicksort Algorithm
        print(f"\n⚡ Testing Quicksort...")
        try:
            # Call the quicksort wrapper which handles performance tracking
            # Returns: (sorted_array, execution_time, memory_usage)
            sorted_data_qs, exec_time_qs, memory_qs = quicksort_wrapper(data)
            
            # Store successful results in our result dictionary
            result['quicksort'] = {
                'execution_time': exec_time_qs,
                'memory_usage': memory_qs,
                'success': True
            }
            
            # Verify that the sorting was performed correctly
            # Check that each element is <= the next element (ascending order)
            is_sorted = all(sorted_data_qs[i] <= sorted_data_qs[i+1] for i in range(len(sorted_data_qs)-1))
            
            # Display performance results with formatting
            print(f"   ✅ Completed in {exec_time_qs:.6f} seconds")
            print(f"   💾 Memory usage: {memory_qs*1024:.2f} KB")
            print(f"   ✓ Sorting verification: {'PASSED' if is_sorted else 'FAILED'}")
            
        except Exception as e:
            # Handle any errors that occur during quicksort execution
            print(f"   ❌ Quicksort failed: {e}")
            result['quicksort'] = {
                'execution_time': None,
                'memory_usage': None,
                'success': False,
                'error': str(e)
            }
        
        # Test Mergesort Algorithm
        print(f"\n🔄 Testing Mergesort...")
        try:
            # Call the mergesort wrapper which handles performance tracking
            # Returns: (sorted_array, execution_time, memory_usage)
            sorted_data_ms, exec_time_ms, memory_ms = mergesort_wrapper(data)
            
            # Store successful results in our result dictionary
            result['mergesort'] = {
                'execution_time': exec_time_ms,
                'memory_usage': memory_ms,
                'success': True
            }
            
            # Verify that the sorting was performed correctly
            # Check that each element is <= the next element (ascending order)
            is_sorted = all(sorted_data_ms[i] <= sorted_data_ms[i+1] for i in range(len(sorted_data_ms)-1))
            
            # Display performance results with formatting
            print(f"   ✅ Completed in {exec_time_ms:.6f} seconds")
            print(f"   💾 Memory usage: {memory_ms*1024:.2f} KB")
            print(f"   ✓ Sorting verification: {'PASSED' if is_sorted else 'FAILED'}")
            
        except Exception as e:
            # Handle any errors that occur during mergesort execution
            print(f"   ❌ Mergesort failed: {e}")
            result['mergesort'] = {
                'execution_time': None,
                'memory_usage': None,
                'success': False,
                'error': str(e)
            }
        
        # Compare Performance Between Algorithms
        if result['quicksort']['success'] and result['mergesort']['success']:
            print(f"\n📈 Performance Comparison:")
            print("-" * 40)
            
            # Extract performance metrics for comparison
            qs_time = result['quicksort']['execution_time']
            ms_time = result['mergesort']['execution_time']
            qs_mem = result['quicksort']['memory_usage']
            ms_mem = result['mergesort']['memory_usage']
            
            # Calculate differences (positive = quicksort uses more)
            time_diff = qs_time - ms_time
            memory_diff = qs_mem - ms_mem
            
            # Determine which algorithm was faster
            faster_algorithm = "Quicksort" if time_diff < 0 else "Mergesort"
            time_advantage = abs(time_diff)
            
            # Display comparison results
            print(f"🏆 Faster algorithm: {faster_algorithm}")
            print(f"⏱️  Time difference: {time_diff:.6f} seconds")
            print(f"💾 Memory difference: {memory_diff*1024:.2f} KB")
            
            # Calculate and display speedup ratio (avoid division by zero)
            if ms_time > 0:
                speedup = qs_time / ms_time
                print(f"📊 Speedup ratio (QS/MS): {speedup:.2f}x")
        
        return result
    
    def generate_all_datasets_table(self) -> None:
        """Generate a comprehensive table showing all datasets."""
        print(f"\n📋 ALL DATASETS COMPARISON")
        print("=" * 50)
        
        # Prepare comprehensive table data
        table_data = []
        headers = ["Dataset", "Size", "QS Time (s)", "MS Time (s)", 
                  "QS Memory (KB)", "MS Memory (KB)", "Time Diff (s)", "Mem Diff (KB)", "Winner", "Speedup"]
        
        # Sort results by dataset name for consistent display
        sorted_results = sorted(self.results.items(), key=lambda x: x[0])
        
        for dataset_name, result in sorted_results:
            size = result['dataset_size']
            
            if result['quicksort']['success'] and result['mergesort']['success']:
                qs_time = result['quicksort']['execution_time']
                ms_time = result['mergesort']['execution_time']
                qs_mem = result['quicksort']['memory_usage']
                ms_mem = result['mergesort']['memory_usage']
                
                winner = "Quicksort" if qs_time < ms_time else "Mergesort"
                speedup = max(qs_time, ms_time) / min(qs_time, ms_time)
                
                table_data.append([
                    dataset_name,
                    f"{size:,}",
                    f"{qs_time:.6f}",
                    f"{ms_time:.6f}",
                    f"{qs_mem*1024:.2f}",
                    f"{ms_mem*1024:.2f}",
                    f"{qs_time-ms_time:.6f}",
                    f"{(qs_mem-ms_mem)*1024:.2f}",
                    winner,
                    f"{speedup:.2f}x"
                ])
            else:
                table_data.append([
                    dataset_name,
                    f"{size:,}",
                    "FAILED" if not result['quicksort']['success'] else f"{result['quicksort']['execution_time']:.6f}",
                    "FAILED" if not result['mergesort']['success'] else f"{result['mergesort']['execution_time']:.6f}",
                    "N/A",
                    "N/A",
                    "N/A",
                    "N/A",
                    "N/A",
                    "N/A"
                ])
        
        # Display comprehensive table
        print(tabulate(table_data, headers=headers, tablefmt="grid", stralign="center"))
    
    def generate_comparison_table(self) -> None:
        """Generate and display comprehensive comparison tables."""
        if not self.results:
            print("❌ No results to display.")
            return
        
        print(f"\n{'='*80}")
        print("📊 COMPREHENSIVE PERFORMANCE COMPARISON TABLES")
        print(f"{'='*80}")
        
        # First, show all datasets in one comprehensive table
        self.generate_all_datasets_table()
        
        # Group results by dataset type
        sorted_results = []
        reverse_results = []
        random_results = []
        
        for dataset_name, data in self.results.items():
            if 'sorted' in dataset_name and 'reverse' not in dataset_name:
                sorted_results.append(data)
            elif 'reverse' in dataset_name:
                reverse_results.append(data)
            elif 'random' in dataset_name:
                random_results.append(data)
        
        # Create tables for each category
        categories = [
            ("🔼 SORTED DATA ANALYSIS", sorted_results),
            ("🔽 REVERSE SORTED DATA ANALYSIS", reverse_results),
            ("🎲 RANDOM DATA ANALYSIS", random_results)
        ]
        
        for category_name, category_results in categories:
            if not category_results:
                continue
            
            print(f"\n{category_name}")
            print("=" * len(category_name))
            
            # Prepare table data
            table_data = []
            headers = ["Dataset", "Size", "QS Time (s)", "MS Time (s)", 
                      "QS Memory (KB)", "MS Memory (KB)", "Time Diff (s)", "Mem Diff (KB)", "Winner", "Speedup"]
            
            for result in category_results:
                dataset_name = result['dataset_name']
                size = result['dataset_size']
                
                if result['quicksort']['success'] and result['mergesort']['success']:
                    qs_time = result['quicksort']['execution_time']
                    ms_time = result['mergesort']['execution_time']
                    qs_mem = result['quicksort']['memory_usage']
                    ms_mem = result['mergesort']['memory_usage']
                    
                    winner = "Quicksort" if qs_time < ms_time else "Mergesort"
                    speedup = max(qs_time, ms_time) / min(qs_time, ms_time)
                    
                    table_data.append([
                        dataset_name,
                        f"{size:,}",
                        f"{qs_time:.6f}",
                        f"{ms_time:.6f}",
                        f"{qs_mem*1024:.2f}",
                        f"{ms_mem*1024:.2f}",
                        f"{qs_time-ms_time:.6f}",
                        f"{(qs_mem-ms_mem)*1024:.2f}",
                        winner,
                        f"{speedup:.2f}x"
                    ])
                else:
                    table_data.append([
                        dataset_name,
                        f"{size:,}",
                        "FAILED" if not result['quicksort']['success'] else f"{result['quicksort']['execution_time']:.6f}",
                        "FAILED" if not result['mergesort']['success'] else f"{result['mergesort']['execution_time']:.6f}",
                        "N/A",
                        "N/A",
                        "N/A",
                        "N/A",
                        "N/A",
                        "N/A"
                    ])
            
            # Display table
            print(tabulate(table_data, headers=headers, tablefmt="grid", stralign="center"))
        
        # Overall summary table
        self.generate_summary_table()
    
    def generate_summary_table(self) -> None:
        """Generate overall summary statistics."""
        print(f"\n{'='*80}")
        print("📈 OVERALL PERFORMANCE SUMMARY")
        print(f"{'='*80}")
        
        successful_results = [r for r in self.results.values() 
                            if r['quicksort']['success'] and r['mergesort']['success']]
        
        if not successful_results:
            print("❌ No successful comparisons available.")
            return
        
        # Calculate statistics
        qs_times = [r['quicksort']['execution_time'] for r in successful_results]
        ms_times = [r['mergesort']['execution_time'] for r in successful_results]
        qs_memories = [r['quicksort']['memory_usage'] for r in successful_results]
        ms_memories = [r['mergesort']['memory_usage'] for r in successful_results]
        
        # Calculate averages
        avg_qs_time = sum(qs_times) / len(qs_times)
        avg_ms_time = sum(ms_times) / len(ms_times)
        avg_qs_memory = sum(qs_memories) / len(qs_memories)
        avg_ms_memory = sum(ms_memories) / len(ms_memories)
        
        # Count wins
        qs_wins = sum(1 for r in successful_results 
                     if r['quicksort']['execution_time'] < r['mergesort']['execution_time'])
        ms_wins = len(successful_results) - qs_wins
        
        # Summary table
        summary_data = [
            ["Metric", "Quicksort", "Mergesort", "Winner"],
            ["Average Time (s)", f"{avg_qs_time:.6f}", f"{avg_ms_time:.6f}", 
             "Quicksort" if avg_qs_time < avg_ms_time else "Mergesort"],
            ["Average Memory (KB)", f"{avg_qs_memory*1024:.2f}", f"{avg_ms_memory*1024:.2f}", 
             "Quicksort" if avg_qs_memory < avg_ms_memory else "Mergesort"],
            ["Wins", f"{qs_wins}", f"{ms_wins}", 
             "Quicksort" if qs_wins > ms_wins else "Mergesort"],
            ["Win Rate", f"{(qs_wins/len(successful_results)*100):.1f}%", 
             f"{(ms_wins/len(successful_results)*100):.1f}%", 
             "Quicksort" if qs_wins > ms_wins else "Mergesort"]
        ]
        
        print(tabulate(summary_data, headers="firstrow", tablefmt="grid", stralign="center"))
        
        # Performance insights
        print(f"\n💡 KEY INSIGHTS:")
        print("-" * 50)
        
        if avg_qs_time < avg_ms_time:
            time_advantage = (avg_ms_time - avg_qs_time) / avg_ms_time * 100
            print(f"⚡ Quicksort is {time_advantage:.1f}% faster on average")
        else:
            time_advantage = (avg_qs_time - avg_ms_time) / avg_qs_time * 100
            print(f"⚡ Mergesort is {time_advantage:.1f}% faster on average")
        
        if avg_qs_memory < avg_ms_memory:
            memory_advantage = (avg_ms_memory - avg_qs_memory) / avg_ms_memory * 100
            print(f"💾 Quicksort uses {memory_advantage:.1f}% less memory on average")
        else:
            memory_advantage = (avg_qs_memory - avg_ms_memory) / avg_qs_memory * 100
            print(f"💾 Mergesort uses {memory_advantage:.1f}% less memory on average")
        
        print(f"🏆 Quicksort wins: {qs_wins}/{len(successful_results)} comparisons")
        print(f"🏆 Mergesort wins: {ms_wins}/{len(successful_results)} comparisons")
    
    def run_complete_analysis(self) -> None:
        """
        Run the complete performance analysis workflow.
        
        This method orchestrates the entire analysis process:
        1. Discovers all available datasets
        2. Runs both algorithms on each dataset
        3. Collects and stores all performance results
        4. Generates comprehensive comparison tables
        5. Provides summary statistics and insights
        """
        # Display analysis header and description
        print("🚀 Sorting Algorithms Performance Analysis")
        print("=" * 60)
        print("This analysis will test both Quicksort and Mergesort algorithms")
        print("on all available datasets and provide comprehensive comparisons.")
        print()
        
        # Step 1: Discover all available datasets
        dataset_files = self.discover_datasets()
        if not dataset_files:
            # Exit early if no datasets are found
            return
        
        # Step 2: Start timing the entire analysis process
        print(f"\n⏳ Starting analysis of {len(dataset_files)} datasets...")
        start_time = time.time()
        
        # Step 3: Analyze each dataset individually
        for i, dataset_file in enumerate(dataset_files, 1):
            print(f"\n📊 Progress: {i}/{len(dataset_files)} datasets analyzed")
            
            # Analyze the current dataset
            result = self.analyze_single_dataset(dataset_file)
            
            # Store results if analysis was successful
            if result:
                self.results[result['dataset_name']] = result
        
        # Step 4: Calculate total analysis time
        total_time = time.time() - start_time
        
        # Step 5: Display completion summary
        print(f"\n✅ Analysis completed in {total_time:.2f} seconds!")
        print(f"📊 Successfully analyzed {len(self.results)} datasets")
        
        # Step 6: Generate comprehensive comparison tables
        self.generate_comparison_table()
        
        # Step 7: Final completion message
        print(f"\n🎉 Analysis complete! Check the tables above for detailed results.")


def main():
    """Main entry point."""
    try:
        analyzer = SortingAlgorithmAnalyzer()
        analyzer.run_complete_analysis()
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Analysis interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()