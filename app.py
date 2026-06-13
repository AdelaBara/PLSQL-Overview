from __future__ import annotations

import json
import random
import re
from pathlib import Path

import streamlit as st


BASE_DIR = Path(__file__).parent
EXAMPLES_FILE = BASE_DIR / "exemple.json"
AUTHOR_NAME = "Adela Bara"
AUTHOR_CONTACT = "bara.adela@ie.ase.ro"


LESSONS = [
    {
        "file": "Les01.ppt",
        "title": "Introduction to PL/SQL",
        "focus": "Why PL/SQL exists, how a block is structured, and how anonymous blocks run.",
        "definitions": [
            ("PL/SQL", "Oracle's procedural extension to SQL. SQL is excellent for describing what data you want, while PL/SQL adds programming logic: variables, IF statements, loops, error handling, and reusable routines. This is useful when database work needs decisions or repeated actions close to the data."),
            ("PL/SQL engine", "The component that executes procedural PL/SQL statements. When a block contains SQL, the PL/SQL engine sends those SQL statements to the SQL statement executor. This cooperation is why PL/SQL can combine application logic and database access efficiently."),
            ("PL/SQL block", "A logical unit of code with an optional declarative part, a mandatory executable part, and an optional exception part. Blocks make code easier to read, test, and maintain because related declarations, actions, and error handling stay together."),
            ("Anonymous block", "A PL/SQL block that is not stored in the database and is compiled/executed each time it is submitted. It is useful for testing, scripts, one-time data operations, and calling stored procedures."),
            ("Stored subprogram", "A named PL/SQL block, such as a procedure or function, saved in the database. It can be reused by many applications and can improve consistency because business rules are implemented in one place."),
            ("DBMS_OUTPUT", "A built-in Oracle package commonly used in beginner PL/SQL examples to print messages. It is useful for learning and debugging, but it is not a substitute for proper application logging in production systems."),
        ],
        "syntax": [
            ("Basic block", "[DECLARE\n  -- variables, cursors, exceptions\nBEGIN\n  -- SQL and PL/SQL statements\nEXCEPTION\n  -- error handlers\nEND;\n/"),
            ("Output", "SET SERVEROUTPUT ON\nBEGIN\n  DBMS_OUTPUT.PUT_LINE('Hello from PL/SQL');\nEND;\n/"),
        ],
        "examples": [
            {
                "title": "Anonymous block from the slides",
                "text": "A minimal anonymous block uses the mandatory executable section.",
                "code": "BEGIN\n  DBMS_OUTPUT.PUT_LINE('Welcome to PL/SQL');\nEND;\n/",
            },
            {
                "title": "PL/SQL block pattern",
                "text": "The slides show PL/SQL as a block that can combine procedural statements and SQL statements.",
                "code": "DECLARE\n  -- variables, cursors, user-defined exceptions\nBEGIN\n  -- SQL statements\n  -- PL/SQL statements\nEXCEPTION\n  -- actions to perform when errors occur\nEND;\n/",
            },
        ],
        "checklist": ["Identify the declarative, executable, and exception sections.", "Explain the difference between anonymous blocks, procedures, and functions.", "Use DBMS_OUTPUT.PUT_LINE for simple output."],
    },
    {
        "file": "Les02.ppt",
        "title": "Declaring PL/SQL Variables",
        "focus": "Identifiers, scalar types, %TYPE, bind variables, and substitution variables.",
        "definitions": [
            ("Identifier", "The name of a PL/SQL object such as a variable, constant, cursor, procedure, function, package, or exception. Good identifiers make code easier to understand; poor names are a common source of confusion in exam exercises and real programs."),
            ("Variable", "A named memory location whose value can change during block execution. Variables are used to hold query results, intermediate calculations, flags, and values passed between statements."),
            ("Constant", "A named value that is initialized once and cannot be changed. Constants make code clearer when a fixed business value, limit, or conversion factor is used in several places."),
            ("Scalar data type", "A data type that stores a single value, such as NUMBER, VARCHAR2, DATE, BOOLEAN, BINARY_FLOAT, or BINARY_DOUBLE. Scalar variables are the basic building blocks for PL/SQL calculations and decisions."),
            ("%TYPE", "An attribute that declares a variable with the same data type as a table column or another variable. It reduces maintenance: if the database column changes from NUMBER(6) to NUMBER(8), the PL/SQL variable automatically follows that type."),
            ("Bind variable", "A host variable created outside the PL/SQL block and referenced inside the block with a preceding colon. Bind variables can receive values from PL/SQL and can still be accessed after the block finishes."),
            ("Substitution variable", "A SQL*Plus or iSQL*Plus placeholder such as `&empno` that is replaced before the PL/SQL block is sent to Oracle. Unlike bind variables, substitution variables perform text replacement, so they are not PL/SQL variables at runtime."),
            ("NOT NULL variable", "A variable that must always contain a value. It must be initialized when declared, because PL/SQL cannot allow it to start as NULL."),
        ],
        "syntax": [
            ("Variables", "DECLARE\n  employee_id NUMBER(6);\n  last_name   VARCHAR2(25) := 'King';\n  active      BOOLEAN := TRUE;\nBEGIN\n  NULL;\nEND;\n/"),
            ("%TYPE", "DECLARE\n  emp_salary employees.salary%TYPE;\nBEGIN\n  SELECT salary INTO emp_salary\n  FROM employees\n  WHERE employee_id = 100;\nEND;\n/"),
            ("Bind variable", "VARIABLE emp_salary NUMBER\nBEGIN\n  SELECT salary INTO :emp_salary\n  FROM employees\n  WHERE employee_id = 178;\nEND;\n/\nPRINT emp_salary"),
        ],
        "examples": [
            {
                "title": "Bind variable example from the slides",
                "text": "The value selected inside PL/SQL remains available after the block finishes.",
                "code": "VARIABLE emp_salary NUMBER\nBEGIN\n  SELECT salary\n  INTO :emp_salary\n  FROM employees\n  WHERE employee_id = 178;\nEND;\n/\nPRINT emp_salary\n\nSELECT first_name, last_name\nFROM employees\nWHERE salary = :emp_salary;",
            },
            {
                "title": "Prompting with a substitution variable",
                "text": "The slides use `ACCEPT` and `&empno` to ask for the employee number before execution.",
                "code": "SET VERIFY OFF\nVARIABLE emp_salary NUMBER\nACCEPT empno PROMPT 'Please enter a valid employee number: '\nSET AUTOPRINT ON\nDECLARE\n  empno NUMBER(6) := &empno;\nBEGIN\n  SELECT salary\n  INTO :emp_salary\n  FROM employees\n  WHERE employee_id = empno;\nEND;\n/",
            },
        ],
        "checklist": ["Choose meaningful variable names.", "Initialize variables when a known starting value is needed.", "Prefer `%TYPE` for table-related variables.", "Distinguish bind variables from local PL/SQL variables."],
    },
    {
        "file": "Les03.ppt",
        "title": "Writing Executable Statements",
        "focus": "Lexical units, comments, SQL functions, conversions, nested blocks, and scope.",
        "definitions": [
            ("Lexical unit", "A building block of PL/SQL source code: identifiers, delimiters, literals, comments, or reserved words. Understanding lexical units helps students read syntax errors because Oracle often reports problems near these basic pieces."),
            ("Literal", "A fixed value written directly in code, such as `'Sales'`, `100`, or `DATE '2026-05-18'`. Literals are useful in examples, but production code often uses variables or parameters for flexibility."),
            ("Comment", "Text ignored by the PL/SQL compiler. Comments should explain intent, assumptions, or business rules, not repeat obvious code."),
            ("Implicit conversion", "A data type conversion Oracle performs automatically. It can be convenient, but it can also make code depend on session settings such as date format, so exam answers usually prefer explicit conversions when formats matter."),
            ("Explicit conversion", "A conversion requested by the programmer with functions such as `TO_CHAR`, `TO_DATE`, or `TO_NUMBER`. Explicit conversion makes code clearer and safer because the expected format is visible."),
            ("Nested block", "A block placed inside the executable or exception section of another block. Nested blocks are used to group related logic, limit variable visibility, or handle a local error without stopping the outer block."),
            ("Scope", "The region of code where an identifier can be referenced. Inner blocks can see outer variables, but if an inner variable has the same name, it hides the outer one unless a label is used."),
            ("Qualified identifier", "A name prefixed by a block label or object name to remove ambiguity, such as `outer_block.deptno`. This is useful when nested blocks contain variables with the same name."),
        ],
        "syntax": [
            ("Comments", "-- single-line comment\n/* multi-line\n   comment */"),
            ("Explicit conversion", "date_of_joining DATE := TO_DATE('February 02, 2000', 'Month DD, YYYY');"),
            ("Qualified identifier", "<<outer_block>>\nDECLARE\n  deptno NUMBER := 10;\nBEGIN\n  DECLARE\n    deptno NUMBER := 20;\n  BEGIN\n    DBMS_OUTPUT.PUT_LINE(outer_block.deptno);\n  END;\nEND;\n/"),
        ],
        "examples": [
            {
                "title": "Explicit date conversion from the slides",
                "text": "Use `TO_DATE` when the string format is not safely handled by implicit conversion.",
                "code": "date_of_joining DATE := TO_DATE('February 02, 2000', 'Month DD, YYYY');",
            },
            {
                "title": "Nested block and scope example",
                "text": "The lesson shows nested blocks and variable scope when selecting department data.",
                "code": "DECLARE\n  deptno      NUMBER(4);\n  location_id NUMBER(4);\nBEGIN\n  SELECT department_id, location_id\n  INTO deptno, location_id\n  FROM departments\n  WHERE department_name = 'Sales';\n\n  -- nested blocks can be placed here for related logic\nEND;\n/",
            },
        ],
        "checklist": ["Use comments to clarify intent.", "Perform explicit conversions when date or number formats matter.", "Know which variable is visible in nested blocks.", "Indent nested code consistently."],
    },
    {
        "file": "Les04.ppt",
        "title": "Interacting with the Oracle Server",
        "focus": "SELECT INTO, DML, transactions, and implicit cursor attributes.",
        "definitions": [
            ("SELECT INTO", "The PL/SQL form of SELECT that retrieves column values into variables or records. It must return exactly one row; no rows raises `NO_DATA_FOUND`, and more than one row raises `TOO_MANY_ROWS`. For multiple rows, use a cursor."),
            ("DML", "Data manipulation statements: INSERT, UPDATE, DELETE, and MERGE. In PL/SQL they are written almost the same as in SQL, but they can use local variables and can be followed by cursor attributes such as `SQL%ROWCOUNT`."),
            ("Transaction", "A logical unit of work made of one or more DML statements. `COMMIT` makes changes permanent, `ROLLBACK` cancels uncommitted changes, and `SAVEPOINT` marks a partial rollback location."),
            ("Implicit cursor", "A cursor automatically created by Oracle for DML and single-row SELECT statements. The programmer does not declare it, but can inspect its result using `SQL%FOUND`, `SQL%NOTFOUND`, `SQL%ROWCOUNT`, and `SQL%ISOPEN`."),
            ("Cursor attribute", "A property that reports the outcome of the most recent SQL operation. For example, `SQL%ROWCOUNT` tells how many rows were affected by an UPDATE or DELETE."),
            ("MERGE", "A DML statement that inserts or updates rows depending on whether matching rows already exist. It is often described as an 'upsert' operation."),
            ("Naming conflict", "A situation where a PL/SQL variable has the same name as a database column. This can produce confusing WHERE clauses, so variables should use a clear naming convention such as `v_employee_id`."),
        ],
        "syntax": [
            ("SELECT INTO", "SELECT select_list\nINTO variable_name [, variable_name]...\nFROM table\nWHERE condition;"),
            ("DML in PL/SQL", "BEGIN\n  UPDATE employees\n  SET salary = salary + 800\n  WHERE job_id = 'ST_CLERK';\nEND;\n/"),
            ("Cursor attributes", "IF SQL%FOUND THEN\n  DBMS_OUTPUT.PUT_LINE(SQL%ROWCOUNT || ' row(s) affected');\nEND IF;"),
        ],
        "examples": [
            {
                "title": "SELECT INTO example from the slides",
                "text": "A PL/SQL `SELECT` stores values in variables with `INTO`.",
                "code": "SET SERVEROUTPUT ON\nDECLARE\n  fname VARCHAR2(25);\nBEGIN\n  SELECT first_name\n  INTO fname\n  FROM employees\n  WHERE employee_id = 200;\n\n  DBMS_OUTPUT.PUT_LINE('First Name is : ' || fname);\nEND;\n/",
            },
            {
                "title": "INSERT example from the slides",
                "text": "The lesson inserts employee Ruth Cores using a sequence and `SYSDATE`.",
                "code": "BEGIN\n  INSERT INTO employees\n    (employee_id, first_name, last_name, email, hire_date, job_id, salary)\n  VALUES\n    (employees_seq.NEXTVAL, 'Ruth', 'Cores', 'RCORES', SYSDATE, 'AD_ASST', 4000);\nEND;\n/",
            },
            {
                "title": "DELETE with SQL cursor attribute",
                "text": "The slides print how many rows were deleted using `SQL%ROWCOUNT`.",
                "code": "VARIABLE rows_deleted VARCHAR2(30)\nDECLARE\n  empno employees.employee_id%TYPE := 176;\nBEGIN\n  DELETE FROM employees\n  WHERE employee_id = empno;\n\n  :rows_deleted := SQL%ROWCOUNT || ' row deleted.';\nEND;\n/\nPRINT rows_deleted",
            },
        ],
        "checklist": ["Every PL/SQL SELECT must have INTO.", "Expect exactly one row for plain SELECT INTO.", "Use `SQL%ROWCOUNT`, `SQL%FOUND`, and `SQL%NOTFOUND` after DML.", "Avoid using variable names identical to column names."],
    },
    {
        "file": "Les05.ppt",
        "title": "Writing Control Structures",
        "focus": "IF, CASE, LOOP, WHILE, FOR, labels, and null-aware conditions.",
        "definitions": [
            ("Selection", "Choosing which statements run with IF or CASE. Selection structures let PL/SQL implement business rules such as different actions for different departments, salaries, or error states."),
            ("IF statement", "A control structure that runs statements only when a Boolean condition is TRUE. `ELSIF` tests additional conditions, and `ELSE` handles the default case."),
            ("CASE expression", "An expression that chooses and returns a value. It is used inside assignments or SQL-like expressions when the result itself is needed."),
            ("CASE statement", "A control structure that chooses and executes statements. It is used when different branches perform different actions, not just return different values."),
            ("Iteration", "Repeating statements with LOOP, WHILE LOOP, or FOR LOOP. Iteration is essential when processing several values, retrying logic, or applying a rule multiple times."),
            ("Basic LOOP", "A loop that repeats until an explicit `EXIT` or `EXIT WHEN` is reached. It is flexible but must contain a clear exit condition to avoid an infinite loop."),
            ("WHILE LOOP", "A loop that continues while its condition is TRUE. The condition is checked before each iteration, so the loop body may execute zero times."),
            ("FOR LOOP", "A loop with an integer counter and a known range. PL/SQL creates the counter automatically, and the loop bounds are evaluated once at the start."),
            ("NULL condition", "A Boolean condition that evaluates to NULL is not TRUE, so IF does not enter that branch. This matters because comparisons with NULL do not behave like comparisons with normal values; use `IS NULL` and `IS NOT NULL`."),
            ("Loop label", "A name attached to a loop, useful in nested loops when `EXIT` or `CONTINUE` must refer to a specific outer loop."),
        ],
        "syntax": [
            ("IF", "IF condition THEN\n  statements;\nELSIF other_condition THEN\n  statements;\nELSE\n  statements;\nEND IF;"),
            ("CASE statement", "CASE selector\n  WHEN expression1 THEN statements;\n  WHEN expression2 THEN statements;\n  ELSE statements;\nEND CASE;"),
            ("Loops", "LOOP\n  statements;\n  EXIT WHEN condition;\nEND LOOP;\n\nWHILE condition LOOP\n  statements;\nEND LOOP;\n\nFOR i IN 1..3 LOOP\n  statements;\nEND LOOP;"),
        ],
        "examples": [
            {
                "title": "Basic LOOP example from the slides",
                "text": "This inserts three Montreal locations and exits when the counter passes 3.",
                "code": "DECLARE\n  countryid locations.country_id%TYPE := 'CA';\n  loc_id    locations.location_id%TYPE;\n  counter   NUMBER(2) := 1;\n  new_city  locations.city%TYPE := 'Montreal';\nBEGIN\n  SELECT MAX(location_id)\n  INTO loc_id\n  FROM locations\n  WHERE country_id = countryid;\n\n  LOOP\n    INSERT INTO locations(location_id, city, country_id)\n    VALUES ((loc_id + counter), new_city, countryid);\n\n    counter := counter + 1;\n    EXIT WHEN counter > 3;\n  END LOOP;\nEND;\n/",
            },
            {
                "title": "FOR LOOP variant from the slides",
                "text": "When the number of iterations is known, the `FOR` loop is shorter.",
                "code": "DECLARE\n  countryid locations.country_id%TYPE := 'CA';\n  loc_id    locations.location_id%TYPE;\n  new_city  locations.city%TYPE := 'Montreal';\nBEGIN\n  SELECT MAX(location_id)\n  INTO loc_id\n  FROM locations\n  WHERE country_id = countryid;\n\n  FOR i IN 1..3 LOOP\n    INSERT INTO locations(location_id, city, country_id)\n    VALUES ((loc_id + i), new_city, countryid);\n  END LOOP;\nEND;\n/",
            },
        ],
        "checklist": ["Use IF for Boolean decisions.", "Use CASE when comparing one selector against many values.", "Use FOR LOOP when the number of iterations is known.", "Always make basic LOOP termination obvious."],
    },
    {
        "file": "Les06.ppt",
        "title": "Composite Data Types",
        "focus": "Records, %ROWTYPE, associative arrays, table methods, and tables of records.",
        "definitions": [
            ("Composite data type", "A data type that can store multiple values in one variable. PL/SQL records and collections reduce long lists of separate variables and help model rows or groups of related values."),
            ("Record", "A composite variable made of fields, similar to one row of related values. Each field can have a different data type, so records are good for representing employee, department, or cursor rows."),
            ("%ROWTYPE", "An attribute that declares a record with the same structure as a table row or cursor row. It is especially useful with `SELECT * INTO` because the record automatically matches the source row structure."),
            ("Associative array", "A PL/SQL collection of key-value pairs, also called an INDEX BY table. It exists only in memory during program execution and is useful for temporary lookup lists or batches of rows."),
            ("INDEX BY table", "An associative array indexed by values such as PLS_INTEGER. Unlike database tables, associative arrays are not stored in the database and do not need consecutive indexes."),
            ("Collection method", "A built-in operation on collections, such as `EXISTS`, `COUNT`, `FIRST`, `LAST`, `PRIOR`, `NEXT`, and `DELETE`. These methods help safely navigate sparse collections."),
            ("Table of records", "A collection where each element is a record. This is useful when a program needs to temporarily hold multiple rows with several columns each."),
            ("Nested table", "A collection type that can be stored in the database or used in PL/SQL. Compared with associative arrays, nested tables are more database-oriented and can be manipulated with SQL in some contexts."),
        ],
        "syntax": [
            ("Custom record", "TYPE emp_record_type IS RECORD (\n  emp_id employees.employee_id%TYPE,\n  name   employees.last_name%TYPE\n);\nemp_rec emp_record_type;"),
            ("%ROWTYPE", "DECLARE\n  emp_rec employees%ROWTYPE;\nBEGIN\n  SELECT * INTO emp_rec\n  FROM employees\n  WHERE employee_id = 124;\nEND;\n/"),
            ("Associative array", "TYPE ename_table_type IS TABLE OF employees.last_name%TYPE\n  INDEX BY PLS_INTEGER;\nename_table ename_table_type;"),
        ],
        "examples": [
            {
                "title": "%ROWTYPE insert example from the slides",
                "text": "The employee row is selected into a record and then inserted into `retired_emps`.",
                "code": "DEFINE employee_number = 124\nDECLARE\n  emp_rec employees%ROWTYPE;\nBEGIN\n  SELECT *\n  INTO emp_rec\n  FROM employees\n  WHERE employee_id = &employee_number;\n\n  INSERT INTO retired_emps(empno, ename, job, mgr, hiredate, leavedate, sal, comm, deptno)\n  VALUES (emp_rec.employee_id, emp_rec.last_name, emp_rec.job_id,\n          emp_rec.manager_id, emp_rec.hire_date, SYSDATE,\n          emp_rec.salary, emp_rec.commission_pct, emp_rec.department_id);\nEND;\n/",
            },
            {
                "title": "Associative array example from the slides",
                "text": "The lesson stores employee rows in an INDEX BY table and prints last names.",
                "code": "SET SERVEROUTPUT ON\nDECLARE\n  TYPE emp_table_type IS TABLE OF employees%ROWTYPE INDEX BY PLS_INTEGER;\n  my_emp_table emp_table_type;\n  max_count NUMBER(3) := 104;\nBEGIN\n  FOR i IN 100..max_count LOOP\n    SELECT * INTO my_emp_table(i)\n    FROM employees\n    WHERE employee_id = i;\n  END LOOP;\n\n  FOR i IN my_emp_table.FIRST..my_emp_table.LAST LOOP\n    DBMS_OUTPUT.PUT_LINE(my_emp_table(i).last_name);\n  END LOOP;\nEND;\n/",
            },
        ],
        "checklist": ["Use records for related fields.", "Use `%ROWTYPE` when the full row structure is useful.", "Use associative arrays for in-memory collections.", "Check `EXISTS(index)` before reading sparse arrays."],
    },
    {
        "file": "Les07.ppt",
        "title": "Using Explicit Cursors",
        "focus": "Declaring, opening, fetching, closing, cursor FOR loops, parameters, and row locking.",
        "definitions": [
            ("Cursor", "A pointer to a private SQL work area. Oracle uses cursors to process SQL statements and keep track of query results."),
            ("Explicit cursor", "A named SQL area declared and controlled by the programmer for queries that can return multiple rows. It gives precise control over opening the query, fetching rows one by one, and closing the cursor."),
            ("Active set", "The rows returned by the cursor query when the cursor is opened. If table data changes later, the active set for that open cursor is already determined by the cursor execution."),
            ("OPEN", "The operation that executes the cursor query and identifies the active set. Cursor parameters, if any, are supplied at this point."),
            ("FETCH", "The operation that retrieves the next row from the active set into variables or a record. After each fetch, cursor attributes can be checked."),
            ("CLOSE", "The operation that releases the cursor's private SQL area. Explicit cursors should be closed when no longer needed."),
            ("Cursor FOR loop", "A compact loop that implicitly opens, fetches, exits, and closes a cursor. It also declares the loop record automatically, which reduces boilerplate and prevents forgetting to close the cursor."),
            ("Parameterized cursor", "A cursor that accepts values when opened. The same cursor declaration can then be reused for different departments, employees, or filter conditions."),
            ("FOR UPDATE", "A cursor clause that locks selected rows so they can be safely updated or deleted during the transaction."),
            ("WHERE CURRENT OF", "A clause used with an explicit cursor to update or delete the row most recently fetched by that cursor."),
        ],
        "syntax": [
            ("Cursor lifecycle", "DECLARE\n  CURSOR emp_cursor IS\n    SELECT employee_id, last_name\n    FROM employees\n    WHERE department_id = 30;\nBEGIN\n  OPEN emp_cursor;\n  LOOP\n    FETCH emp_cursor INTO empno, lname;\n    EXIT WHEN emp_cursor%NOTFOUND;\n  END LOOP;\n  CLOSE emp_cursor;\nEND;\n/"),
            ("Cursor FOR loop", "FOR emp_record IN emp_cursor LOOP\n  DBMS_OUTPUT.PUT_LINE(emp_record.employee_id || ' ' || emp_record.last_name);\nEND LOOP;"),
            ("Parameterized cursor", "CURSOR emp_cursor(deptno NUMBER) IS\n  SELECT employee_id, last_name\n  FROM employees\n  WHERE department_id = deptno;\n\nOPEN emp_cursor(10);"),
        ],
        "examples": [
            {
                "title": "Explicit cursor fetch loop from the slides",
                "text": "The cursor is opened, fetched until `%NOTFOUND`, then closed.",
                "code": "SET SERVEROUTPUT ON\nDECLARE\n  CURSOR emp_cursor IS\n    SELECT employee_id, last_name\n    FROM employees\n    WHERE department_id = 30;\n  empno employees.employee_id%TYPE;\n  lname employees.last_name%TYPE;\nBEGIN\n  OPEN emp_cursor;\n  LOOP\n    FETCH emp_cursor INTO empno, lname;\n    EXIT WHEN emp_cursor%NOTFOUND;\n    DBMS_OUTPUT.PUT_LINE(empno || ' ' || lname);\n  END LOOP;\n  CLOSE emp_cursor;\nEND;\n/",
            },
            {
                "title": "Cursor FOR loop from the slides",
                "text": "The cursor FOR loop implicitly opens, fetches, exits, and closes.",
                "code": "SET SERVEROUTPUT ON\nDECLARE\n  CURSOR emp_cursor IS\n    SELECT employee_id, last_name\n    FROM employees\n    WHERE department_id = 30;\nBEGIN\n  FOR emp_record IN emp_cursor LOOP\n    DBMS_OUTPUT.PUT_LINE(emp_record.employee_id || ' ' || emp_record.last_name);\n  END LOOP;\nEND;\n/",
            },
        ],
        "checklist": ["Declare the cursor query.", "Open it before fetching.", "Exit the fetch loop on `%NOTFOUND`.", "Close manually unless using a cursor FOR loop.", "Use cursor parameters for reusable queries."],
    },
    {
        "file": "Les08.ppt",
        "title": "Handling Exceptions",
        "focus": "Predefined, non-predefined, and user-defined exceptions; propagation and custom errors.",
        "definitions": [
            ("Exception", "A PL/SQL error raised during execution, either by Oracle or explicitly by your program. Exceptions separate normal logic from error-handling logic, making blocks easier to read."),
            ("Exception handler", "A `WHEN ... THEN` section that reacts to a raised exception. Only one handler runs for a raised exception, and after the handler finishes, control leaves that block."),
            ("Predefined exception", "A common Oracle error with a predefined PL/SQL name, such as `NO_DATA_FOUND`, `TOO_MANY_ROWS`, `ZERO_DIVIDE`, `INVALID_CURSOR`, or `DUP_VAL_ON_INDEX`. These can be handled directly by name."),
            ("Non-predefined exception", "An Oracle error that has an error number but no predefined PL/SQL name. You can give it a name with `PRAGMA EXCEPTION_INIT` and then handle it clearly."),
            ("User-defined exception", "An exception declared by the programmer for a business rule or application condition. It is raised explicitly with `RAISE`."),
            ("WHEN OTHERS", "A catch-all exception handler. It should be last and should usually log or re-raise the error; using it to silently hide errors is bad practice."),
            ("SQLCODE and SQLERRM", "`SQLCODE` returns the numeric error code and `SQLERRM` returns the error message for the current exception. They are commonly used for diagnostic logging."),
            ("Propagation", "Passing an unhandled exception to the enclosing block or calling environment. This allows an inner block to handle local problems while unexpected errors move outward."),
            ("RAISE_APPLICATION_ERROR", "A procedure used to return a custom Oracle-style error message to the caller. Application error numbers must be in the range -20000 to -20999."),
        ],
        "syntax": [
            ("Exception section", "EXCEPTION\n  WHEN NO_DATA_FOUND THEN\n    statements;\n  WHEN TOO_MANY_ROWS THEN\n    statements;\n  WHEN OTHERS THEN\n    statements;\nEND;"),
            ("Non-predefined exception", "DECLARE\n  insert_excep EXCEPTION;\n  PRAGMA EXCEPTION_INIT(insert_excep, -01400);\nBEGIN\n  -- code that can raise ORA-01400\nEXCEPTION\n  WHEN insert_excep THEN\n    DBMS_OUTPUT.PUT_LINE(SQLERRM);\nEND;\n/"),
            ("Application error", "DECLARE\n    user_excep EXCEPTION;\n    PRAGMA EXCEPTION_INIT(user_excep, -20202);\nBEGIN\n    RAISE_APPLICATION_ERROR(-20202, 'This is not a valid manager');\nEND;"),
        ],
        "examples": [
            {
                "title": "Handling TOO_MANY_ROWS from the slides",
                "text": "The exception handler explains that a cursor may be needed for multiple rows.",
                "code": "SET SERVEROUTPUT ON\nDECLARE\n  lname VARCHAR2(15);\nBEGIN\n  SELECT last_name\n  INTO lname\n  FROM employees\n  WHERE first_name = 'John';\n\n  DBMS_OUTPUT.PUT_LINE('John''s last name is : ' || lname);\nEXCEPTION\n  WHEN TOO_MANY_ROWS THEN\n    DBMS_OUTPUT.PUT_LINE('Your select statement retrieved multiple rows. Consider using a cursor.');\nEND;\n/",
            },
            {
                "title": "User-defined exception from the slides",
                "text": "If no department is updated, the block raises and handles `invalid_department`.",
                "code": "DECLARE\n  invalid_department EXCEPTION;\n  name   VARCHAR2(20) := '&name';\n  deptno NUMBER := &deptno;\nBEGIN\n  UPDATE departments\n  SET department_name = name\n  WHERE department_id = deptno;\n\n  IF SQL%NOTFOUND THEN\n    RAISE invalid_department;\n  END IF;\n  COMMIT;\nEXCEPTION\n  WHEN invalid_department THEN\n    DBMS_OUTPUT.PUT_LINE('No such department id.');\nEND;\n/",
            },
        ],
        "checklist": ["Place `WHEN OTHERS` last.", "Handle expected errors specifically.", "Use `SQLCODE` and `SQLERRM` for diagnostics.", "Raise custom business errors in the -20000 to -20999 range."],
    },
    {
        "file": "Les09.ppt",
        "title": "Stored Procedures and Functions",
        "focus": "Creating named subprograms, invoking them, and returning values from functions.",
        "definitions": [
            ("Subprogram", "A procedure or function stored in the database or declared inside another PL/SQL unit. Subprograms make code reusable, testable, and easier to maintain than repeating anonymous blocks."),
            ("Procedure", "A named PL/SQL block called to perform an action. Procedures are appropriate for tasks such as inserting rows, updating data, running validations, or coordinating several operations."),
            ("Function", "A named PL/SQL block that returns exactly one value with `RETURN`. Functions are appropriate when the main purpose is to compute and return a result."),
            ("Parameter", "A value passed between a caller and a subprogram. Parameters make subprograms reusable because the same code can run with different input values."),
            ("Parameter mode", "`IN` passes a value into a subprogram, `OUT` returns a value to the caller, and `IN OUT` does both. If no mode is specified, `IN` is the default."),
            ("Return type", "The data type of the value returned by a function. A function must execute a `RETURN` statement that provides a value compatible with this type."),
            ("Stored procedure/function", "A subprogram compiled and saved in the database schema. It can be granted to users, called from applications, and reused across sessions."),
            ("Anonymous block versus subprogram", "An anonymous block is usually temporary and unnamed. A subprogram is named, compiled, reusable, and can accept parameters."),
        ],
        "syntax": [
            ("Procedure", "CREATE OR REPLACE PROCEDURE procedure_name\nIS\nBEGIN\n  statements;\nEXCEPTION\n  handlers;\nEND;\n/"),
            ("Function", "CREATE OR REPLACE FUNCTION function_name(parameter datatype)\nRETURN datatype\nIS\nBEGIN\n  RETURN value;\nEND;\n/"),
            ("Invoke", "BEGIN\n  add_dept;\nEND;\n/"),
        ],
        "examples": [
            {
                "title": "Procedure example from the slides",
                "text": "`add_dept` inserts department 280 and reports the affected row count.",
                "code": "CREATE TABLE dept AS SELECT * FROM departments;\n\nCREATE OR REPLACE PROCEDURE add_dept IS\n  dept_id   dept.department_id%TYPE;\n  dept_name dept.department_name%TYPE;\nBEGIN\n  dept_id := 280;\n  dept_name := 'ST-Curriculum';\n\n  INSERT INTO dept(department_id, department_name)\n  VALUES (dept_id, dept_name);\n\n  DBMS_OUTPUT.PUT_LINE('Inserted ' || SQL%ROWCOUNT || ' row');\nEND;\n/",
            },
            {
                "title": "Function example from the slides",
                "text": "`check_sal` compares an employee salary to the average salary in that department.",
                "code": "CREATE OR REPLACE FUNCTION check_sal(empno employees.employee_id%TYPE)\nRETURN BOOLEAN IS\n  dept_id employees.department_id%TYPE;\n  sal     employees.salary%TYPE;\n  avg_sal employees.salary%TYPE;\nBEGIN\n  SELECT salary, department_id\n  INTO sal, dept_id\n  FROM employees\n  WHERE employee_id = empno;\n\n  SELECT AVG(salary)\n  INTO avg_sal\n  FROM employees\n  WHERE department_id = dept_id;\n\n  RETURN sal > avg_sal;\nEXCEPTION\n  WHEN NO_DATA_FOUND THEN\n    RETURN NULL;\nEND;\n/",
            },
        ],
        "checklist": ["Use procedures for actions.", "Use functions when a value must be returned.", "Do not include `DECLARE` in stored procedure/function syntax.", "Test subprograms with a small anonymous block."],
    },
    {
        "file": "les10.ppt",
        "title": "Creating Packages",
        "focus": "Package specifications, bodies, public/private members, global state, and maintenance.",
        "definitions": [
            ("Package", "A schema object that groups related types, variables, exceptions, procedures, and functions. Packages are used to organize PL/SQL code around a business area or technical service."),
            ("Package specification", "The public interface visible to users with privileges on the package. It declares what outside code is allowed to use: public variables, types, exceptions, procedures, and functions."),
            ("Package body", "The implementation, including private declarations and subprogram bodies. The body can change without forcing callers to change, as long as the specification stays the same."),
            ("Public component", "A package item declared in the specification. Public components can be referenced from outside the package with `package_name.component_name`."),
            ("Private component", "A package item declared only in the body. Private components support the package implementation but are hidden from callers, which improves encapsulation."),
            ("Package state", "Values of package variables that can persist for the duration of a database session. This can be useful, but it must be designed carefully because state can affect later calls in the same session."),
            ("Bodiless package", "A package that has only a specification and no body. This is possible when the package contains only declarations such as constants, types, or variables."),
            ("Overloading", "Defining multiple subprograms with the same name but different parameter lists. Packages commonly use overloading to provide related operations with convenient variations."),
            ("Encapsulation", "The design principle of exposing only what callers need and hiding internal details. Packages support encapsulation through the split between specification and body."),
        ],
        "syntax": [
            ("Specification", "CREATE OR REPLACE PACKAGE package_name IS\n  public declarations;\n  PROCEDURE procedure_name(parameter datatype);\nEND package_name;\n/"),
            ("Body", "CREATE OR REPLACE PACKAGE BODY package_name IS\n  private declarations;\n  PROCEDURE procedure_name(parameter datatype) IS\n  BEGIN\n    statements;\n  END;\nEND package_name;\n/"),
            ("Drop", "DROP PACKAGE package_name;\nDROP PACKAGE BODY package_name;"),
        ],
        "examples": [
            {
                "title": "Package specification from the slides",
                "text": "`comm_pkg` exposes a public variable and a public procedure.",
                "code": "CREATE OR REPLACE PACKAGE comm_pkg IS\n  std_comm NUMBER := 0.10;\n  PROCEDURE reset_comm(new_comm NUMBER);\nEND comm_pkg;\n/",
            },
            {
                "title": "Package body from the slides",
                "text": "The body hides `validate` and implements `reset_comm`.",
                "code": "CREATE OR REPLACE PACKAGE BODY comm_pkg IS\n  FUNCTION validate(comm NUMBER) RETURN BOOLEAN IS\n    max_comm employees.commission_pct%TYPE;\n  BEGIN\n    SELECT MAX(commission_pct)\n    INTO max_comm\n    FROM employees;\n    RETURN comm BETWEEN 0.0 AND max_comm;\n  END validate;\n\n  PROCEDURE reset_comm(new_comm NUMBER) IS\n  BEGIN\n    IF validate(new_comm) THEN\n      std_comm := new_comm;\n    ELSE\n      RAISE_APPLICATION_ERROR(-20210, 'Bad Commission');\n    END IF;\n  END reset_comm;\nEND comm_pkg;\n/",
            },
        ],
        "checklist": ["Put only the public contract in the specification.", "Hide implementation details in the body.", "Changing the body usually avoids recompiling callers.", "Use packages to group related subprograms and shared state."],
    },
    {
        "file": "les11.ppt",
        "title": "Creating Triggers",
        "focus": "DML triggers, timing, row triggers, OLD/NEW qualifiers, INSTEAD OF triggers, and management.",
        "definitions": [
            ("Trigger", "A stored PL/SQL block that runs automatically when a database event occurs. In this course, the focus is on DML triggers that fire for INSERT, UPDATE, or DELETE operations."),
            ("Statement trigger", "A trigger that fires once for the triggering statement, even if the statement affects zero, one, or many rows. Use it for rules that do not need individual row values."),
            ("Row trigger", "A trigger that fires once for each affected row and uses `FOR EACH ROW`. Use it when the logic must inspect or change values for each row."),
            ("Trigger timing", "The point when a trigger fires: BEFORE, AFTER, or INSTEAD OF. BEFORE triggers can validate or adjust values before the DML occurs; AFTER triggers are useful for auditing or follow-up actions."),
            ("Trigger event", "The operation that causes the trigger to fire: INSERT, UPDATE, or DELETE. A trigger can handle multiple events and use predicates such as `INSERTING`, `UPDATING`, and `DELETING`."),
            (":OLD and :NEW", "Row trigger qualifiers that expose column values before and after the DML operation. `:OLD` is available for UPDATE and DELETE; `:NEW` is available for INSERT and UPDATE."),
            ("WHEN clause", "A row-trigger condition that decides whether the trigger body runs for a particular row. It helps avoid putting all filtering logic inside the trigger body."),
            ("INSTEAD OF trigger", "A trigger defined on a view that runs instead of the requested DML. It is commonly used to make complex views updatable by translating the operation into changes on base tables."),
            ("Trigger firing sequence", "For a DML statement, Oracle fires BEFORE statement triggers, then BEFORE row and AFTER row triggers for each affected row, then AFTER statement triggers."),
            ("Trigger restriction", "Database triggers cannot use transaction control statements such as COMMIT, ROLLBACK, or SAVEPOINT. The triggering statement and trigger actions are part of the same transaction."),
        ],
        "syntax": [
            ("Statement trigger", "CREATE OR REPLACE TRIGGER secure_emp\nBEFORE INSERT OR UPDATE OR DELETE ON employees\nBEGIN\n  -- business rule\nEND;\n/"),
            ("Row trigger", "CREATE OR REPLACE TRIGGER restrict_salary\nBEFORE INSERT OR UPDATE OF salary ON employees\nFOR EACH ROW\nBEGIN\n  IF :NEW.salary > 15000 THEN\n    RAISE_APPLICATION_ERROR(-20202, 'Salary too high');\n  END IF;\nEND;\n/"),
            ("Manage triggers", "ALTER TRIGGER trigger_name DISABLE;\nALTER TRIGGER trigger_name ENABLE;\nALTER TABLE table_name DISABLE ALL TRIGGERS;\nDROP TRIGGER trigger_name;"),
        ],
        "examples": [
            {
                "title": "Statement trigger from the slides",
                "text": "`secure_emp` blocks inserts outside business hours.",
                "code": "CREATE OR REPLACE TRIGGER secure_emp\nBEFORE INSERT ON employees\nBEGIN\n  IF TO_CHAR(SYSDATE, 'DY') IN ('SAT', 'SUN')\n     OR TO_CHAR(SYSDATE, 'HH24:MI') NOT BETWEEN '08:00' AND '18:00' THEN\n    RAISE_APPLICATION_ERROR(\n      -20500,\n      'You may insert into EMPLOYEES table only during business hours.'\n    );\n  END IF;\nEND;\n/",
            },
            {
                "title": "Row trigger from the slides",
                "text": "`restrict_salary` checks each affected row with `:NEW`.",
                "code": "CREATE OR REPLACE TRIGGER restrict_salary\nBEFORE INSERT OR UPDATE OF salary ON employees\nFOR EACH ROW\nBEGIN\n  IF NOT (:NEW.job_id IN ('AD_PRES', 'AD_VP'))\n     AND :NEW.salary > 15000 THEN\n    RAISE_APPLICATION_ERROR(-20202, 'Employee cannot earn more than $15,000.');\n  END IF;\nEND;\n/",
            },
            {
                "title": "Audit trigger from the slides",
                "text": "`audit_emp_values` records old and new values after DML.",
                "code": "CREATE OR REPLACE TRIGGER audit_emp_values\nAFTER DELETE OR INSERT OR UPDATE ON employees\nFOR EACH ROW\nBEGIN\n  INSERT INTO audit_emp(user_name, time_stamp, id,\n                        old_last_name, new_last_name,\n                        old_title, new_title,\n                        old_salary, new_salary)\n  VALUES (USER, SYSDATE, :OLD.employee_id,\n          :OLD.last_name, :NEW.last_name,\n          :OLD.job_id, :NEW.job_id,\n          :OLD.salary, :NEW.salary);\nEND;\n/",
            },
        ],
        "checklist": ["Choose BEFORE or AFTER timing deliberately.", "Use row triggers only when row values are needed.", "Remember that COMMIT, ROLLBACK, and SAVEPOINT are not allowed in database triggers.", "Test triggering and non-triggering operations."],
    },
]


