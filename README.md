# Sorting Algorithms Performance Analysis

This project implements and analyzes the performance of two fundamental sorting algorithms: **Quicksort** and **Mergesort**. The implementation includes comprehensive performance tracking, detailed comments, and analysis of theoretical vs. practical performance characteristics.

## Project Structure

```
assign2/
├── main.py                   # Main orchestrator - runs complete analysis with comparison tables
├── quicksort.py              # Quicksort implementation with performance tracking
├── mergesort.py              # Mergesort implementation with performance tracking
├── performance_analysis.py    # Comprehensive performance analysis script
├── datasets/                 # Directory containing test datasets
│   ├── sorted_data.txt      # Pre-sorted ascending data (10,000 elements)
│   ├── reverse_sorted_data.txt # Reverse sorted data (10,000 elements)
│   ├── random_data.txt      # Random data (10,000 elements)
│   └── [additional size variants] # Various sizes for comprehensive testing
├── README.md                 # This file
├── requirements.txt          # Python dependencies
└── .gitignore               # Git ignore rules
```

## Features

- **Detailed Algorithm Implementations**: Both Quicksort and Mergesort with comprehensive comments explaining the algorithms, time/space complexity, and implementation details
- **Performance Tracking**: Real-time monitoring of execution time and memory usage using `psutil` and `time` modules
- **Multiple Dataset Types**: Sorted, reverse sorted, and random data for comprehensive testing
- **Automated Analysis**: Scripts for generating datasets and running performance comparisons
- **Results Export**: JSON export of detailed performance metrics for further analysis

## Requirements

- Python 3.7+
- `psutil` library for memory monitoring

## Virtual Environment Setup (Recommended)

It's recommended to use a virtual environment to avoid conflicts with system packages:


# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install required dependencies
pip install -r requirements.txt
```

### Option 2: Using the Setup Script
```bash
# Make the setup script executable (macOS/Linux only)
chmod +x setup_venv.sh

# Run the setup script
./setup_venv.sh
```

### Deactivating Virtual Environment
```bash
deactivate
```

## Quick Start

**Note**: Make sure your virtual environment is activated before running the commands below.

### Option 1: Complete Analysis (Recommended)
```bash
# Run the main orchestrator for complete analysis with comparison tables
python main.py
```
This runs both algorithms on all datasets and displays comprehensive comparison tables in the terminal.

### Option 2: Individual Analysis
```bash
# Test Quicksort on all datasets
python quicksort.py

# Test Mergesort on all datasets  
python mergesort.py

# Run detailed performance analysis
python performance_analysis.py
```

## Algorithm Implementations

### Quicksort (`quicksort.py`)

**Algorithm Overview:**
- Divide-and-conquer algorithm
- Selects a pivot element and partitions the array
- Recursively sorts subarrays before and after the pivot

**Time Complexity:**
- Best Case: O(n log n) - when pivot divides array into equal halves
- Average Case: O(n log n) - expected performance with random data
- Worst Case: O(n²) - when pivot is always smallest/largest element

**Space Complexity:** O(log n) - due to recursive call stack

**Key Features:**
- In-place sorting (modifies input array)
- Unstable sorting algorithm
- Performance depends heavily on pivot selection

### Mergesort (`mergesort.py`)

**Algorithm Overview:**
- Divide-and-conquer algorithm
- Divides array into two halves, sorts each half, then merges
- Guaranteed stable performance regardless of input

**Time Complexity:**
- Best Case: O(n log n)
- Average Case: O(n log n)  
- Worst Case: O(n log n)

**Space Complexity:** O(n) - requires additional space for temporary arrays

**Key Features:**
- Stable sorting algorithm
- Consistent performance across all input types
- Requires additional memory for temporary arrays

## Performance Analysis

The `performance_analysis.py` script provides comprehensive analysis including:

- **Execution Time Comparison**: Direct timing comparison between algorithms
- **Memory Usage Analysis**: Memory consumption tracking during sorting
- **Dataset-Specific Analysis**: Performance across different data characteristics
- **Summary Reports**: Categorized analysis by data type (sorted, reverse sorted, random)
- **JSON Export**: Detailed results saved for further analysis

### Sample Output

```
PERFORMANCE SUMMARY REPORT
======================================================================

