#include <sys/types.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <assert.h>
#include <limits.h>
#include <ctype.h>
#include <picl.h>
#include "vesamode.h"
#include "vbe.h"
#ident "$Id: vbe.c,v 1.9 2002/01/04 02:29:30 notting Exp $"

#define EDID1_LEN 128
static unsigned char *mem;

static int
walk_callback(picl_nodehdl_t nodeh, void *args)
{
        char vga[10];
        picl_propinfo_t pinfo;
        picl_prophdl_t ph;
        /*int i;*/

        if (picl_get_propval_by_name(nodeh, "driver-name", vga, 10) != 0) {
                return (PICL_WALK_CONTINUE);
        }
         
        if (strcmp(vga, "vgatext") != 0) {
                return (PICL_WALK_CONTINUE);
        }
         
        if (picl_get_propinfo_by_name(nodeh, "display-edif-block",
                                &pinfo, &ph) != 0) {
                return (PICL_WALK_TERMINATE);
        }      
               
        mem = (unsigned char *)malloc(pinfo.size);
	if (mem == NULL) {
		return (PICL_WALK_TERMINATE);
	}

        if (picl_get_propval(ph, mem, pinfo.size)) {
                (void) printf("Unable to get block\n");
                return (PICL_WALK_TERMINATE);
        }      
               
        /*(void) printf("display-edif-block = ");
        for (i = 0; i < pinfo.size; i++)
                (void) printf("%02x.", mem[i]);
        (void) putchar('\n');*/
               
        return (PICL_WALK_TERMINATE);
}       


/* Get EDID info. from the display-edif-block property of the vgatext device node */
struct vbe_edid1_info *vbe_get_edid_info(char *edid_file, char *xorg_log)
{
	struct vbe_edid1_info *ret = NULL;
        picl_nodehdl_t  hdl;
	u_int16_t man;
	int count = 0;

	mem = NULL;

	if (edid_file == NULL && xorg_log == NULL) {
        	if (picl_initialize() == 0) {
                	if (picl_get_root(&hdl) == 0) {
                        	if (picl_walk_tree_by_class(hdl, NULL,
                                	NULL, walk_callback) != 0) {
                                	picl_shutdown();
					return (NULL);
                        	}
                	} else {
                        	picl_shutdown();
				return (NULL);
                	}
        	} else {
			return (NULL);
        	}
        	picl_shutdown();

	} else if (edid_file != NULL) {
		/* Read raw EDID data from file */
		FILE *ef = fopen(edid_file, "r");

		if (ef != NULL) {
			mem = malloc(EDID1_LEN);
			if (fread(mem, EDID1_LEN, 1, ef) == 1) {
				perror("Unable to read edid file ");
				free(mem);
				mem = NULL;
			} 
			(void) fclose(ef);
		} else {
			perror("Unable to read edid file ");
		}

	} else if (xorg_log != NULL) {
		/* Parse EDID data block from Xorg logfile */
		FILE *fh;
		char line[512], hexbyte[5];
		char *xline, *pos;
		int edid_data = 0;
		int i, j;
		int bytes = 0;

		count = 0;
		mem = malloc(sizeof(struct _EDIFinfo));
		hexbyte[0] = '0';
		hexbyte[1] = 'x';
		hexbyte[4] = '\0';
		fh = fopen(xorg_log, "r");
		if (fh != NULL) {
			while ((xline = fgets(line, 512, fh)) != NULL) {
				if (strstr(xline, "EDID (in hex):")) {
					edid_data = 1;
					continue;
				}
				if (edid_data && count < 8) {
					pos = strstr(xline, " 	");
					if (!pos) {
						free(mem);
						mem = NULL;
						break;
					}

					pos += 2;
					for (i=0; i<16; i++) {
						j = i * 2;
						hexbyte[2] = pos[j];
						hexbyte[3] = pos[j+1];
						mem[bytes++] = strtol(hexbyte, NULL, 0);
					}
					count++;

				} else if (count == 8) {
					break;
				}
			}

			/* Second try to detect Raw EDID dump from NVIDIA binary
			   driver */
			if (count < 8) {
				bytes = 0;
				count = 0;
				if (mem == NULL)
					mem = malloc(sizeof(struct _EDIFinfo));
				rewind(fh);
				while ((xline = fgets(line, 512, fh)) != NULL) {
					if (strstr(xline, "Raw EDID bytes:")) {
						edid_data = 1;
						continue;
					}
					if (edid_data && count < 8) {
						pos = strstr(xline, "--- End of EDID");
						if (pos) {
							free(mem);
							mem = NULL;
							break;
						}
						pos = strstr(xline, ":   ");
						if (!pos)
							continue;
	
						pos += 4;
						for (i=0; i<48;) {
							while (pos[i] == ' ') i++;
							hexbyte[2] = pos[i];
							hexbyte[3] = pos[i+1];
							mem[bytes++] = strtol(hexbyte, NULL, 0);
							i += 2;
						}
						count++;
	
					} else if (count == 8) {
						break;
					}
				}
			}
			(void) fclose(fh);
		}
	}

