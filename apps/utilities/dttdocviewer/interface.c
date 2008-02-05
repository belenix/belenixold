/*
 * Copyright 2007 Sun Microsystems, Inc.  All rights reserved.
 * Use is subject to license terms.
 */

#ifdef HAVE_CONFIG_H
#  include <config.h>
#endif

#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>

#include <gdk/gdkkeysyms.h>
#include <gtk/gtk.h>

#include "callbacks.h"
#include "interface.h"
#include "support.h"

#define GLADE_HOOKUP_OBJECT(component,widget,name) \
  g_object_set_data_full (G_OBJECT (component), name, \
    gtk_widget_ref (widget), (GDestroyNotify) gtk_widget_unref)

#define GLADE_HOOKUP_OBJECT_NO_REF(component,widget,name) \
  g_object_set_data (G_OBJECT (component), name, widget)

static GtkTextBuffer *info_buffer = NULL;
static char line[512];

void
load_file (GtkWidget *view, char *filename)
{
	FILE *fp;
	char *s;
	GtkTextIter pos, pend;

	fp = fopen(filename, "r");
	if (fp == NULL) {
		perror("Error reading docs ");
		exit (1);
	}

	info_buffer = gtk_text_buffer_new (NULL);

	gtk_text_buffer_get_iter_at_offset(info_buffer, &pos, 0);
	line[0] = '\0';
	s = fgets(line, 512, fp);
	do {
		gtk_text_buffer_insert(info_buffer, &pos, line, strlen(line));
		s = fgets(line, 512, fp);
	} while (s != NULL && !feof(fp));

	fclose(fp);

	gtk_text_view_set_buffer(GTK_TEXT_VIEW(view), info_buffer);
}