def apply_custom_style() -> None:
    st.markdown(
        """
        <style>
        :root {
            --recap-ink: #1f2933;
            --recap-muted: #5b6472;
            --recap-paper: #fffaf2;
            --recap-panel: #ffffff;
            --recap-line: #d8d1c5;
            --recap-accent: #c4513b;
            --recap-teal: #0f766e;
        }

        .stApp {
            background:
                linear-gradient(180deg, rgba(255,250,242,0.92) 0%, rgba(244,241,234,1) 42%),
                repeating-linear-gradient(90deg, rgba(31,41,51,0.035) 0 1px, transparent 1px 78px);
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1f2933 0%, #273848 100%);
            border-right: 1px solid rgba(255, 255, 255, 0.12);
        }

        [data-testid="stSidebar"] * {
            color: #f8fafc;
        }

        [data-testid="stSidebar"] [data-testid="stMetricValue"] {
            color: #ffd7bd;
        }

        h1, h2, h3 {
            color: var(--recap-ink);
            letter-spacing: 0;
        }

        h1 {
            padding-bottom: 0.35rem;
            border-bottom: 3px solid var(--recap-accent);
        }

        div[data-testid="stAlert"] {
            border: 1px solid var(--recap-line);
            border-left: 6px solid var(--recap-teal);
            border-radius: 8px;
            background-color: var(--recap-paper);
        }

        div[data-testid="stTabs"] button {
            border-radius: 6px 6px 0 0;
            color: var(--recap-muted);
        }

        div[data-testid="stTabs"] button[aria-selected="true"] {
            color: var(--recap-accent);
            font-weight: 700;
        }

        div[data-testid="stCodeBlock"] {
            border: 1px solid #26313d;
            border-radius: 8px;
            box-shadow: 0 10px 22px rgba(31, 41, 51, 0.10);
        }

        [data-testid="stDataFrame"] {
            border: 1px solid var(--recap-line);
            border-radius: 8px;
            overflow: hidden;
        }

        .author-card {
            margin-top: 1rem;
            padding: 0.85rem;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.16);
        }

        .author-card .label {
            color: #ffd7bd;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .author-card .name {
            margin-top: 0.25rem;
            font-size: 1rem;
            font-weight: 700;
        }

        .author-card .contact {
            margin-top: 0.15rem;
            font-size: 0.86rem;
            color: #e8eef5;
        }

        .footer-note {
            margin-top: 2.2rem;
            padding-top: 0.8rem;
            border-top: 1px solid var(--recap-line);
            color: var(--recap-muted);
            font-size: 0.9rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_author_card() -> None:
    st.sidebar.markdown(
        f"""
        <div class="author-card">
            <div class="label">Course recap prepared by</div>
            <div class="name">PhD Professor {AUTHOR_NAME}</div>
            <div class="contact">{AUTHOR_CONTACT}</div>
            <div class="website"><a href="https://adela-bara.ase.ro/" target="_blank">https://adela-bara.ase.ro/</a></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    st.markdown(
        f'<div class="footer-note">Prepared by <strong>PhD Professor {AUTHOR_NAME}</strong> | {AUTHOR_CONTACT} | 2026</div>',
        unsafe_allow_html=True,
    )


