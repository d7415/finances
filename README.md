finances
===

Setup
---
To create the SQLite database

    sqlite3 finances < finances.sql


Usage
---
Command          | Parameters                                                                                | Description
-----------------|-------------------------------------------------------------------------------------------|-------------
v, view          | `[number]`                                                                                | Print the 5 (or `number`) most recent transactions.
a, add           |                                                                                           | Add a new transaction.
e, edit          | `<id>`                                                                                    | Edit the transaction with the specified id.
d, del, delete   | `<id>`                                                                                    | Delete the transaction with the specified id.
nt, newt         |                                                                                           | Add a new template for recurring monthly expenses.
aft              |                                                                                           | Add recurring monthly expenses based on a monthly statement date.
s, /, search     | `[i <id>] [d <date>] [m <method>] [p <place>] [c[a] <category>] [co <comment>] [results]` | Search transactions by the given criteria using SQL ILIKE. % may be used as a wildcard. Returns 10 results unless `results` is specified.
es, //, exact    | `[i <id>] [d <date>] [m <method>] [p <place>] [c[a] <category>] [co <comment>] [results]` | Search transactions by the given criteria. Returns 10 results unless `results` is specified.
st, stats        | `[number]`                                                                                | Show some basic statistics. The Top 3 lists can be adjusted by specifying `number`.
h, ?, help       |                                                                                           | Not implemented.
q, x, quit, exit |                                                                                           | Quit.

