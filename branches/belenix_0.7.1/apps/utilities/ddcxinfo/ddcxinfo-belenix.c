#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "vbe.h"
/************* This is derived from ddcxinfo written by *****************\
#ident "$Id: ddcxinfo.c,v 1.7 1999/08/24 01:08:47 nalin Exp $"
modified by Klaus Knopper <knoppix@knopper.net> for KNOPPIX Feb. 2003
modified to max out the monitor for KNOPPIX July 2003
modified by Moinak Ghosh for BeleniX Oct 2005
modified by Moinak Ghosh to add parse_edid_detailed (from read_edid utility)
to parse EDID1 detailed timing block March 2006
\************************************************************************/

extern int parse_edid_detailed( unsigned char * edid, struct vbe_modeline *mode );

const char *monitor_start=
"Section \"Monitor\"\n"
"	Identifier   \"Monitor2\"\n";

const char *default_monitor_hfreqs=
"#	HorizSync    28.0 - 78.0 # Warning: This may fry very old Monitors\n"
"	HorizSync    28.0 - 96.0 # Warning: This may fry old Monitors\n";

const char *default_monitor_vfreqs=
"	VertRefresh  50.0 - 75.0 # Very conservative. May flicker.\n"
"#	VertRefresh  50.0 - 62.0 # Extreme conservative. Will flicker. TFT default.\n";

