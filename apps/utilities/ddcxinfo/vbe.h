#ifndef vbe_h
#define vbe_h
#ident "$Id: vbe.h,v 1.1 1999/08/24 01:08:47 nalin Exp $"
#include <sys/types.h>

#ifndef __TYPEMAPS__
#define __TYPEMAPS__
typedef uint16_t u_int16_t;
typedef uint32_t u_int32_t;
#endif

struct _EDIFinfo {
        unsigned char hdr[8];
        unsigned short mfname; /* EISA style compressed id */
        unsigned short pid;
        unsigned long serialno;
        char mfweek;
        unsigned char mfyear;
        unsigned char edidver;
        unsigned char edidrev;
        unsigned char vidindef;
        unsigned char maxHimagesz; /* cm */
        unsigned char maxVimagesz; /* cm */
        unsigned char displayxferchar;
        unsigned char DPMSfeat;
        unsigned char RGlowbits;
        unsigned char BWlowbits;
        unsigned char redx;
        unsigned char redy;
        unsigned char greenx;
        unsigned char greeny;
        unsigned char bluex;
        unsigned char bluey;
        unsigned char whitex;
        unsigned char whitey;
        unsigned char esttimings1;
        unsigned char esttimings2;
        unsigned char rsvdtimings;
        short stdtimingid1;
        short stdtimingid2;
        short stdtimingid3;
        short stdtimingid4;
        short stdtimingid5;
        short stdtimingid6;
        short stdtimingid7;
        short stdtimingid8;
        unsigned char dettimingdesc1[18];
        unsigned char dettimingdesc2[18];
        unsigned char dettimingdesc3[18];
        unsigned char dettimingdesc4[18];
        unsigned char extflg;
        unsigned char chksum;
} __attribute__ ((packed));

/* Modeline information used by XFree86. */
struct vbe_modeline {
	u_int16_t width, height;
	unsigned char interlaced;
	float refresh;
	char *modeline;
	float hfreq, vfreq, pixel_clock;
};

/* Aspect ratios used in EDID info. */
enum vbe_edid_aspect {
	aspect_unknown = 0,
	aspect_75,
	aspect_8,
	aspect_5625,
};

/* Detailed timing information used in EDID v1.x */
struct vbe_edid_detailed_timing {
	u_int16_t pixel_clock;
#define VBE_EDID_DETAILED_TIMING_PIXEL_CLOCK(_x) \
	((_x).pixel_clock * 10000)
	unsigned char horizontal_active;
	unsigned char horizontal_blanking;
	unsigned char horizontal_active_hi: 4;
	unsigned char horizontal_blanking_hi: 4;
#define VBE_EDID_DETAILED_TIMING_HORIZONTAL_ACTIVE(_x) \
	(((_x).horizontal_active_hi << 8) + (_x).horizontal_active)
#define VBE_EDID_DETAILED_TIMING_HORIZONTAL_BLANKING(_x) \
	(((_x).horizontal_blanking_hi << 8) + (_x).horizontal_blanking)
	unsigned char vertical_active;
	unsigned char vertical_blanking;
	unsigned char vertical_active_hi: 4;
	unsigned char vertical_blanking_hi: 4;
#define VBE_EDID_DETAILED_TIMING_VERTICAL_ACTIVE(_x) \
	(((_x).vertical_active_hi << 8) + (_x).vertical_active)
#define VBE_EDID_DETAILED_TIMING_VERTICAL_BLANKING(_x) \
	(((_x).vertical_blanking_hi << 8) + (_x).vertical_blanking)
	unsigned char hsync_offset;
	unsigned char hsync_pulse_width;
	unsigned char vsync_offset: 4;
	unsigned char vsync_pulse_width: 4;
	unsigned char hsync_offset_hi: 2;
	unsigned char hsync_pulse_width_hi: 2;
	unsigned char vsync_offset_hi: 2;
	unsigned char vsync_pulse_width_hi: 2;
#define VBE_EDID_DETAILED_TIMING_HSYNC_OFFSET(_x) \
	(((_x).hsync_offset_hi << 8) + (_x).hsync_offset)
#define VBE_EDID_DETAILED_TIMING_HSYNC_PULSE_WIDTH(_x) \
	(((_x).hsync_pulse_width_hi << 8) + (_x).hsync_pulse_width)
#define VBE_EDID_DETAILED_TIMING_VSYNC_OFFSET(_x) \
	(((_x).vsync_offset_hi << 4) + (_x).vsync_offset)
#define VBE_EDID_DETAILED_TIMING_VSYNC_PULSE_WIDTH(_x) \
	(((_x).vsync_pulse_width_hi << 4) + (_x).vsync_pulse_width)
	unsigned char himage_size;
	unsigned char vimage_size;
	unsigned char himage_size_hi: 4;
	unsigned char vimage_size_hi: 4;
#define VBE_EDID_DETAILED_TIMING_HIMAGE_SIZE(_x) \
	(((_x).himage_size_hi << 8) + (_x).himage_size)
#define VBE_EDID_DETAILED_TIMING_VIMAGE_SIZE(_x) \
	(((_x).vimage_size_hi << 8) + (_x).vimage_size)
	unsigned char hborder;
	unsigned char vborder;
	struct {
		unsigned char interlaced: 1;
		unsigned char stereo: 2;
		unsigned char digital_composite: 2;
		unsigned char variant: 2;
		unsigned char zero: 1;
	} flags __attribute__ ((packed));
} __attribute__ ((packed));

