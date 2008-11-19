/*
 * Mount NTFS - Mount an NTFS file system
 * using the NFS file system and an NFS server
 * Copyright (c) 2006 by Martin Rosenau
 *
 * This is free software; you can redistribute it and/or modify it under the
 * terms of the GNU General Public License, see the file COPYING.
 *
 * Comparing unicode file names case-insensitive
 *
 * Currently only characters below 128 are compared
 * case-insensitive
 */
#include "ntfs.h"

/* Compare two Unicode texts
 * Both texts are two-byte strings (not UTF-8) in
 * little endian storage (lower byte stored first)
 * They have the same length (len) and are not
 * (necessarily) NUL-terminated.
 * 0 is returned if the strings are not equal, 1 otherwise */
int compare_unicode(const char *text1,const char *text2,int len)
{
    for(;len>0;len--,text1+=2,text2+=2)
    {
        if(!text1[1] && !text2[1] &&
            (text1[0]&0xDF)>='A' && (text1[0]&0xDF)<='Z' &&
            (text1[0]&0xDF)==(text2[0]&0xDF))
                continue;
        else if(text1[0]!=text2[0] || text1[1]!=text2[1])
            return 0;
    }
    return 1;
}