const char *default_modelines=
"	#  Default modes distilled from\n"
"	#      \"VESA and Industry Standards and Guide for Computer Display Monitor\n"
"	#       Timing\", version 1.0, revision 0.8, adopted September 17, 1998.\n"
"	#  $XFree86: xc/programs/Xserver/hw/xfree86/etc/vesamodes,v 1.4 1999/11/18 16:52:17 tsi Exp $\n"
"	# 640x350 @ 85Hz (VESA) hsync: 37.9kHz\n"
"	ModeLine \"640x350\"    31.5  640  672  736  832    350  382  385  445 +hsync -vsync\n"
"	# 640x400 @ 85Hz (VESA) hsync: 37.9kHz\n"
"	ModeLine \"640x400\"    31.5  640  672  736  832    400  401  404  445 -hsync +vsync\n"
"	# 720x400 @ 85Hz (VESA) hsync: 37.9kHz\n"
"	ModeLine \"720x400\"    35.5  720  756  828  936    400  401  404  446 -hsync +vsync\n"
"	# 640x480 @ 60Hz (Industry standard) hsync: 31.5kHz\n"
"	ModeLine \"640x480\"    25.2  640  656  752  800    480  490  492  525 -hsync -vsync\n"
"	# 640x480 @ 72Hz (VESA) hsync: 37.9kHz\n"
"	ModeLine \"640x480\"    31.5  640  664  704  832    480  489  491  520 -hsync -vsync\n"
"	# 640x480 @ 75Hz (VESA) hsync: 37.5kHz\n"
"	ModeLine \"640x480\"    31.5  640  656  720  840    480  481  484  500 -hsync -vsync\n"
"	# 640x480 @ 85Hz (VESA) hsync: 43.3kHz\n"
"	ModeLine \"640x480\"    36.0  640  696  752  832    480  481  484  509 -hsync -vsync\n"
"	# 800x600 @ 56Hz (VESA) hsync: 35.2kHz\n"
"	ModeLine \"800x600\"    36.0  800  824  896 1024    600  601  603  625 +hsync +vsync\n"
"	# 800x600 @ 60Hz (VESA) hsync: 37.9kHz\n"
"	ModeLine \"800x600\"    40.0  800  840  968 1056    600  601  605  628 +hsync +vsync\n"
"	# 800x600 @ 72Hz (VESA) hsync: 48.1kHz\n"
"	ModeLine \"800x600\"    50.0  800  856  976 1040    600  637  643  666 +hsync +vsync\n"
"	# 800x600 @ 75Hz (VESA) hsync: 46.9kHz\n"
"	ModeLine \"800x600\"    49.5  800  816  896 1056    600  601  604  625 +hsync +vsync\n"
"	# 800x600 @ 85Hz (VESA) hsync: 53.7kHz\n"
"	ModeLine \"800x600\"    56.3  800  832  896 1048    600  601  604  631 +hsync +vsync\n"
"	# 1024x768i @ 43Hz (industry standard) hsync: 35.5kHz\n"
"	ModeLine \"1024x768\"   44.9 1024 1032 1208 1264    768  768  776  817 +hsync +vsync Interlace\n"
"	# 1024x768 @ 60Hz (VESA) hsync: 48.4kHz\n"
"	ModeLine \"1024x768\"   65.0 1024 1048 1184 1344    768  771  777  806 -hsync -vsync\n"
"	# 1024x768 @ 70Hz (VESA) hsync: 56.5kHz\n"
"	ModeLine \"1024x768\"   75.0 1024 1048 1184 1328    768  771  777  806 -hsync -vsync\n"
"	# 1024x768 @ 75Hz (VESA) hsync: 60.0kHz\n"
"	ModeLine \"1024x768\"   78.8 1024 1040 1136 1312    768  769  772  800 +hsync +vsync\n"
"	# 1024x768 @ 85Hz (VESA) hsync: 68.7kHz\n"
"	ModeLine \"1024x768\"   94.5 1024 1072 1168 1376    768  769  772  808 +hsync +vsync\n"
"	# 1152x864 @ 75Hz (VESA) hsync: 67.5kHz\n"
"	ModeLine \"1152x864\"  108.0 1152 1216 1344 1600    864  865  868  900 +hsync +vsync\n"
"	# 1280x960 @ 60Hz (VESA) hsync: 60.0kHz\n"
"	ModeLine \"1280x960\"  108.0 1280 1376 1488 1800    960  961  964 1000 +hsync +vsync\n"
"	# 1280x960 @ 85Hz (VESA) hsync: 85.9kHz\n"
"	ModeLine \"1280x960\"  148.5 1280 1344 1504 1728    960  961  964 1011 +hsync +vsync\n"
"	# 1280x1024 @ 60Hz (VESA) hsync: 64.0kHz\n"
"	ModeLine \"1280x1024\" 108.0 1280 1328 1440 1688   1024 1025 1028 1066 +hsync +vsync\n"
"	# 1280x1024 @ 75Hz (VESA) hsync: 80.0kHz\n"
"	ModeLine \"1280x1024\" 135.0 1280 1296 1440 1688   1024 1025 1028 1066 +hsync +vsync\n"
"	# 1280x1024 @ 85Hz (VESA) hsync: 91.1kHz\n"
"	ModeLine \"1280x1024\" 157.5 1280 1344 1504 1728   1024 1025 1028 1072 +hsync +vsync\n"
"	# 1600x1200 @ 60Hz (VESA) hsync: 75.0kHz\n"
"	ModeLine \"1600x1200\" 162.0 1600 1664 1856 2160   1200 1201 1204 1250 +hsync +vsync\n"
"	# 1600x1200 @ 65Hz (VESA) hsync: 81.3kHz\n"
"	ModeLine \"1600x1200\" 175.5 1600 1664 1856 2160   1200 1201 1204 1250 +hsync +vsync\n"
"	# 1600x1200 @ 70Hz (VESA) hsync: 87.5kHz\n"
"	ModeLine \"1600x1200\" 189.0 1600 1664 1856 2160   1200 1201 1204 1250 +hsync +vsync\n"
"	# 1600x1200 @ 75Hz (VESA) hsync: 93.8kHz\n"
"	ModeLine \"1600x1200\" 202.5 1600 1664 1856 2160   1200 1201 1204 1250 +hsync +vsync\n"
"	# 1600x1200 @ 85Hz (VESA) hsync: 106.3kHz\n"
"	ModeLine \"1600x1200\" 229.5 1600 1664 1856 2160   1200 1201 1204 1250 +hsync +vsync\n"
"	# 1792x1344 @ 60Hz (VESA) hsync: 83.6kHz\n"
"	ModeLine \"1792x1344\" 204.8 1792 1920 2120 2448   1344 1345 1348 1394 -hsync +vsync\n"
"	# 1792x1344 @ 75Hz (VESA) hsync: 106.3kHz\n"
"	ModeLine \"1792x1344\" 261.0 1792 1888 2104 2456   1344 1345 1348 1417 -hsync +vsync\n"
"	# 1856x1392 @ 60Hz (VESA) hsync: 86.3kHz\n"
"	ModeLine \"1856x1392\" 218.3 1856 1952 2176 2528   1392 1393 1396 1439 -hsync +vsync\n"
"	# 1856x1392 @ 75Hz (VESA) hsync: 112.5kHz\n"
"	ModeLine \"1856x1392\" 288.0 1856 1984 2208 2560   1392 1393 1396 1500 -hsync +vsync\n"
"	# 1920x1440 @ 60Hz (VESA) hsync: 90.0kHz\n"
"	ModeLine \"1920x1440\" 234.0 1920 2048 2256 2600   1440 1441 1444 1500 -hsync +vsync\n"
"	# 1920x1440 @ 75Hz (VESA) hsync: 112.5kHz\n"
"	ModeLine \"1920x1440\" 297.0 1920 2064 2288 2640   1440 1441 1444 1500 -hsync +vsync\n"
"	# Additional modelines\n"
"	ModeLine \"1800x1440\"  230    1800 1896 2088 2392  1440 1441 1444 1490 +HSync +VSync\n"
"	ModeLine \"1800x1440\"  250    1800 1896 2088 2392  1440 1441 1444 1490 +HSync +VSync\n";