enum {
	vbe_edid_monitor_descriptor_serial = 0xff,
	vbe_edid_monitor_descriptor_ascii = 0xfe,
	vbe_edid_monitor_descriptor_range = 0xfd,
	vbe_edid_monitor_descriptor_name = 0xfc,
} vbe_edid_monitor_descriptor_types;

struct vbe_edid_monitor_descriptor {
	u_int16_t zero_flag_1;
	unsigned char zero_flag_2;
	unsigned char type;
	unsigned char zero_flag_3;
	union {
		char string[13];
		struct {
			unsigned char vertical_min;
			unsigned char vertical_max;
			unsigned char horizontal_min;
			unsigned char horizontal_max;
			unsigned char pixel_clock_max;
			unsigned char gtf_data[8];
		} range_data;
	} data;
} __attribute__ ((packed));

struct vbe_edid1_info {
	unsigned char header[8];
	struct {
		u_int16_t char3: 5;
		u_int16_t char2: 5;
		u_int16_t char1: 5;
		u_int16_t zero: 1;
	} manufacturer_name __attribute__ ((packed));
	u_int16_t product_code;
	u_int32_t serial_number;
	unsigned char week;
	unsigned char year;
	unsigned char version;
	unsigned char revision;
	struct {
		unsigned char separate_sync: 1;
		unsigned char composite_sync: 1;
		unsigned char sync_on_green: 1;
		unsigned char unused: 2;
		unsigned char voltage_level: 2;
		unsigned char digital: 1;
	} video_input_definition __attribute__ ((packed));
	unsigned char max_size_horizontal;
	unsigned char max_size_vertical;
	unsigned char gamma;
	struct {
		unsigned char unused1: 3;
		unsigned char rgb: 1;
		unsigned char unused2: 1;
		unsigned char active_off: 1;
		unsigned char suspend: 1;
		unsigned char standby: 1;
	} feature_support __attribute__ ((packed));
	unsigned char color_characteristics[10];
	struct {
		unsigned char timing_720x400_70: 1;
		unsigned char timing_720x400_88: 1;
		unsigned char timing_640x480_60: 1;
		unsigned char timing_640x480_67: 1;
		unsigned char timing_640x480_72: 1;
		unsigned char timing_640x480_75: 1;
		unsigned char timing_800x600_56: 1;
		unsigned char timing_800x600_60: 1;
		unsigned char timing_800x600_72: 1;
		unsigned char timing_800x600_75: 1;
		unsigned char timing_832x624_75: 1;
		unsigned char timing_1024x768_87i: 1;
		unsigned char timing_1024x768_60: 1;
		unsigned char timing_1024x768_70: 1;
		unsigned char timing_1024x768_75: 1;
		unsigned char timing_1280x1024_75: 1;
	} established_timings __attribute__ ((packed));
	struct {
		unsigned char timing_1152x870_75: 1;
		unsigned char reserved: 7;
	} manufacturer_timings __attribute__ ((packed));
	struct {
		u_int16_t xresolution: 8;
		u_int16_t vfreq: 6;
		u_int16_t aspect: 2;
	} standard_timing[8] __attribute__ ((packed));
	union {
		struct vbe_edid_detailed_timing detailed_timing[4];
		struct vbe_edid_monitor_descriptor monitor_descriptor[4];
	} monitor_details __attribute__ ((packed));
	unsigned char extension_flag;
	unsigned char checksum;
	unsigned char padding[128];
} __attribute__ ((packed));

#define VBE_LINEAR_FRAMEBUFFER 0x4000

struct vbe_edid1_info *vbe_get_edid_info(char *edid_file, char *xorg_log);

/* Get the ranges of values suitable for the attached monitor. */
void vbe_get_edid_ranges(struct vbe_edid1_info *edid,
			 unsigned char *hmin, unsigned char *hmax,
			 unsigned char *vmin, unsigned char *vmax);

/* Get a list of modelines that will work with this monitor. */
struct vbe_modeline *vbe_get_edid_modelines(struct vbe_edid1_info *edid);


#define DETAILED_TIMING_DESCRIPTIONS_START      0x36
#define DETAILED_TIMING_DESCRIPTION_SIZE        18
#define NO_DETAILED_TIMING_DESCRIPTIONS         4

#define DETAILED_TIMING_DESCRIPTION_1           0x36
#define DETAILED_TIMING_DESCRIPTION_2           0x48
#define DETAILED_TIMING_DESCRIPTION_3           0x5a
#define DETAILED_TIMING_DESCRIPTION_4           0x6c

#endif
