--- pulseaudio-0.9.17/src/modules/rtp/module-rtp-send.c.orig	2009-09-03 07:02:45.000000000 +0530
+++ pulseaudio-0.9.17/src/modules/rtp/module-rtp-send.c	2009-09-11 20:29:06.904053782 +0530
@@ -296,7 +296,7 @@
     if (setsockopt(fd, IPPROTO_IP, IP_MULTICAST_LOOP, &j, sizeof(j)) < 0 ||
         setsockopt(sap_fd, IPPROTO_IP, IP_MULTICAST_LOOP, &j, sizeof(j)) < 0) {
         pa_log("IP_MULTICAST_LOOP failed: %s", pa_cstrerror(errno));
-        goto fail;
+        /* simply continue until completely fixed in Solaris (X86)  goto fail; */
     }
 
     if (ttl != DEFAULT_TTL) {