def page_header(lesson: dict) -> None:
    st.title(lesson["title"])
    st.caption(f"Source: `{lesson['file']}`")
    st.info(lesson["focus"])


def render_definitions(lesson: dict) -> None:
    for term, definition in lesson["definitions"]:
        st.markdown(f"**{term}**")
        st.write(definition)


def render_syntax(lesson: dict) -> None:
    for label, code in lesson["syntax"]:
        st.markdown(f"**{label}**")
        st.code(code, language="sql")


def render_examples(lesson: dict) -> None:
    for item in lesson["examples"]:
        if isinstance(item, dict):
            st.markdown(f"**{item['title']}**")
            if item.get("text"):
                st.write(item["text"])
            if item.get("code"):
                st.code(item["code"], language="sql")
        else:
            st.markdown(f"- {item}")


def render_checklist(lesson: dict, prefix: str) -> None:
    for item in lesson["checklist"]:
        st.checkbox(item, key=f"{prefix}-{lesson['file']}-{item}")


def render_exam_overview() -> None:
    st.subheader("Fast Exam Map")
    rows = [
        {"Area": lesson["title"], "Must know": lesson["focus"]}
        for lesson in LESSONS
    ]
    st.dataframe(rows, width="stretch", hide_index=True)

    st.subheader("Common Syntax To Memorize")
    st.code(
        """ -- PL/SQL blocks
DECLARE
  -- declarations
BEGIN
  -- executable statements
EXCEPTION
  WHEN exception_name THEN
    -- handler
END;
/

-- Using variables and SELECT INTO
SELECT column_list INTO variable_list
FROM table
WHERE condition;

--Exceptions
EXCEPTION
  WHEN NO_DATA_FOUND THEN
    -- handle no rows
  WHEN TOO_MANY_ROWS THEN
    -- handle multiple rows
  WHEN OTHERS THEN
    -- handle all other exceptions
    DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
    RAISE;

-- Cursors
CURSOR cursor_name IS select_statement;
OPEN cursor_name;
FETCH cursor_name INTO variables;
CLOSE cursor_name;

-- Procedures
CREATE OR REPLACE PROCEDURE name IS
BEGIN
  statements;
END;
/

-- Functions
CREATE OR REPLACE FUNCTION name(parameter datatype) RETURN datatype IS
BEGIN
  RETURN value;
EXCEPTION
  WHEN exception_name THEN
    RETURN value;
END;
/

-- Triggers
CREATE OR REPLACE TRIGGER name
BEFORE INSERT OR UPDATE OR DELETE ON table_name
[FOR EACH ROW]
BEGIN
  statements;
END;
/""",
        language="sql",
    )


