## Tests for functions used in data analysis

### Running the tests
The test suite can be run from the project root directory via:

```
pytest tests/*
```

### Preparation of auto-generated test files for test_clean_confdence_intervals
The test data used in `test_clean_confdence_intervals` were genereated by running the `conftest.py` script in the `tests` directory.

## Dependencies:
Jupyter, Python and the following packages:
- pandas
- pytest