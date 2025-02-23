# Changelog

## [0.3.0] - 2025-02-22

*BREAKING CHANGES:* This release has breaking changes from 0.2.x.

### Added

- `DroltaResults` support Python's `with`-statement to ensure resources are freed

### Changed

- (breaking) Renamed `execute` to `query` to make its use more clear.
- (breaking) `QueryEngine` doesn't maintain a reference to a db Connection. The connection is passed to `query()`

### Fixed

- Fixed syntax error raised when calling `execute_query` and `execute` with empty strings

## [0.2.1] - 2025-02-12

### Fixed

- Removed "APPLES!!!" debugging print statement

## [0.2.0] - 2025-02-12

### Changed

- Update `IN` operator syntax to use parenthesis `()` instead of `[]` to align with SQLite syntax.
- Fix `IN` operator bug that used brackets `[]` in the SQL query.
- Drolta queries return `QueryResult` object instead of database cursor.
- Update the ANTLR4 grammar to enforce ordering between `GROUP BY`, `ORDER BY`, and `LIMIT`.
- Converted to MIT license

### Added

- Support for the `ASC` and `DESC` in `ORDER BY` clauses.
- Support for `OFFSET` in `LIMIT` clauses.
- Support for passing multiple columns to `ORDER BY`.
- Support for passing multiple columns to `GROUP BY`.
- Support for `NULL FIRST` and `NULL LAST` in `ORDER BY` clauses.
- Support for the `COUNT` aggregator in queries and rules.
- Support for the `AVG` aggregate function in queries and rules.
- Support for the `MAX` aggregate function in queries and rules.
- Support for the `MIN` aggregate function in queries and rules.
- Support for the `SUM` aggregate function in queries and rules.
- Support for `NOT IN`.
- Support for result variable aliases
- `description` property to query results to get column names and data types.

### Fixed

- Temporary tables not deleted between queries
- Using backslashes in f-strings (python<=3.11)
- `IN` operator using incorrect brackets in SQL

## [0.1.0] - 2025-02-03

_initial release._

[0.1.0]: https://github.com/ShiJbey/drolta_py/releases/v0.1.0
[0.2.0]: https://github.com/ShiJbey/drolta_py/releases/v0.2.0
[0.2.1]: https://github.com/ShiJbey/drolta_py/releases/v0.2.0