GtkWidget*
create_window1 (void)
{
  GtkWidget *window1;
  GtkWidget *fixed1;
  GtkWidget *label1;
  GtkWidget *hseparator1;
  GtkWidget *notebook2;
  GtkWidget *scrolledwindow1;
  GtkWidget *Guideview;
  GtkWidget *Guide;
  GtkWidget *scrolledwindow2;
  GtkWidget *Contentsview;
  GtkWidget *Contents;
  GtkWidget *scrolledwindow4;
  GtkWidget *FAQview;
  GtkWidget *FAQ;
  GtkWidget *scrolledwindow5;
  GtkWidget *Historyview;
  GtkWidget *History;
  GtkWidget *scrolledwindow6;
  GtkWidget *Linkview;
  GtkWidget *Links;
  GtkWidget *scrolledwindow7;
  GtkWidget *Maintainerview;
  GtkWidget *Maintainer;
  GtkWidget *scrolledwindow8;
  GtkWidget *Readmeview;
  GtkWidget *Readme;
  GtkWidget *scrolledwindow9;
  GtkWidget *TODOview;
  GtkWidget *TODO;
  GtkWidget *scrolledwindow10;
  GtkWidget *Whoview;
  GtkWidget *Who;
  GtkWidget *scrolledwindow11;
  GtkWidget *Onelinersview;
  GtkWidget *Oneliners;
  GtkWidget *closebutton;
  GtkWidget *alignment1;
  GtkWidget *hbox1;
  GtkWidget *image1;
  GtkWidget *label13;

  window1 = gtk_window_new (GTK_WINDOW_TOPLEVEL);
  gtk_window_set_title (GTK_WINDOW (window1), _("DTrace Toolkit Docs"));
  gtk_window_set_type_hint (GTK_WINDOW (window1), GDK_WINDOW_TYPE_HINT_DIALOG);
  gtk_window_set_resizable (GTK_WINDOW (window1), FALSE);

  fixed1 = gtk_fixed_new ();
  gtk_widget_show (fixed1);
  gtk_container_add (GTK_CONTAINER (window1), fixed1);

  label1 = gtk_label_new (_("DTrace Toolkit Documentation Collection"));
  gtk_widget_show (label1);
  gtk_fixed_put (GTK_FIXED (fixed1), label1, 8, 8);
  gtk_widget_set_size_request (label1, 304, 24);
  gtk_misc_set_padding (GTK_MISC (label1), 0, 4);

  hseparator1 = gtk_hseparator_new ();
  gtk_widget_show (hseparator1);
  gtk_fixed_put (GTK_FIXED (fixed1), hseparator1, 0, 520);
  gtk_widget_set_size_request (hseparator1, 752, 16);

  notebook2 = gtk_notebook_new ();
  gtk_widget_show (notebook2);
  gtk_fixed_put (GTK_FIXED (fixed1), notebook2, 8, 40);
  gtk_widget_set_size_request (notebook2, 736, 480);
  gtk_notebook_set_tab_pos (GTK_NOTEBOOK (notebook2), GTK_POS_LEFT);

  scrolledwindow1 = gtk_scrolled_window_new (NULL, NULL);
  gtk_widget_show (scrolledwindow1);
  gtk_container_add (GTK_CONTAINER (notebook2), scrolledwindow1);

  Guideview = gtk_text_view_new ();
  gtk_widget_show (Guideview);
  gtk_container_add (GTK_CONTAINER (scrolledwindow1), Guideview);
  gtk_container_set_border_width (GTK_CONTAINER (Guideview), 2);
  gtk_text_view_set_editable (GTK_TEXT_VIEW (Guideview), FALSE);
  gtk_text_view_set_pixels_inside_wrap (GTK_TEXT_VIEW (Guideview), 2);

  Guide = gtk_label_new (_("Guide"));
  gtk_widget_show (Guide);
  gtk_notebook_set_tab_label (GTK_NOTEBOOK (notebook2), gtk_notebook_get_nth_page (GTK_NOTEBOOK (notebook2), 0), Guide);

  scrolledwindow2 = gtk_scrolled_window_new (NULL, NULL);
  gtk_widget_show (scrolledwindow2);
  gtk_container_add (GTK_CONTAINER (notebook2), scrolledwindow2);

  Contentsview = gtk_text_view_new ();
  gtk_widget_show (Contentsview);
  gtk_container_add (GTK_CONTAINER (scrolledwindow2), Contentsview);
  gtk_container_set_border_width (GTK_CONTAINER (Contentsview), 2);
  gtk_text_view_set_editable (GTK_TEXT_VIEW (Contentsview), FALSE);
  gtk_text_view_set_pixels_inside_wrap (GTK_TEXT_VIEW (Contentsview), 2);

  Contents = gtk_label_new (_("Contents"));
  gtk_widget_show (Contents);
  gtk_notebook_set_tab_label (GTK_NOTEBOOK (notebook2), gtk_notebook_get_nth_page (GTK_NOTEBOOK (notebook2), 1), Contents);

  scrolledwindow4 = gtk_scrolled_window_new (NULL, NULL);
  gtk_widget_show (scrolledwindow4);
  gtk_container_add (GTK_CONTAINER (notebook2), scrolledwindow4);

  FAQview = gtk_text_view_new ();
  gtk_widget_show (FAQview);
  gtk_container_add (GTK_CONTAINER (scrolledwindow4), FAQview);
  gtk_container_set_border_width (GTK_CONTAINER (FAQview), 2);
  gtk_text_view_set_editable (GTK_TEXT_VIEW (FAQview), FALSE);
  gtk_text_view_set_pixels_inside_wrap (GTK_TEXT_VIEW (FAQview), 2);

  FAQ = gtk_label_new (_("FAQ"));
  gtk_widget_show (FAQ);
  gtk_notebook_set_tab_label (GTK_NOTEBOOK (notebook2), gtk_notebook_get_nth_page (GTK_NOTEBOOK (notebook2), 2), FAQ);

  scrolledwindow5 = gtk_scrolled_window_new (NULL, NULL);
  gtk_widget_show (scrolledwindow5);
  gtk_container_add (GTK_CONTAINER (notebook2), scrolledwindow5);

  Historyview = gtk_text_view_new ();
  gtk_widget_show (Historyview);
  gtk_container_add (GTK_CONTAINER (scrolledwindow5), Historyview);
  gtk_container_set_border_width (GTK_CONTAINER (Historyview), 2);
  gtk_text_view_set_editable (GTK_TEXT_VIEW (Historyview), FALSE);
  gtk_text_view_set_pixels_inside_wrap (GTK_TEXT_VIEW (Historyview), 2);

  History = gtk_label_new (_("History"));
  gtk_widget_show (History);
  gtk_notebook_set_tab_label (GTK_NOTEBOOK (notebook2), gtk_notebook_get_nth_page (GTK_NOTEBOOK (notebook2), 3), History);

  scrolledwindow6 = gtk_scrolled_window_new (NULL, NULL);
  gtk_widget_show (scrolledwindow6);
  gtk_container_add (GTK_CONTAINER (notebook2), scrolledwindow6);

  Linkview = gtk_text_view_new ();
  gtk_widget_show (Linkview);
  gtk_container_add (GTK_CONTAINER (scrolledwindow6), Linkview);
  gtk_container_set_border_width (GTK_CONTAINER (Linkview), 2);
  gtk_text_view_set_editable (GTK_TEXT_VIEW (Linkview), FALSE);
  gtk_text_view_set_pixels_inside_wrap (GTK_TEXT_VIEW (Linkview), 2);

  Links = gtk_label_new (_("DTrace Links"));
  gtk_widget_show (Links);
  gtk_notebook_set_tab_label (GTK_NOTEBOOK (notebook2), gtk_notebook_get_nth_page (GTK_NOTEBOOK (notebook2), 4), Links);

  scrolledwindow7 = gtk_scrolled_window_new (NULL, NULL);
  gtk_widget_show (scrolledwindow7);
  gtk_container_add (GTK_CONTAINER (notebook2), scrolledwindow7);

  Maintainerview = gtk_text_view_new ();
  gtk_widget_show (Maintainerview);
  gtk_container_add (GTK_CONTAINER (scrolledwindow7), Maintainerview);
  gtk_container_set_border_width (GTK_CONTAINER (Maintainerview), 2);
  gtk_text_view_set_editable (GTK_TEXT_VIEW (Maintainerview), FALSE);
  gtk_text_view_set_pixels_inside_wrap (GTK_TEXT_VIEW (Maintainerview), 2);

  Maintainer = gtk_label_new (_("Maintainer"));
  gtk_widget_show (Maintainer);
  gtk_notebook_set_tab_label (GTK_NOTEBOOK (notebook2), gtk_notebook_get_nth_page (GTK_NOTEBOOK (notebook2), 5), Maintainer);

  scrolledwindow8 = gtk_scrolled_window_new (NULL, NULL);
  gtk_widget_show (scrolledwindow8);
  gtk_container_add (GTK_CONTAINER (notebook2), scrolledwindow8);

  Readmeview = gtk_text_view_new ();
  gtk_widget_show (Readmeview);
  gtk_container_add (GTK_CONTAINER (scrolledwindow8), Readmeview);
  gtk_container_set_border_width (GTK_CONTAINER (Readmeview), 2);
  gtk_text_view_set_editable (GTK_TEXT_VIEW (Readmeview), FALSE);
  gtk_text_view_set_pixels_inside_wrap (GTK_TEXT_VIEW (Readmeview), 2);

  Readme = gtk_label_new (_("Readme"));
  gtk_widget_show (Readme);
  gtk_notebook_set_tab_label (GTK_NOTEBOOK (notebook2), gtk_notebook_get_nth_page (GTK_NOTEBOOK (notebook2), 6), Readme);

  scrolledwindow9 = gtk_scrolled_window_new (NULL, NULL);
  gtk_widget_show (scrolledwindow9);
  gtk_container_add (GTK_CONTAINER (notebook2), scrolledwindow9);

  TODOview = gtk_text_view_new ();
  gtk_widget_show (TODOview);
  gtk_container_add (GTK_CONTAINER (scrolledwindow9), TODOview);
  gtk_container_set_border_width (GTK_CONTAINER (TODOview), 2);
  gtk_text_view_set_editable (GTK_TEXT_VIEW (TODOview), FALSE);
  gtk_text_view_set_pixels_inside_wrap (GTK_TEXT_VIEW (TODOview), 2);

  TODO = gtk_label_new (_("TODO"));
  gtk_widget_show (TODO);
  gtk_notebook_set_tab_label (GTK_NOTEBOOK (notebook2), gtk_notebook_get_nth_page (GTK_NOTEBOOK (notebook2), 7), TODO);

  scrolledwindow10 = gtk_scrolled_window_new (NULL, NULL);
  gtk_widget_show (scrolledwindow10);
  gtk_container_add (GTK_CONTAINER (notebook2), scrolledwindow10);

  Whoview = gtk_text_view_new ();
  gtk_widget_show (Whoview);
  gtk_container_add (GTK_CONTAINER (scrolledwindow10), Whoview);
  gtk_container_set_border_width (GTK_CONTAINER (Whoview), 2);
  gtk_text_view_set_editable (GTK_TEXT_VIEW (Whoview), FALSE);
  gtk_text_view_set_pixels_inside_wrap (GTK_TEXT_VIEW (Whoview), 2);

  Who = gtk_label_new (_("Who's Who"));
  gtk_widget_show (Who);
  gtk_notebook_set_tab_label (GTK_NOTEBOOK (notebook2), gtk_notebook_get_nth_page (GTK_NOTEBOOK (notebook2), 8), Who);

  scrolledwindow11 = gtk_scrolled_window_new (NULL, NULL);
  gtk_widget_show (scrolledwindow11);
  gtk_container_add (GTK_CONTAINER (notebook2), scrolledwindow11);

  Onelinersview = gtk_text_view_new ();
  gtk_widget_show (Onelinersview);
  gtk_container_add (GTK_CONTAINER (scrolledwindow11), Onelinersview);
  gtk_container_set_border_width (GTK_CONTAINER (Onelinersview), 2);
  gtk_text_view_set_editable (GTK_TEXT_VIEW (Onelinersview), FALSE);
  gtk_text_view_set_pixels_inside_wrap (GTK_TEXT_VIEW (Onelinersview), 2);

  Oneliners = gtk_label_new (_("One Liners"));
  gtk_widget_show (Oneliners);
  gtk_notebook_set_tab_label (GTK_NOTEBOOK (notebook2), gtk_notebook_get_nth_page (GTK_NOTEBOOK (notebook2), 9), Oneliners);

  closebutton = gtk_button_new ();
  gtk_widget_show (closebutton);
  gtk_fixed_put (GTK_FIXED (fixed1), closebutton, 648, 536);
  gtk_widget_set_size_request (closebutton, 88, 40);

  alignment1 = gtk_alignment_new (0.5, 0.5, 0, 0);
  gtk_widget_show (alignment1);
  gtk_container_add (GTK_CONTAINER (closebutton), alignment1);

  hbox1 = gtk_hbox_new (FALSE, 2);
  gtk_widget_show (hbox1);
  gtk_container_add (GTK_CONTAINER (alignment1), hbox1);

  image1 = gtk_image_new_from_stock ("gtk-close", GTK_ICON_SIZE_BUTTON);
  gtk_widget_show (image1);
  gtk_box_pack_start (GTK_BOX (hbox1), image1, FALSE, FALSE, 0);

  label13 = gtk_label_new_with_mnemonic (_("Close"));
  gtk_widget_show (label13);
  gtk_box_pack_start (GTK_BOX (hbox1), label13, FALSE, FALSE, 0);

  g_signal_connect ((gpointer) window1, "hide",
                    G_CALLBACK (gtk_main_quit),
                    NULL);
  g_signal_connect ((gpointer) closebutton, "clicked",
                    G_CALLBACK (gtk_main_quit),
                    NULL);

  /* Store pointers to all widgets, for use by lookup_widget(). */
  GLADE_HOOKUP_OBJECT_NO_REF (window1, window1, "window1");
  GLADE_HOOKUP_OBJECT (window1, fixed1, "fixed1");
  GLADE_HOOKUP_OBJECT (window1, label1, "label1");
  GLADE_HOOKUP_OBJECT (window1, hseparator1, "hseparator1");
  GLADE_HOOKUP_OBJECT (window1, notebook2, "notebook2");
  GLADE_HOOKUP_OBJECT (window1, scrolledwindow1, "scrolledwindow1");
  GLADE_HOOKUP_OBJECT (window1, Guideview, "Guideview");
  GLADE_HOOKUP_OBJECT (window1, Guide, "Guide");
  GLADE_HOOKUP_OBJECT (window1, scrolledwindow2, "scrolledwindow2");
  GLADE_HOOKUP_OBJECT (window1, Contentsview, "Contentsview");
  GLADE_HOOKUP_OBJECT (window1, Contents, "Contents");
  GLADE_HOOKUP_OBJECT (window1, scrolledwindow4, "scrolledwindow4");
  GLADE_HOOKUP_OBJECT (window1, FAQview, "FAQview");
  GLADE_HOOKUP_OBJECT (window1, FAQ, "FAQ");
  GLADE_HOOKUP_OBJECT (window1, scrolledwindow5, "scrolledwindow5");
  GLADE_HOOKUP_OBJECT (window1, Historyview, "Historyview");
  GLADE_HOOKUP_OBJECT (window1, History, "History");
  GLADE_HOOKUP_OBJECT (window1, scrolledwindow6, "scrolledwindow6");
  GLADE_HOOKUP_OBJECT (window1, Linkview, "Linkview");
  GLADE_HOOKUP_OBJECT (window1, Links, "Links");
  GLADE_HOOKUP_OBJECT (window1, scrolledwindow7, "scrolledwindow7");
  GLADE_HOOKUP_OBJECT (window1, Maintainerview, "Maintainerview");
  GLADE_HOOKUP_OBJECT (window1, Maintainer, "Maintainer");
  GLADE_HOOKUP_OBJECT (window1, scrolledwindow8, "scrolledwindow8");
  GLADE_HOOKUP_OBJECT (window1, Readmeview, "Readmeview");
  GLADE_HOOKUP_OBJECT (window1, Readme, "Readme");
  GLADE_HOOKUP_OBJECT (window1, scrolledwindow9, "scrolledwindow9");
  GLADE_HOOKUP_OBJECT (window1, TODOview, "TODOview");
  GLADE_HOOKUP_OBJECT (window1, TODO, "TODO");
  GLADE_HOOKUP_OBJECT (window1, scrolledwindow10, "scrolledwindow10");
  GLADE_HOOKUP_OBJECT (window1, Whoview, "Whoview");
  GLADE_HOOKUP_OBJECT (window1, Who, "Who");
  GLADE_HOOKUP_OBJECT (window1, scrolledwindow11, "scrolledwindow11");
  GLADE_HOOKUP_OBJECT (window1, Onelinersview, "Onelinersview");
  GLADE_HOOKUP_OBJECT (window1, Oneliners, "Oneliners");
  GLADE_HOOKUP_OBJECT (window1, closebutton, "closebutton");
  GLADE_HOOKUP_OBJECT (window1, alignment1, "alignment1");
  GLADE_HOOKUP_OBJECT (window1, hbox1, "hbox1");
  GLADE_HOOKUP_OBJECT (window1, image1, "image1");
  GLADE_HOOKUP_OBJECT (window1, label13, "label13");

  load_file(Guideview, "/opt/DTT/Guide");
  load_file(Contentsview, "/opt/DTT/Docs/Contents");
  load_file(FAQview, "/opt/DTT/Docs/Faq");
  load_file(Historyview, "/opt/DTT/Docs/History");
  load_file(Linkview, "/opt/DTT/Docs/Links");
  load_file(Maintainerview, "/opt/DTT/Docs/Maintainer");
  load_file(Readmeview, "/opt/DTT/Docs/Readme");
  load_file(TODOview, "/opt/DTT/Docs/ToDo");
  load_file(Whoview, "/opt/DTT/Docs/Who");
  load_file(Onelinersview, "/opt/DTT/Docs/oneliners.txt");

  return window1;
}