const char *extended_modelines=
"	# Extended modelines with GTF timings\n"
"	# 640x480 @ 100.00 Hz (GTF) hsync: 50.90 kHz; pclk: 43.16 MHz\n"
"	ModeLine \"640x480\"  43.16  640 680 744 848  480 481 484 509  -HSync +Vsync\n"
"	# 768x576 @ 60.00 Hz (GTF) hsync: 35.82 kHz; pclk: 34.96 MHz\n"
"	ModeLine \"768x576\"  34.96  768 792 872 976  576 577 580 597  -HSync +Vsync\n"
"	# 768x576 @ 72.00 Hz (GTF) hsync: 43.27 kHz; pclk: 42.93 MHz\n"
"	ModeLine \"768x576\"  42.93  768 800 880 992  576 577 580 601  -HSync +Vsync\n"
"	# 768x576 @ 75.00 Hz (GTF) hsync: 45.15 kHz; pclk: 45.51 MHz\n"
"	ModeLine \"768x576\"  45.51  768 808 888 1008  576 577 580 602  -HSync +Vsync\n"
"	# 768x576 @ 85.00 Hz (GTF) hsync: 51.42 kHz; pclk: 51.84 MHz\n"
"	ModeLine \"768x576\"  51.84  768 808 888 1008  576 577 580 605  -HSync +Vsync\n"
"	# 768x576 @ 100.00 Hz (GTF) hsync: 61.10 kHz; pclk: 62.57 MHz\n"
"	ModeLine \"768x576\"  62.57  768 816 896 1024  576 577 580 611  -HSync +Vsync\n"
"	# 800x600 @ 100.00 Hz (GTF) hsync: 63.60 kHz; pclk: 68.18 MHz\n"
"	ModeLine \"800x600\"  68.18  800 848 936 1072  600 601 604 636  -HSync +Vsync\n"
"	# 1024x768 @ 100.00 Hz (GTF) hsync: 81.40 kHz; pclk: 113.31 MHz\n"
"	ModeLine \"1024x768\"  113.31  1024 1096 1208 1392  768 769 772 814  -HSync +Vsync\n"
"	# 1152x864 @ 60.00 Hz (GTF) hsync: 53.70 kHz; pclk: 81.62 MHz\n"
"	ModeLine \"1152x864\"  81.62  1152 1216 1336 1520  864 865 868 895  -HSync +Vsync\n"
"	# 1152x864 @ 85.00 Hz (GTF) hsync: 77.10 kHz; pclk: 119.65 MHz\n"
"	ModeLine \"1152x864\"  119.65  1152 1224 1352 1552  864 865 868 907  -HSync +Vsync\n"
"	# 1152x864 @ 100.00 Hz (GTF) hsync: 91.50 kHz; pclk: 143.47 MHz\n"
"	ModeLine \"1152x864\"  143.47  1152 1232 1360 1568  864 865 868 915  -HSync +Vsync\n"
"	# 1280x960 @ 72.00 Hz (GTF) hsync: 72.07 kHz; pclk: 124.54 MHz\n"
"	ModeLine \"1280x960\"  124.54  1280 1368 1504 1728  960 961 964 1001  -HSync +Vsync\n"
"	# 1280x960 @ 75.00 Hz (GTF) hsync: 75.15 kHz; pclk: 129.86 MHz\n"
"	ModeLine \"1280x960\"  129.86  1280 1368 1504 1728  960 961 964 1002  -HSync +Vsync\n"
"	# 1280x960 @ 100.00 Hz (GTF) hsync: 101.70 kHz; pclk: 178.99 MHz\n"
"	ModeLine \"1280x960\"  178.99  1280 1376 1520 1760  960 961 964 1017  -HSync +Vsync\n"
"	# 1280x1024 @ 100.00 Hz (GTF) hsync: 108.50 kHz; pclk: 190.96 MHz\n"
"	ModeLine \"1280x1024\"  190.96  1280 1376 1520 1760  1024 1025 1028 1085  -HSync +Vsync\n"
"	# 1400x1050 @ 60.00 Hz (GTF) hsync: 65.22 kHz; pclk: 122.61 MHz\n"
"	ModeLine \"1400x1050\"  122.61  1400 1488 1640 1880  1050 1051 1054 1087  -HSync +Vsync\n"
"	# 1400x1050 @ 72.00 Hz (GTF) hsync: 78.77 kHz; pclk: 149.34 MHz\n"
"	ModeLine \"1400x1050\"  149.34  1400 1496 1648 1896  1050 1051 1054 1094  -HSync +Vsync\n"
"	# 1400x1050 @ 75.00 Hz (GTF) hsync: 82.20 kHz; pclk: 155.85 MHz\n"
"	ModeLine \"1400x1050\"  155.85  1400 1496 1648 1896  1050 1051 1054 1096  -HSync +Vsync\n"
"	# 1400x1050 @ 85.00 Hz (GTF) hsync: 93.76 kHz; pclk: 179.26 MHz\n"
"	ModeLine \"1400x1050\"  179.26  1400 1504 1656 1912  1050 1051 1054 1103  -HSync +Vsync\n"
"	# 1400x1050 @ 100.00 Hz (GTF) hsync: 111.20 kHz; pclk: 214.39 MHz\n"
"	ModeLine \"1400x1050\"  214.39  1400 1512 1664 1928  1050 1051 1054 1112  -HSync +Vsync\n"
"	# 1600x1200 @ 100.00 Hz (GTF) hsync: 127.10 kHz; pclk: 280.64 MHz\n"
"	ModeLine \"1600x1200\"  280.64  1600 1728 1904 2208  1200 1201 1204 1271  -HSync +Vsync\n";

