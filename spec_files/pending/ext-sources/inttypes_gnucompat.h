#ifndef _INTTYPES_GNUCOMPAT_H
#define _INTTYPES_GNUCOMPAT_H

#include <sys/types.h>
#include <inttypes.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef uint8_t u_int8_t;
typedef uint16_t u_int16_t;
typedef uint32_t u_int32_t;
typedef uint64_t u_int64_t;

#ifdef __cplusplus
}
#endif
#endif

