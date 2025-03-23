# TODO

## Now ...

🟥🟥🟥🟥🟥🟥 check that function calls use BrE

🟧🟧🟧🟧🟧🟧 CHECK WHAT THE CURRENT BRANCH IS

Current task:

-   utils: organise functions into their correct files (the main purpose of the function determines the file it belongs to)

    -   e.g. `format_timedelta()`'s main purpose is formatting (i.e. `formatting.py`), and does NOT belong in `time_utils.py`, even though it's working with time

-   organise tests into folders (`utils/test_formatting.py`)
-   update `tests/run_tests.py` so it accepts an argument to specify which folder to use

Requirements:

-   All code and comments must use British English spelling
-   KISS principle
-   Robust error handling and logging

## Next ...

-   write tests for each util file (start with `test_formatting.py` and make sure it has all of the correct functions)
-   check out fuzzywuzzy library for `parsing.py`

## Then ...

-   db: CRUD db queries for users table
-   db: CRUD db queries for other tables
-   SQLite db
    -   make it scale
    -   prevent duplicate records (old durability table went gnarly!)
    -   delete unused records (as per durability table)

---

## READY FOR USER TESTING

-   nothing just yet