	/*
 	 * mem == NULL means that either PICL did not find the
	 * display-edif-block or the EDID data file could not be read.
 	 * So either the monitor does not provide EDID data or there is
	 * some other problem. In any case we cannot continue.
 	 */
	if (mem == NULL || count < 8) {
		if (mem != NULL)
			free(mem);
		printf("No EDID data\n");
		return (NULL);
	}

	/* Get memory for return. */
	ret = malloc(sizeof(struct vbe_edid1_info));
	if(ret == NULL) {
		(void) free(mem);
		return (NULL);
	}

	/* Copy the buffer for return. */
	memcpy(ret, mem, sizeof(struct _EDIFinfo));

	memcpy(&man, &ret->manufacturer_name, 2);
	man = ntohs(man);
	memcpy(&ret->manufacturer_name, &man, 2);

	free(mem);
	mem = NULL;
	return ret;
}

/* Just read ranges from the EDID. */
void vbe_get_edid_ranges(struct vbe_edid1_info *edid,
			 unsigned char *hmin, unsigned char *hmax,
			 unsigned char *vmin, unsigned char *vmax)
{
	struct vbe_edid_monitor_descriptor *monitor;
	int i;

	*hmin = *hmax = *vmin = *vmax = 0;

	if (edid == NULL) {
		if((edid = vbe_get_edid_info(NULL, NULL)) == NULL) {
			return;
		}
	}

	for(i = 0; i < 4; i++) {
		monitor = &edid->monitor_details.monitor_descriptor[i];
		if(monitor->type == vbe_edid_monitor_descriptor_range) {
			*hmin = monitor->data.range_data.horizontal_min;
			*hmax = monitor->data.range_data.horizontal_max;
			*vmin = monitor->data.range_data.vertical_min;
			*vmax = monitor->data.range_data.vertical_max;
		}
	}
}

static int compare_vbe_modelines(const void *m1, const void *m2)
{
	const struct vbe_modeline *M1 = (const struct vbe_modeline*) m1;
	const struct vbe_modeline *M2 = (const struct vbe_modeline*) m2;
	if(M1->width < M2->width) return -1;
	if(M1->width > M2->width) return 1;
	return 0;
}

struct vbe_modeline *vbe_get_edid_modelines(struct vbe_edid1_info *edid)
{
	struct vbe_modeline *ret;
	char buf[LINE_MAX];
	int modeline_count = 0, i, j;

	if (edid == NULL) {
		if((edid = vbe_get_edid_info(NULL, NULL)) == NULL) {
			return NULL;
		}
	}

	memcpy(buf, &edid->established_timings,
	       sizeof(edid->established_timings));
	for(i = 0; i < (8 * sizeof(edid->established_timings)); i++) {
		if(buf[i / 8] & (1 << (i % 8))) {
			modeline_count++;
		}
	}

	/* Count the number of standard timings. */
	for(i = 0; i < 8; i++) {
		int x, v;
		x = edid->standard_timing[i].xresolution;
		v = edid->standard_timing[i].vfreq;
		if(((edid->standard_timing[i].xresolution & 0x01) != x) &&
		   ((edid->standard_timing[i].vfreq & 0x01) != v)) {
			modeline_count++;
		}
	}

	ret = malloc(sizeof(struct vbe_modeline) * (modeline_count + 1));
	if(ret == NULL) {
		return NULL;
	}
	memset(ret, 0, sizeof(struct vbe_modeline) * (modeline_count + 1));

	modeline_count = 0;

