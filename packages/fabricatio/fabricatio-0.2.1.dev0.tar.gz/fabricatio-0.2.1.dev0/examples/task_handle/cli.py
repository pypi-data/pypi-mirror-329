#!/usr/bin/env python3
import argparse

def calculate_sum(n):
    """Calculate the sum of integers from 1 to n."""
    return n * (n + 1) // 2

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Calculate the sum of integers from 1 to n.")
    parser.add_argument('n', type=int, help="The upper limit integer")
    
    args = parser.parse_args()
    
    # Validate input
    if args.n < 1:
        print("Error: Input must be a positive integer.")
        return
    
    # Calculate and print the sum
    result = calculate_sum(args.n)
    print(f"The sum of integers from 1 to {args.n} is: {result}")

if __name__ == "__main__":
    main()