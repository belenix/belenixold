#ifndef __CURL_CURLBUILD_WRAPPER_H
#define __CURL_CURLBUILD_WRAPPER_H
/***************************************************************************
 * This software is licensed as described in the file COPYING, which
 * you should have received as part of this distribution. The terms
 * are also available at http://curl.haxx.se/docs/copyright.html.
 *
 * You may opt to use, copy, modify, merge, publish, distribute and/or sell
 * copies of the Software, and permit persons to whom the Software is
 * furnished to do so, under the terms of the COPYING file.
 *
 * This software is distributed on an "AS IS" basis, WITHOUT WARRANTY OF ANY
 * KIND, either express or implied.
 *
 ***************************************************************************/

#ifdef _LP64
#include <curl/64/curlbuild.h>
#else
#include <curl/curlbuild.h>
#endif

#endif /* __CURL_CURLBUILD_WRAPPER_H */