@st.cache_data
def load_course_examples(modified_time_ns: int) -> list[dict]:
    del modified_time_ns
    with EXAMPLES_FILE.open(encoding="utf-8-sig") as examples_file:
        return json.load(examples_file)


def split_sql_into_chunks(lines: list[str], maximum_chunks: int = 6) -> list[str]:
    if not lines:
        return []

    chunk_count = min(maximum_chunks, len(lines))
    chunk_size, remainder = divmod(len(lines), chunk_count)
    chunks = []
    start = 0

    for index in range(chunk_count):
        end = start + chunk_size + (1 if index < remainder else 0)
        chunks.append("\n".join(lines[start:end]))
        start = end

    return chunks


def build_topic_puzzles(topic: dict) -> list[dict]:
    examples = topic.get("examples", [])
    if not examples:
        return []

    puzzles = []

    for puzzle_index in range(2):
        example = examples[puzzle_index % len(examples)]
        lines = [
            line.rstrip()
            for line in example.get("content", "").splitlines()
            if line.strip()
        ]

        if len(examples) == 1 and len(lines) >= 12:
            midpoint = len(lines) // 2
            lines = lines[:midpoint] if puzzle_index == 0 else lines[midpoint:]

        chunks = split_sql_into_chunks(lines)
        if not chunks:
            continue

        shuffled_indices = list(range(len(chunks)))
        random.Random(f"{topic['topic']}:{puzzle_index}").shuffle(shuffled_indices)
        if shuffled_indices == list(range(len(chunks))):
            shuffled_indices.reverse()

        shuffled_commands = [
            {
                "label": chr(ord("A") + label_index),
                "content": chunks[chunk_index],
                "original_index": chunk_index,
            }
            for label_index, chunk_index in enumerate(shuffled_indices)
        ]
        correct_order = [
            command["label"]
            for command in sorted(
                shuffled_commands, key=lambda command: command["original_index"]
            )
        ]
        puzzles.append(
            {
                "title": example["title"],
                "source": example.get("source", ""),
                "commands": shuffled_commands,
                "correct_order": correct_order,
            }
        )

    return puzzles