const char *monitor_end=
"EndSection\n";

#define SHOW_HSYNC 1
#define SHOW_VSYNC 2
#define SHOW_MODELINES 4
#define SHOW_MONITOR 8
#define SHOW_MODES 16
#define SHOW_MONITOR_ID 32
#define SHOW_CARD_ID 64

int cmpmodeline(const void *a, const void *b)
{
	int hdiff  = ((struct vbe_modeline*)b)->width - ((struct vbe_modeline*)a)->width;
	int vdiff  = ((struct vbe_modeline*)b)->height - ((struct vbe_modeline*)a)->height;
	int fdiff = ((struct vbe_modeline*)b)->vfreq - ((struct vbe_modeline*)a)->vfreq;
	return hdiff?hdiff:vdiff?vdiff:fdiff?fdiff:0;
}

int countmodelines(struct vbe_modeline *m)
{
	int i;

	for(i=0; m[i].refresh != 0; i++);
	return i;
}

#define HMIN 640
#define HMAX 1680
#define VMIN 480
#define VMAX 1200
#define FMAX 180
#define FMIN 49

#define DEFAULTWIDTH 1024
#define DEFAULTHEIGHT 768

/* Check modelines for extreme values, return 0 if OK */
int checkmodelines(struct vbe_modeline *m)
{
	int i;
	if(!m) return 1;
	for(i=0; m[i].refresh != 0; i++)
	 {
		 if(m[i].modeline)
		  {
		   if(m[i].width>HMAX) return 1;
		   if(m[i].width<HMIN)  return 1;
		   if(m[i].height>VMAX)  return 1;
		   if(m[i].height<VMIN)  return 1;
		   if(m[i].vfreq>FMAX)  return 1;
		   if(m[i].vfreq<FMIN)  return 1;
		  }
	 }
	return 0;
}

/* Return position of modeline found, or -1 if none */
int findmodeline(struct vbe_modeline *m, int width, int height)
{
	int i;
	if(!m) return -1;
	for(i=0; m[i].refresh != 0; i++)
	 {
	  if(!m[i].modeline) continue;
	  if((m[i].width==width)&&(m[i].height==height)) return i;
	 }
	return -1;
}

