# Sorting Algorithms Performance Analysis

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Educational-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Complete-brightgreen.svg)]()

A comprehensive analysis and implementation of **Quicksort** and **Mergesort** algorithms with detailed performance tracking, theoretical analysis, and empirical comparisons across multiple dataset characteristics.

## 🚀 Quick Start

```bash
# Clone and setup
git clone <repository-url>
cd MSCS532_Assignment2

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run complete analysis
python main.py
```

## 📊 Performance Summary

| Algorithm | Best Case | Average Case | Worst Case | Space | Stability |
|-----------|-----------|--------------|------------|-------|-----------|
| **Quicksort** | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| **Mergesort** | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |

**Key Findings:**
- Quicksort: **1.6x faster** on average, but unpredictable worst-case
- Mergesort: **Consistent performance** across all inputs, stable sorting

## 📁 Project Structure

```
MSCS532_Assignment2/
├── 📄 main.py                    # Main orchestrator with comparison tables
├── 🔧 quicksort.py               # Quicksort implementation with tracking
├── 🔧 mergesort.py               # Mergesort implementation with tracking
├── 📊 performance_analysis.py    # Comprehensive analysis script
├── 📁 datasets/                  # Test datasets (multiple sizes & types)
│   ├── sorted_data_*.txt        # Pre-sorted ascending data
│   ├── reverse_sorted_data_*.txt # Reverse sorted data
│   └── random_data_*.txt        # Random data
├── 📋 requirements.txt           # Python dependencies
└── 📖 README.md                  # This file
```

## 🎯 Features

- ✅ **Comprehensive Implementations**: Detailed Quicksort and Mergesort with extensive comments
- ⏱️ **Performance Tracking**: Real-time execution time and memory usage monitoring
- 📈 **Multiple Dataset Types**: Sorted, reverse sorted, and random data across various sizes
- 🤖 **Automated Analysis**: Complete performance comparison with formatted output
- 📊 **Export Capabilities**: JSON export of detailed metrics for further analysis
- 📚 **Educational Focus**: Clear explanations of algorithms, complexity analysis, and trade-offs

## 🛠️ Requirements

- **Python**: 3.7 or higher
- **Dependencies**: `psutil` (memory monitoring), `tabulate` (formatted output)

## 🚀 Usage

### Complete Analysis (Recommended)
```bash
python main.py
```
Runs both algorithms on all datasets and displays comprehensive comparison tables.

### Individual Algorithm Testing
```bash
# Test Quicksort performance
python quicksort.py

# Test Mergesort performance
python mergesort.py

# Run detailed performance analysis
python performance_analysis.py
```

### Custom Dataset Testing
Create a text file with one integer per line and modify the dataset paths in the sorting scripts.

## 🔍 Algorithm Details

### Quicksort
**Strategy**: Divide-and-conquer with pivot-based partitioning
- **Best Case**: O(n log n) - balanced partitions
- **Average Case**: O(n log n) - random pivot selection
- **Worst Case**: O(n²) - unbalanced partitions
- **Space**: O(log n) - recursion stack
- **Characteristics**: In-place, unstable, cache-friendly

### Mergesort
**Strategy**: Divide-and-conquer with guaranteed balanced splits
- **All Cases**: O(n log n) - consistent performance
- **Space**: O(n) - temporary arrays
- **Characteristics**: Stable, predictable, external sorting capable

## 📊 Dataset Information

The project includes datasets of various sizes (1K, 5K, 10K elements) with three characteristics:

| Dataset Type | Purpose | Quicksort Performance | Mergesort Performance |
|--------------|---------|----------------------|----------------------|
| **Sorted** | Best-case test | Excellent (O(n log n)) | Consistent (O(n log n)) |
| **Reverse Sorted** | Worst-case test | Poor (O(n²)) | Consistent (O(n log n)) |
| **Random** | Average-case test | Good (O(n log n)) | Consistent (O(n log n)) |

## 📈 Sample Output

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

## 🔧 Troubleshooting

### Common Issues

**Virtual Environment Problems:**
```bash
# Command not found
python -m venv venv  # Use 'python' instead of 'python3'

# Permission denied
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

**Dependency Issues:**
```bash
# Upgrade pip first
pip install --upgrade pip
pip install psutil tabulate

# Alternative with conda
conda install psutil tabulate
```

**Dataset Issues:**
- Datasets are generated automatically when running scripts
- Check `datasets/` directory exists and contains `.txt` files
- Memory usage showing 0.00 MB is normal for small datasets

## 📚 Documentation

- **[Algorithm Analysis](assets/algorithm_analysis.md)**: Detailed theoretical analysis including recurrence relations, complexity proofs, and comparative analysis
- **[Performance Analysis](assets/performance_analysis.md)**: Empirical performance analysis with real-world implications and optimization strategies

## 🎓 Educational Context

This project is part of **MSCS-532 Assignment 2** and focuses on:
- **Algorithm Implementation**: Clear, commented code for educational purposes
- **Performance Analysis**: Theoretical vs. practical performance comparison
- **Real-world Applications**: Industry use cases and optimization strategies
- **Comprehensive Testing**: Multiple dataset types and sizes for thorough analysis

## 📄 License

This project is created for educational purposes as part of academic coursework.

---

**Note**: This analysis demonstrates that while Mergesort provides consistent performance guarantees, Quicksort often outperforms it in practice due to better cache locality and lower constant factors, especially with randomized pivot selection.