def meaningful_sql_lines(content: str) -> list[str]:
    return [
        line.strip()
        for line in content.splitlines()
        if line.strip()
        and not line.lstrip().startswith("--")
        and line.strip() != "/"
    ]


BUG_CONTEXT_ANCHORS = {
    "Cursors": re.compile(r"^\s*cursor\b", re.IGNORECASE),
    "Exceptions": re.compile(r"^\s*exception\s*$", re.IGNORECASE),
    "Packages": re.compile(
        r"^\s*create\s+or\s+replace\s+package(?:\s+body)?\b", re.IGNORECASE
    ),
    "Procedures": re.compile(
        r"^\s*create\s+or\s+replace\s+procedure\b", re.IGNORECASE
    ),
    "Functions": re.compile(
        r"^\s*create\s+or\s+replace\s+function\b", re.IGNORECASE
    ),
    "Triggers": re.compile(
        r"^\s*create\s+or\s+replace\s+trigger\b", re.IGNORECASE
    ),
}


def find_bug_context(
    topic_name: str, lines: list[str], challenge_index: int
) -> tuple[int, int] | None:
    anchor_pattern = BUG_CONTEXT_ANCHORS.get(topic_name)
    if not anchor_pattern:
        return None

    anchor_indices = [
        index
        for index, line in enumerate(lines)
        if not line.lstrip().startswith("--") and anchor_pattern.search(line)
    ]
    if not anchor_indices:
        return None

    anchor_index = anchor_indices[challenge_index % len(anchor_indices)]
    next_anchor = next(
        (index for index in anchor_indices if index > anchor_index),
        len(lines),
    )
    unit_end = next_anchor
    for index in range(anchor_index + 1, next_anchor):
        if lines[index].strip() == "/":
            unit_end = index + 1
            break

    return anchor_index, unit_end


