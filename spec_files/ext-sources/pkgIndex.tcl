package ifneeded sqlite3 3.5 [list load [format "/usr/lib/tcl8.4/sqlite3/%s/libtclsqlite3.so"  [expr $tcl_platform(wordSize) * 8]] sqlite3]