SORTED DATA ANALYSIS:
--------------------------------------------------

Dataset: sorted_data_10000 (Size: 10000)
  Quicksort:  0.002345s, 0.15MB
  Mergesort:  0.003456s, 0.23MB
  Winner: Quicksort (1.47x faster)

REVERSE SORTED DATA ANALYSIS:
--------------------------------------------------

Dataset: reverse_sorted_data_10000 (Size: 10000)
  Quicksort:  0.045678s, 0.18MB
  Mergesort:  0.003123s, 0.25MB
  Winner: Mergesort (14.63x faster)
```

## Dataset Information

### Generated Datasets

The project includes datasets of various sizes (1,000, 5,000, 10,000 elements) with three characteristics:

1. **Sorted Data**: Pre-sorted in ascending order
   - Tests best-case performance for Quicksort
   - Tests consistent performance for Mergesort

2. **Reverse Sorted Data**: Sorted in descending order  
   - Tests worst-case performance for Quicksort
   - Tests consistent performance for Mergesort

3. **Random Data**: Randomly generated integers
   - Tests average-case performance for both algorithms
   - Most realistic scenario for practical applications

## Expected Performance Characteristics

### Quicksort
- **Best Performance**: On sorted or nearly sorted data
- **Worst Performance**: On reverse sorted data (worst-case O(n²))
- **Memory Efficient**: Lower memory usage due to in-place sorting
- **Unpredictable**: Performance varies significantly with input characteristics

### Mergesort  
- **Consistent Performance**: Same O(n log n) performance regardless of input
- **Higher Memory Usage**: Requires O(n) additional space
- **Predictable**: Reliable performance makes it suitable for critical applications
- **Stable**: Maintains relative order of equal elements

## Files Description

- **`main.py`**: Main orchestrator that runs complete analysis with comparison tables
- **`quicksort.py`**: Complete Quicksort implementation with performance tracking
- **`mergesort.py`**: Complete Mergesort implementation with performance tracking  
- **`performance_analysis.py`**: Comprehensive analysis script comparing both algorithms
- **`performance_analysis.md`**: Detailed analysis of theoretical vs practical performance discrepancies
- **`requirements.txt`**: Python dependencies (psutil, tabulate)
- **`.gitignore`**: Git ignore rules for Python projects

## Usage Examples

### Running Individual Tests
```bash
# Test specific algorithm
python quicksort.py
python mergesort.py

# Generate new datasets with different parameters
python generate_datasets.py
```

### Custom Dataset Testing
To test with your own dataset, create a text file with one integer per line and modify the dataset paths in the sorting scripts.

### Performance Analysis
```bash
# Run comprehensive analysis
python performance_analysis.py

# Results will be displayed in terminal and saved to performance_results.json
```

## Troubleshooting

### Virtual Environment Issues

**Problem**: `python3` command not found
```bash
# Try using 'python' instead
python -m venv venv
```

**Problem**: Permission denied when activating virtual environment
```bash
# Make sure you're using the correct activation command
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

**Problem**: `psutil` installation fails
```bash
# Try upgrading pip first
pip install --upgrade pip
pip install psutil

# If still failing, try installing with conda
conda install psutil
```

**Problem**: Virtual environment not activating
```bash
# Check if virtual environment was created properly
ls -la venv/

# Recreate if necessary
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

### Performance Analysis Issues

**Problem**: Dataset files not found
```bash
# Make sure datasets directory exists and contains files
ls -la datasets/

# If empty, the datasets are generated automatically when running the scripts
```

**Problem**: Memory usage shows 0.00 MB
- This is normal for small datasets or when memory usage is below the measurement threshold
- The algorithms are working correctly; memory tracking has limitations for very small operations

## Contributing

This project is part of Assignment 2 for MSCS-532. The implementations focus on:
- Educational clarity with detailed comments
- Comprehensive performance analysis
- Real-world applicability considerations
- Theoretical vs practical performance analysis

## License

This project is created for educational purposes as part of academic coursework.