void getfreqs(struct vbe_edid1_info *edid, 
             struct vbe_modeline* m,
             unsigned char *h1, unsigned char *h2,
             unsigned char *v1, unsigned char *v2)
{
 unsigned char hmin=255, vmin=255, hmax=0, vmax=0;
 int i;

 if(!m || countmodelines(m) == 0 || checkmodelines(m) != 0)
        parse_edid_detailed((unsigned char *)edid, m);

 vbe_get_edid_ranges(edid, &hmin, &hmax, &vmin, &vmax);
 if(!hmin && !hmax && !vmin && !vmax)
  {
   for(i = 0; m && (m[i].refresh != 0); i++)
    {
     if(m[i].hfreq)
      {
       if(hmin > m[i].hfreq) hmin = m[i].hfreq;
       if(hmax < m[i].hfreq) hmax = m[i].hfreq;
      }
     if(m[i].vfreq)
      {
       if(vmin > m[i].vfreq) vmin = m[i].vfreq;
       if(vmax < m[i].vfreq) vmax = m[i].vfreq;
      }
    }
  }
 *h1=hmin; *h2=hmax; *v1=vmin; *v2=vmax;
}

#define MODELINE_MATCH 1
#define MODELINE_FIRST 2
#define MODELINE_PERFECT 4

/* Return 1 if modeline resolution is listed in "standard" modes of Monitor,
 *        2 if listed at first, 4 if also vfreq matches. */
int bestmodeline(struct vbe_edid1_info* e, int width, int height, int freq)
 {
  int i, match=0;
  if(!e) return 0;
  /* Search in standard timings. */
  for(i = 0; i < 8; i++)
   {
    double aspect = 1;
    unsigned int x, y;
    unsigned char xres, vfreq;
    xres = e->standard_timing[i].xresolution;
    vfreq = e->standard_timing[i].vfreq;
    if((xres != vfreq) || ((xres != 0) && (xres !=1)) || ((vfreq != 0) && (vfreq != 1)))
     {
      switch(e->standard_timing[i].aspect)
       {
        case 1: aspect = 0.750; break;
        case 2: aspect = 0.800; break;
        case 3: aspect = 0.625; break;
        default: aspect = 1.0; break;
       }
      x = (xres + 31) * 8;
      y = x * aspect;
      if((width == x) && (height == y))
       {
	match|=MODELINE_MATCH;
	if(i==0) match|=MODELINE_FIRST;
	/* Perfect match */
	if(freq==((vfreq & 0x3f) + 60)) return (match|MODELINE_PERFECT);
       }
     }
   }
  return match;
 }

void showmodelines(struct vbe_edid1_info *edid, struct vbe_modeline* m)
{

 if(!m || countmodelines(m) == 0 || checkmodelines(m) != 0)
	parse_edid_detailed((unsigned char *)edid, m);

 if(m && countmodelines(m) && (checkmodelines(m)==0))
  {
   int maxwidth=0, maxheight=0, maxfreq=0, i;
   printf("\t# These are the DDC-probed settings reported by your monitor.\n"); fflush(stdout);
   for(i=0; m[i].refresh != 0; i++)
    {
     if(m[i].modeline)
      {
       if(maxwidth  < m[i].width)  maxwidth = m[i].width;
       if(maxheight < m[i].height) maxheight = m[i].height;
       if(maxfreq   < m[i].vfreq)  maxfreq = m[i].vfreq;
       printf("\t# %dx%d, %1.1f%sHz; hfreq=%.2f, vfreq=%.2f\n\t%s\n",
	         m[i].width, m[i].height,
	         m[i].refresh, m[i].interlaced?"i":"",
	         m[i].hfreq, m[i].vfreq,
	         m[i].modeline);
      }
    }
   printf("\n");
   printf(extended_modelines); fflush(stdout);
  }
 else
  {
   printf(default_modelines); printf(extended_modelines); fflush(stdout);
  }
}

void showmonitor(struct vbe_edid1_info* e, struct vbe_modeline* m,
	       	 unsigned char hmin, unsigned char hmax, unsigned char vmin,
		 unsigned char vmax)
{
  if (m && countmodelines(m) == 0) {
    if (parse_edid_detailed((unsigned char *)e, NULL) == 0) {
      return;
    }
  }
  printf(monitor_start); fflush(stdout);
  if(e && !(e->version == 0 && e->revision == 0)
       && !(e->version == 0xff && e->revision == 0xff))
   {
    char manufacturer[4] = { e->manufacturer_name.char1 + 'A' - 1,
                      e->manufacturer_name.char2 + 'A' - 1,
		      e->manufacturer_name.char3 + 'A' - 1,
			      0 };
     printf("\tVendorName\t\"%s\"\n", manufacturer); fflush(stdout);
     printf("\tModelName\t\"%s%04x\"\n", manufacturer, e->product_code); fflush(stdout);
   }
   /* Are these safe for HorizSync? */
   if(hmin>=28 && hmin<=150 && hmax >= 28 && hmax <= 150 && hmin <= hmax)
    {
     if((hmax - hmin) < 2) hmin = hmax - 2; /* XFree needs a little sloppyness */
     printf("\tHorizSync %d - %d # DDC-probed\n", hmin, hmax); fflush(stdout);
    }
   else
     printf(default_monitor_hfreqs); fflush(stdout);
   /* Are these safe for VertRefresh? */
   if(vmin>=FMIN && vmin<=FMAX && vmax >= FMIN && vmax <= FMAX && vmin <= vmax)
    {
     if((vmax - vmin) < 2) vmin = vmax - 2; /* XFree needs a little sloppyness */
     printf("\tVertRefresh %d - %d # DDC-probed\n", vmin, vmax); fflush(stdout);
    }
   else
    { printf(default_monitor_vfreqs); fflush(stdout); }
   showmodelines(e, m);
   printf(monitor_end); fflush(stdout);
}

