/* This file is here to prevent a file conflict on multiarch systems.  A
 * conflict will occur because gmp.h has arch-specific definitions.
 *
 * DO NOT INCLUDE THE NEW FILE DIRECTLY -- ALWAYS INCLUDE THIS ONE INSTEAD. */

#if defined(_LP64)
#include "gmp-64.h"
#else
#include "gmp-i386.h"
#endif