def build_bug_challenges(topic: dict) -> list[dict]:
    examples = topic.get("examples", [])
    if not examples:
        return []

    distractor_pool = []
    for example in examples:
        distractor_pool.extend(meaningful_sql_lines(example.get("content", "")))

    challenges = []
    for challenge_index in range(2):
        example = examples[challenge_index % len(examples)]
        original_lines = example.get("content", "").splitlines()
        context_bounds = find_bug_context(
            topic["topic"], original_lines, challenge_index
        )
        if not context_bounds:
            continue
        context_start, unit_end = context_bounds

        candidate_indices = [
            index
            for index, line in enumerate(original_lines[context_start + 1 : unit_end])
            if line.strip()
            and not line.lstrip().startswith("--")
            and line.strip() != "/"
        ]
        candidate_indices = [
            index + context_start + 1
            for index in candidate_indices
        ]
        if not candidate_indices:
            continue

        target_position = random.Random(
            f"bug-target:{topic['topic']}:{challenge_index}"
        ).randrange(len(candidate_indices))
        missing_index = candidate_indices[target_position]
        missing_line = original_lines[missing_index].strip()

        context_end = min(unit_end, missing_index + 6)
        broken_lines = original_lines[context_start:context_end]
        marker_index = missing_index - context_start
        indentation = original_lines[missing_index][
            : len(original_lines[missing_index]) - len(original_lines[missing_index].lstrip())
        ]
        broken_lines[marker_index] = f"{indentation}-- ??? MISSING LINE ???"

        distractors = []
        for line in distractor_pool:
            if line != missing_line and line not in distractors:
                distractors.append(line)
        random.Random(f"bug-distractors:{topic['topic']}:{challenge_index}").shuffle(
            distractors
        )
        options = [missing_line] + distractors[:3]
        random.Random(f"bug-options:{topic['topic']}:{challenge_index}").shuffle(options)
        labeled_options = [
            {"label": chr(ord("A") + index), "content": option}
            for index, option in enumerate(options)
        ]
        correct_label = next(
            option["label"]
            for option in labeled_options
            if option["content"] == missing_line
        )

        challenges.append(
            {
                "title": example["title"],
                "source": example.get("source", ""),
                "broken_code": "\n".join(broken_lines),
                "options": labeled_options,
                "correct_label": correct_label,
            }
        )

    return challenges


