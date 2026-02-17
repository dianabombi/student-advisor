#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated test runner for University Chat System
Runs all tests and generates coverage report
"""

import subprocess
import sys
import os


def run_tests():
    """Run all university chat tests"""
    
    print("=" * 70)
    print("RUNNING UNIVERSITY CHAT TESTS")
    print("=" * 70)
    print()
    
    # Change to backend directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(backend_dir)
    
    # Test suites to run
    test_suites = [
        {
            "name": "Smoke Tests (Quick)",
            "path": "tests/test_university_chat_smoke.py",
            "marker": "smoke"
        },
        {
            "name": "Unit Tests",
            "path": "tests/test_university_chat_service.py",
            "marker": "unit"
        },
        {
            "name": "Integration Tests",
            "path": "tests/test_university_chat_integration.py",
            "marker": "integration"
        }
    ]
    
    all_passed = True
    results = []
    
    for suite in test_suites:
        print(f"\n{'=' * 70}")
        print(f"Running: {suite['name']}")
        print(f"{'=' * 70}\n")
        
        # Run pytest
        cmd = [
            sys.executable, "-m", "pytest",
            suite['path'],
            "-v",
            "--tb=short",
            "-m", suite['marker'] if suite.get('marker') else "",
            "--color=yes"
        ]
        
        # Remove empty marker if not specified
        if not suite.get('marker'):
            cmd = [c for c in cmd if c != "-m" and c != ""]
        
        result = subprocess.run(cmd, capture_output=False)
        
        if result.returncode == 0:
            results.append(f"[PASS] {suite['name']}: PASSED")
        else:
            results.append(f"[FAIL] {suite['name']}: FAILED")
            all_passed = False
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    for result in results:
        print(result)
    print("=" * 70)
    
    if all_passed:
        print("\n*** ALL TESTS PASSED! ***\n")
        return 0
    else:
        print("\n*** SOME TESTS FAILED ***\n")
        return 1


def run_coverage():
    """Run tests with coverage report"""
    
    print("\n" + "=" * 70)
    print("RUNNING TESTS WITH COVERAGE")
    print("=" * 70 + "\n")
    
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/test_university_chat*.py",
        "-v",
        "--cov=services.university_chat_service",
        "--cov-report=html",
        "--cov-report=term-missing",
        "--color=yes"
    ]
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\n[SUCCESS] Coverage report generated in htmlcov/index.html")
    
    return result.returncode


if __name__ == "__main__":
    # Check if coverage flag is provided
    if "--coverage" in sys.argv:
        exit_code = run_coverage()
    else:
        exit_code = run_tests()
    
    sys.exit(exit_code)