#define HAS_1400x1050 (1<<0)
#define HAS_1280x1024 (1<<1)
#define HAS_1152x864  (1<<2)
#define HAS_1024x768  (1<<3)
#define HAS_800x600   (1<<4)
#define HAS_640x480   (1<<5)

void showmodes(struct vbe_edid1_info* e, struct vbe_modeline* m, char *firstmode)
{
 int i;
 unsigned int foundmodes=0;
 unsigned int maxwidth=0, maxheight=0;
 unsigned int widthlimit=HMAX, heightlimit=VMAX;
 unsigned int lastwidth=0, lastheight=0; /* for uniq */
 struct vbe_modeline *modes;

 printf("Modes"); 
 if(firstmode)
  {
   const char *delim="x@";
   char *s=strtok(firstmode,delim); /* "800x600" */
   if(s)
    {
     int firstwidth=atoi(s);
     s=strtok(NULL,delim);
     if((firstwidth>=HMIN) && (firstwidth<=HMAX) && (s!=NULL))
      {
       int firstheight=atoi(s);
       if((firstheight>=VMIN) && (firstheight<=VMAX))
	{
         lastwidth  = maxwidth  = widthlimit  = firstwidth;
         lastheight = maxheight = heightlimit = firstheight;
         switch(firstwidth)
  	  {
	   case 1400: foundmodes|=HAS_1400x1050; break;
	   case 1280: foundmodes|=HAS_1280x1024; break;
	   case 1152: foundmodes|=HAS_1152x864;  break;
	   case 1024: foundmodes|=HAS_1024x768;  break;
	   case 800:  foundmodes|=HAS_800x600;   break;
	   case 640:  foundmodes|=HAS_640x480;   break;
	  }
         printf(" \"%dx%d\"", firstwidth, firstheight);
	}
      }
    }
  }
 if(m&&countmodelines(m)&&(checkmodelines(m)==0))
  {
   for(i=0; m[i].refresh != 0; i++)
    {
     if(m[i].modeline)
      {
       if((m[i].width > widthlimit)   || (m[i].width<HMIN) ||
	  (m[i].height > heightlimit) || (m[i].height>HMAX)) continue; /* skip too extreme modes */
       if(m[i].width!=lastwidth || m[i].height != lastheight) /* Skip modes we already have */
        {
	 if(m[i].width>DEFAULTWIDTH || m[i].height>DEFAULTHEIGHT) /* This may still be too large for small monitors */
	  {
	   /* Only add mode if it is the _first_ standard mode of this Monitor */
	   /* (true for all TFT Displays?)                                   */
	   unsigned int matchmode;
	   matchmode = bestmodeline(e, m[i].width, m[i].height, m[i].vfreq);
	   if((matchmode&MODELINE_FIRST)==0) continue;
	  }
	 if(maxwidth<m[i].width)   maxwidth =m[i].width;
	 if(maxheight<m[i].height) maxheight=m[i].height;
	 switch(m[i].width)
	 {
		 case 1400: foundmodes|=HAS_1400x1050; break;
		 case 1280: foundmodes|=HAS_1280x1024; break;
		 case 1152: foundmodes|=HAS_1152x864;  break;
		 case 1024: foundmodes|=HAS_1024x768;  break;
		 case 800:  foundmodes|=HAS_800x600;   break;
		 case 640:  foundmodes|=HAS_640x480;   break;
	 }
	 /* Add "in between" modes */
         if(!(foundmodes&HAS_1400x1050) && ((lastwidth>1400) && (m[i].width<1400)) && ((lastheight>1050)&&(m[i].height<1050)))
	  { foundmodes|=HAS_1400x1050; printf(" \"1400x1050\""); }
         if(!(foundmodes&HAS_1280x1024) && ((lastwidth>1280) && (m[i].width<1280)) && ((lastheight>1024)&&(m[i].height<1024)))
	  { foundmodes|=HAS_1280x1024; printf(" \"1280x1024\""); }
	 if(!(foundmodes&HAS_1152x864) && ((lastwidth>1152) && (m[i].width<1152)) && ((lastheight>864)&&(m[i].height<864)))
	  { foundmodes|=HAS_1152x864;  printf(" \"1152x864\""); }
	 if(!(foundmodes&HAS_1024x768) && ((lastwidth>1024) && (m[i].width<1024)) && ((lastheight>768)&&(m[i].height<768)))
	  { foundmodes|=HAS_1024x768;  printf(" \"1024x768\""); }
	 if(!(foundmodes&HAS_800x600) && ((lastwidth>800) && (m[i].width<800)) && ((lastheight>600)&&(m[i].height<600)))
	  { foundmodes|=HAS_800x600;   printf(" \"800x600\""); }
	 if(!(foundmodes&HAS_640x480) && ((lastwidth>640) && (m[i].width<640)) && ((lastheight>480)&&(m[i].height<480)))
	  { foundmodes|=HAS_640x480;   printf(" \"640x480\""); }
	 printf(" \"%dx%d\"", m[i].width, m[i].height);
	}
       lastwidth=m[i].width; lastheight=m[i].height;
      }
    }
  }

  if(!maxwidth && !maxheight) /* No valid modes found! Probe Detailed Timings */
  {
    int dcount;

    /*
     * Get modelines from detailed timings
     */
    dcount = parse_edid_detailed((unsigned char *)e, modes);
    foundmodes = 0;

    if (dcount > 0) {
      for (i=0; i<dcount; i++) {
	/* skip too extreme modes */
        if((modes[i].width > widthlimit)   || (modes[i].width<HMIN) ||
	   (modes[i].height > heightlimit) || (modes[i].height>HMAX))
		continue;

	/* Skip modes we already have */
        if(modes[i].width!=lastwidth || modes[i].height != lastheight)
        {
          /* If we are here, then we do not have standard timings so can't
           * check for that.
           */

          if(maxwidth<modes[i].width)   maxwidth =modes[i].width;
	  if(maxheight<modes[i].height) maxheight=modes[i].height;
	  switch(modes[i].width)
	  {
		 case 1400: foundmodes|=HAS_1400x1050; break;
		 case 1280: foundmodes|=HAS_1280x1024; break;
		 case 1152: foundmodes|=HAS_1152x864;  break;
		 case 1024: foundmodes|=HAS_1024x768;  break;
		 case 800:  foundmodes|=HAS_800x600;   break;
		 case 640:  foundmodes|=HAS_640x480;   break;
	  }
	  /* Add "in between" modes */
          if(!(foundmodes&HAS_1400x1050) && ((lastwidth>1400) &&
            (modes[i].width<1400)) && ((lastheight>1050)&&(modes[i].height<1050)))
	   { foundmodes|=HAS_1400x1050; printf(" \"1400x1050\""); }

          if(!(foundmodes&HAS_1280x1024) && ((lastwidth>1280) &&
            (modes[i].width<1280)) && ((lastheight>1024)&&(modes[i].height<1024)))
	   { foundmodes|=HAS_1280x1024; printf(" \"1280x1024\""); }

	  if(!(foundmodes&HAS_1152x864) && ((lastwidth>1152) &&
            (modes[i].width<1152)) && ((lastheight>864)&&(modes[i].height<864)))
	   { foundmodes|=HAS_1152x864;  printf(" \"1152x864\""); }

	  if(!(foundmodes&HAS_1024x768) && ((lastwidth>1024) &&
            (modes[i].width<1024)) && ((lastheight>768)&&(modes[i].height<768)))
	   { foundmodes|=HAS_1024x768;  printf(" \"1024x768\""); }

	  if(!(foundmodes&HAS_800x600) && ((lastwidth>800) &&
            (modes[i].width<800)) && ((lastheight>600)&&(modes[i].height<600)))
	   { foundmodes|=HAS_800x600;   printf(" \"800x600\""); }

	  if(!(foundmodes&HAS_640x480) && ((lastwidth>640) &&
            (modes[i].width<640)) && ((lastheight>480)&&(modes[i].height<480)))
	   { foundmodes|=HAS_640x480;   printf(" \"640x480\""); }

	  printf(" \"%dx%d\"", modes[i].width, modes[i].height);    
        }
        lastwidth=modes[i].width; lastheight=modes[i].height;
      }
    }
  }

  if (!maxwidth && !maxheight) {
	/* Still no valid modes. Use default ones */
	printf ("\"1024x768\" \"800x600\" \"640x480\"");
  }

  /* Now add missing modes for low resolutions */
  if(maxwidth>=1400 && !(foundmodes&HAS_1400x1050)) printf(" \"1400x1050\"");
  if(maxwidth>=1280 && !(foundmodes&HAS_1280x1024)) printf(" \"1280x1024\"");
  if(maxwidth>=1152 && !(foundmodes&HAS_1152x864))  printf(" \"1152x864\"");
  if(maxwidth>=1024 && !(foundmodes&HAS_1024x768))  printf(" \"1024x768\"");
  if(maxwidth>=800  && !(foundmodes&HAS_800x600))   printf(" \"800x600\"");
  if(maxwidth>=640  && !(foundmodes&HAS_640x480))   printf(" \"640x480\"");
  printf("\n"); fflush(stdout);
}