def render_course_examples() -> None:
    st.title("Course Examples")
    st.caption("Open SQL Developer or VS Code with Oracle extension to run these examples.")

    try:
        topics = load_course_examples(EXAMPLES_FILE.stat().st_mtime_ns)
    except (OSError, json.JSONDecodeError) as error:
        st.error(f"Could not load course examples: {error}")
        return

    if not topics:
        st.info("No course examples are available.")
        return

    topic_names = [item["topic"] for item in topics]
    selected_topic = st.selectbox("Choose a topic", topic_names)
    topic = next(item for item in topics if item["topic"] == selected_topic)
    examples = topic.get("examples", [])

    st.subheader(selected_topic)
    st.caption(f"{len(examples)} example{'s' if len(examples) != 1 else ''}")

    for index, example in enumerate(examples, start=1):
        with st.expander(f"{index}. {example['title']}", expanded=index == 1):
            if example.get("description"):
                st.write(example["description"])
            if example.get("source"):
                st.caption(f"Source: `{example['source']}`")
            st.code(example.get("content", ""), language="sql")


def render_code_puzzles() -> None:
    st.title("Code Puzzles")
    st.write("Arrange the shuffled SQL commands in the order used by the original example.")

    try:
        topics = load_course_examples(EXAMPLES_FILE.stat().st_mtime_ns)
    except (OSError, json.JSONDecodeError) as error:
        st.error(f"Could not load course examples: {error}")
        return

    topics = [topic for topic in topics if topic.get("examples")]
    if not topics:
        st.info("No examples are available for puzzles.")
        return

    selected_topic = st.selectbox(
        "Choose a topic",
        [topic["topic"] for topic in topics],
        key="puzzle-topic",
    )
    topic = next(topic for topic in topics if topic["topic"] == selected_topic)
    puzzles = build_topic_puzzles(topic)
    if len(puzzles) < 2:
        st.error("This topic does not contain enough SQL content to build two puzzles.")
        return

    puzzle_number = st.radio(
        "Choose a puzzle",
        [1, 2],
        horizontal=True,
        format_func=lambda number: f"Puzzle {number}",
        key=f"puzzle-number-{selected_topic}",
    )
    puzzle = puzzles[puzzle_number - 1]

    st.subheader(puzzle["title"])
    if puzzle["source"]:
        st.caption(f"Based on: `{puzzle['source']}`")
    st.info("Each labeled block is one command group. Select each label exactly once.")

    for command in puzzle["commands"]:
        st.markdown(f"**Command {command['label']}**")
        st.code(command["content"], language="sql")

    labels = [command["label"] for command in puzzle["commands"]]
    form_key = f"puzzle-form-{selected_topic}-{puzzle_number}"
    with st.form(form_key):
        selected_order = [
            st.selectbox(
                f"Position {position}",
                ["Choose a command"] + labels,
                key=f"{form_key}-position-{position}",
            )
            for position in range(1, len(labels) + 1)
        ]
        submitted = st.form_submit_button("Check answer")

    if submitted:
        if "Choose a command" in selected_order or len(set(selected_order)) != len(labels):
            st.error("Fail. Select every command exactly once.")
        elif selected_order == puzzle["correct_order"]:
            st.success("Success! The commands are in the correct order.")
        else:
            st.error("Fail. The commands are not in the correct order.")