	/* Fill out established timings. */
	if(edid->established_timings.timing_720x400_70) {
		ret[modeline_count].width = 720;
		ret[modeline_count].height = 400;
		ret[modeline_count].refresh = 70;
		modeline_count++;
	}
	if(edid->established_timings.timing_720x400_88) {
		ret[modeline_count].width = 720;
		ret[modeline_count].height = 400;
		ret[modeline_count].refresh = 88;
		modeline_count++;
	}
	if(edid->established_timings.timing_640x480_60) {
		ret[modeline_count].width = 640;
		ret[modeline_count].height = 480;
		ret[modeline_count].refresh = 60;
		modeline_count++;
	}
	if(edid->established_timings.timing_640x480_67) {
		ret[modeline_count].width = 640;
		ret[modeline_count].height = 480;
		ret[modeline_count].refresh = 67;
		modeline_count++;
	}
	if(edid->established_timings.timing_640x480_72) {
		ret[modeline_count].width = 640;
		ret[modeline_count].height = 480;
		ret[modeline_count].refresh = 72;
		modeline_count++;
	}
	if(edid->established_timings.timing_640x480_75) {
		ret[modeline_count].width = 640;
		ret[modeline_count].height = 480;
		ret[modeline_count].refresh = 75;
		modeline_count++;
	}
	if(edid->established_timings.timing_800x600_56) {
		ret[modeline_count].width = 800;
		ret[modeline_count].height = 600;
		ret[modeline_count].refresh = 56;
		modeline_count++;
	}
	if(edid->established_timings.timing_800x600_60) {
		ret[modeline_count].width = 800;
		ret[modeline_count].height = 600;
		ret[modeline_count].refresh = 60;
		modeline_count++;
	}
	if(edid->established_timings.timing_800x600_72) {
		ret[modeline_count].width = 800;
		ret[modeline_count].height = 600;
		ret[modeline_count].refresh = 72;
		modeline_count++;
	}
	if(edid->established_timings.timing_800x600_75) {
		ret[modeline_count].width = 800;
		ret[modeline_count].height = 600;
		ret[modeline_count].refresh = 75;
		modeline_count++;
	}
	if(edid->established_timings.timing_832x624_75) {
		ret[modeline_count].width = 832;
		ret[modeline_count].height = 624;
		ret[modeline_count].refresh = 75;
		modeline_count++;
	}
	if(edid->established_timings.timing_1024x768_87i) {
		ret[modeline_count].width = 1024;
		ret[modeline_count].height = 768;
		ret[modeline_count].refresh = 87;
		ret[modeline_count].interlaced = 1;
		modeline_count++;
	}
	if(edid->established_timings.timing_1024x768_60){
		ret[modeline_count].width = 1024;
		ret[modeline_count].height = 768;
		ret[modeline_count].refresh = 60;
		modeline_count++;
	}
	if(edid->established_timings.timing_1024x768_70){
		ret[modeline_count].width = 1024;
		ret[modeline_count].height = 768;
		ret[modeline_count].refresh = 70;
		modeline_count++;
	}
	if(edid->established_timings.timing_1024x768_75){
		ret[modeline_count].width = 1024;
		ret[modeline_count].height = 768;
		ret[modeline_count].refresh = 75;
		modeline_count++;
	}
	if(edid->established_timings.timing_1280x1024_75) {
		ret[modeline_count].width = 1280;
		ret[modeline_count].height = 1024;
		ret[modeline_count].refresh = 75;
		modeline_count++;
	}

	/* Add in standard timings. */
	for(i = 0; i < 8; i++) {
		float aspect = 1;
		int x, v;
		x = edid->standard_timing[i].xresolution;
		v = edid->standard_timing[i].vfreq;
		if(((edid->standard_timing[i].xresolution & 0x01) != x) &&
		   ((edid->standard_timing[i].vfreq & 0x01) != v)) {
			switch(edid->standard_timing[i].aspect) {
				case aspect_75: aspect = 0.7500; break;
				case aspect_8: aspect = 0.8000; break;
				case aspect_5625: aspect = 0.5625; break;
				default: aspect = 1; break;
			}
			x = (edid->standard_timing[i].xresolution + 31) * 8;
			ret[modeline_count].width = x;
			ret[modeline_count].height = x * aspect;
			ret[modeline_count].refresh =
				edid->standard_timing[i].vfreq + 60;
			modeline_count++;
		}
	}

	/* Now tack on any matching modelines. */
	for(i = 0; ret[i].refresh != 0; i++) {
		struct vesa_timing_t *t = NULL;
		for(j = 0; known_vesa_timings[j].refresh != 0; j++) {
			t = &known_vesa_timings[j];
			if(ret[i].width == t->x)
			if(ret[i].height == t->y)
			if(ret[i].refresh == t->refresh) {
				snprintf(buf, sizeof(buf),
					 "ModeLine \"%dx%d\"\t%6.2f "
					 "%4d %4d %4d %4d %4d %4d %4d %4d %s %s"
					 , t->x, t->y, t->dotclock,
					 t->timings[0],
					 t->timings[0] + t->timings[1],
					 t->timings[0] + t->timings[1] +
					 t->timings[2],
					 t->timings[0] + t->timings[1] +
					 t->timings[2] + t->timings[3],
					 t->timings[4],
					 t->timings[4] + t->timings[5],
					 t->timings[4] + t->timings[5] +
					 t->timings[6],
					 t->timings[4] + t->timings[5] +
					 t->timings[6] + t->timings[7],
					 t->hsync == hsync_pos ?
					 "+hsync" : "-hsync",
					 t->vsync == vsync_pos ?
					 "+vsync" : "-vsync");
				ret[i].modeline = strdup(buf);
				ret[i].hfreq = t->hfreq;
				ret[i].vfreq = t->vfreq;
			}
		}
	}

	modeline_count = 0;
	for(i = 0; ret[i].refresh != 0; i++) {
		modeline_count++;
	}
	qsort(ret, modeline_count, sizeof(ret[0]), compare_vbe_modelines);

	return ret;
}