int main(int argc, char **argv)
{
	struct vbe_modeline* modelines = NULL;
	/*struct vbe_modeline* tmp = NULL;*/
  	struct vbe_edid1_info* edid = NULL;
	char *firstmode = NULL;
	int i, whattodo=0;
	unsigned char hmin = -1, hmax = -1, vmin = -1, vmax = -1;
	char *edid_file = NULL;
	char *xorg_log = NULL;
/*
	int j;
	unsigned char *buf;
*/

	if(argc < 2)
	 {
		char *p = argv[0];
		if(strchr(p, '/')) {
			p = strchr(p, '/');
			p++;
		}
		fprintf(stderr,"syntax: %s [-hsync] [-vsync] [-modelines] [-monitor] [-modes] [-firstmode 1024x768]\n",p);
		fprintf(stderr,"        [-edidfile <raw EDID data file> | -xorglog <Xorg log file>]\n");
		exit(1);
	 }

	for(i = 1; i < argc; i++)
	 {
		if(strcmp(argv[i], "-hsync") == 0)          whattodo |= SHOW_HSYNC;
		else if(strcmp(argv[i], "-vsync") == 0)     whattodo |= SHOW_VSYNC;
		else if(strcmp(argv[i], "-modelines") == 0) whattodo |= SHOW_MODELINES;
		else if(strcmp(argv[i], "-monitor") == 0)   whattodo |= SHOW_MONITOR;
		else if(strcmp(argv[i], "-modes") == 0)     whattodo |= SHOW_MODES;
		else if(strcmp(argv[i], "-firstmode") == 0) {
			if((++i)<argc)
				firstmode=argv[i];
		} else if(strcmp(argv[i], "-edidfile") == 0) {
			if((++i)<argc)
				edid_file=argv[i];
		} else if(strcmp(argv[i], "-xorglog") == 0) {
			if((++i)<argc)
				xorg_log=argv[i];
		}
	 }

	if (edid_file && xorg_log) {
		fprintf(stderr, "Only one of -edidfile or -xorglog can be specified\n");
		exit(1);
	}

	edid = vbe_get_edid_info(edid_file, xorg_log);

/*
	buf = (unsigned char *)edid;
        for (i = 0; i < 128; i += 16) {
                for (j = 0; j < 16; ++j) {
                        printf("%02x", buf[i + j]);
                }
                printf("\n");
        }
*/

	modelines = vbe_get_edid_modelines(edid);

/*
	if (modelines && countmodelines(modelines) == 0) {
		if (parse_edid_detailed((unsigned char *)edid, &tmp) > 0) {
			free(modelines);
			modelines = tmp;
		}
	}
*/

	if(modelines) qsort(modelines,countmodelines(modelines),sizeof(struct vbe_modeline),cmpmodeline);
	getfreqs(edid, modelines, &hmin, &hmax, &vmin, &vmax);
	if(whattodo & SHOW_HSYNC) { printf("%d-%d\n", hmin, hmax); fflush(stdout); }
	if(whattodo & SHOW_VSYNC) { printf("%d-%d\n", vmin, vmax); fflush(stdout); }
	if(whattodo & SHOW_MODELINES) showmodelines(edid, modelines);
	if(whattodo & SHOW_MONITOR) showmonitor(edid, modelines, hmin, hmax, vmin, vmax);
	if(whattodo & SHOW_MODES && edid) showmodes(edid, modelines, firstmode);

	return (0);
}