def render_find_the_bug() -> None:
    st.title("Find the Bug")
    st.write("Find the line removed from the original SQL example.")

    try:
        topics = load_course_examples(EXAMPLES_FILE.stat().st_mtime_ns)
    except (OSError, json.JSONDecodeError) as error:
        st.error(f"Could not load course examples: {error}")
        return

    topics = [topic for topic in topics if topic.get("examples")]
    if not topics:
        st.info("No examples are available for bug challenges.")
        return

    selected_topic = st.selectbox(
        "Choose a topic",
        [topic["topic"] for topic in topics],
        key="bug-topic",
    )
    topic = next(topic for topic in topics if topic["topic"] == selected_topic)
    challenges = build_bug_challenges(topic)
    if len(challenges) < 2:
        st.error("This topic does not contain enough SQL content for two challenges.")
        return

    challenge_number = st.radio(
        "Choose a challenge",
        [1, 2],
        horizontal=True,
        format_func=lambda number: f"Challenge {number}",
        key=f"bug-number-{selected_topic}",
    )
    challenge = challenges[challenge_number - 1]

    st.subheader(challenge["title"])
    if challenge["source"]:
        st.caption(f"Based on: `{challenge['source']}`")
    st.code(challenge["broken_code"], language="sql")

    st.markdown("**Which line is missing?**")
    for option in challenge["options"]:
        st.markdown(f"**Option {option['label']}**")
        st.code(option["content"], language="sql")

    form_key = f"bug-form-{selected_topic}-{challenge_number}"
    with st.form(form_key):
        selected_answer = st.selectbox(
            "Your answer",
            ["Choose an option"] + [
                option["label"] for option in challenge["options"]
            ],
            key=f"{form_key}-answer",
        )
        submitted = st.form_submit_button("Check answer")

    if submitted:
        if selected_answer == challenge["correct_label"]:
            st.success("Success! You found the missing line.")
        else:
            st.error("Fail. That is not the missing line.")


def main() -> None:
    st.set_page_config(page_title="PL/SQL Exam Recap", page_icon="DB", layout="wide")
    apply_custom_style()

    st.sidebar.title("PL/SQL Recap")
    st.sidebar.caption("Built from the PPT files: Oracle PL/SQL Fundamentals I - Les01.ppt to Les11.ppt")
    render_author_card()
    st.sidebar.divider()
    page_options = (
        ["Exam overview"]
        + [lesson["title"] for lesson in LESSONS]
        + ["Course examples", "Code puzzles", "Find the bug"]
    )
    selected = st.sidebar.radio("Choose a page", page_options)

    st.sidebar.divider()
    st.sidebar.metric("Lessons", len(LESSONS))
    st.sidebar.metric("PPT files summarized", len(LESSONS))

    if selected == "Exam overview":
        st.title("PL/SQL Exam Recap")
        st.caption(f"Prepared by {AUTHOR_NAME} | {AUTHOR_CONTACT}")
        st.write("Use these pages as a short revision guide before the exam. Each lesson keeps the key definitions, syntax patterns, and examples from the original slides.")
        render_exam_overview()
        render_footer()
        return

    if selected == "Course examples":
        render_course_examples()
        render_footer()
        return

    if selected == "Code puzzles":
        render_code_puzzles()
        render_footer()
        return

    if selected == "Find the bug":
        render_find_the_bug()
        render_footer()
        return

    lesson = next(item for item in LESSONS if item["title"] == selected)
    page_header(lesson)

    tab_recap, tab_defs, tab_syntax, tab_examples, tab_check = st.tabs(
        ["Recap", "Definitions", "Syntax", "Examples", "Checklist"]
    )
    with tab_recap:
        st.subheader("What students should remember")
        render_checklist(lesson, "recap")
    with tab_defs:
        render_definitions(lesson)
    with tab_syntax:
        render_syntax(lesson)
    with tab_examples:
        render_examples(lesson)
    with tab_check:
        st.subheader("Self-check")
        render_checklist(lesson, "check")
    render_footer()


if __name__ == "__main__":
    main()
