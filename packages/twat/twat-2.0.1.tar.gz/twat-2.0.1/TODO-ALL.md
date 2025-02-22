# TODO for all `twat` repos

# `twat_fs`, `twat_cache` and `twat_hatch` have had the most work done. Do not make major changes to them. Instead, distill a "best" configuration for them, and apply it to the other packages.

## 1. Critical Issues

### 1.1. Package Import and Version Issues

* `twat_speech`: Fix missing `__version__` attribute
* `twat_text`: Fix missing `__version__` attribute
* `twat_llm`: Fix missing `__version__` attribute

### 1.2. Missing Dependencies

* `twat_genai`: Install missing `fal` package
* `twat_cache`: Install missing `pydantic` package
* `twat_image`: Install missing `numpy`,  `webcolors`,  `PIL` packages
* `twat_llm`: Install missing `cv2`,  `llm`,  `pathos`,  `PIL`,  `tenacity` packages

### 1.3. Type Annotation Issues

* All packages: Add return type annotations to test functions
* `twat_cache`: Fix multiple type annotation issues in engines
* `twat_ez`: Fix type annotations in `py_needs.py`
* `twat_genai`: Fix type annotations in async functions
* `twat_hatch`: Fix type annotations in CLI functions

## 2. High Priority Improvements

### 2.1. Code Quality

* `twat_cache`: 
  + Fix 39 linting errors
  + Address 344 type checking errors
  + Fix failing tests
* `twat_genai`:
  + Fix 43 linting errors
  + Address 29 type checking errors
  + Fix dependency issues
* `twat_hatch`:
  + Fix 27 linting errors
  + Address 5 type checking errors

### 2.2. Test Coverage

* `twat_mp`: Excellent test coverage, use as reference
* Most packages: Only have basic version test
* Add comprehensive test suites for:
  + `twat_cache`
  + `twat_genai`
  + `twat_fs`
  + `twat_image`
  + `twat_llm`

### 2.3. Documentation

* All packages: Add proper docstrings
* All packages: Create README.md with:
  + Installation instructions
  + Basic usage examples
  + API documentation
  + Development setup guide

## 3. Medium Priority Tasks

### 3.1. Code Structure

* `twat_task`: Fix property decorators

### 3.2. Security

* `twat_task`: Fix random number generation usage


## 4. Low Priority Enhancements

### 4.1. Developer Experience

* All packages: Add pre-commit hooks
* All packages: Standardize development tools

### 4.2. CI/CD

* All packages: Add GitHub Actions for:
  + Testing
  + Linting
  + Type checking
  + Documentation building
  + Package publishing

### 4.3. Monitoring & Logging

* All packages: Add structured logging
* All packages: Add error reporting

## 5. Package-Specific Notes

### 5.1. twat_cache

* Highest priority for fixes
* Major type system overhaul needed
* Test suite needs complete rewrite

### 5.2. twat_genai

* Second highest priority
* Focus on async code improvements
* Fix dependency management

### 5.3. twat_mp

* Use as reference implementation
* Well-tested with benchmarks
* Document performance patterns

### 5.4. twat_fs

* Core functionality package
* Needs better error handling
* Add upload progress tracking

### 5.5. twat_hatch

* Focus on CLI improvements
* Better subprocess handling
* Add project templates

### 5.6. twat_image

* Fix dependency chain
* Add image processing tests
* Improve error messages

### 5.7. twat_llm

* Complete dependency audit
* Add model validation
* Improve async handling

## 6. Action Plan

1. Week 1:
   - Fix all critical version issues
   - Resolve dependency problems
   - Add missing type annotations

2. Week 2:
   - Address major linting issues
   - Fix type checking errors
   - Get all tests passing

3. Week 3:
   - Improve test coverage
   - Add documentation
   - Fix security issues

4. Week 4:
   - Implement CI/CD
   - Add development tools
   - Performance optimizations

## 7. Metrics for Success

1. All packages should have:
   - Zero linting errors
   - Zero type checking errors
   - 80%+ test coverage
   - Complete documentation
   - Working CI/CD pipeline

2. Performance targets:
   - Cache hit time < 1ms
   - Image processing < 100ms
   - API response time < 200ms

3. Code quality metrics:
   - Cyclomatic complexity < 10
   - Method length < 50 lines
   - Class length < 300 lines
