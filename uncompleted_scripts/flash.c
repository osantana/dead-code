/*
 * AT-SPI - Assistive Technology Service Provider Interface
 * (Gnome Accessibility Project; http://developer.gnome.org/projects/gap)
 *
 * Copyright 2001, 2002 Sun Microsystems Inc.,
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Library General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Library General Public License for more details.
 *
 * You should have received a copy of the GNU Library General Public
 * License along with this library; if not, write to the
 * Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 */

#include <stdio.h>
#include <stdlib.h>
#include <X11/Xlib.h>

static void
visual_bell_notify (Display *display)
{
    Window root;
    int width, height;
    static  Window flash_window = None;
    root = RootWindow (display, DefaultScreen (display));
    width = DisplayWidth (display, DefaultScreen (display));
    height = DisplayHeight (display, DefaultScreen (display));
    if (flash_window == None)
    {
        flash_window = XCreateSimpleWindow (display, root,
                            0, 0, width, height,
                            0, 0L, 0L);
        XSelectInput (display, flash_window, ExposureMask);
        XMapWindow (display, flash_window);
    }
    else
    {
        /* just draw something in the window */
        GC gc = XCreateGC (display, flash_window, 0, NULL);
        XSetForeground (display, gc,
                WhitePixel (display, DefaultScreen (display)));
        XFillRectangle (display, flash_window, gc,
                0, 0, width, height);
        XSetForeground (display, gc,
                BlackPixel (display, DefaultScreen (display)));
        XFillRectangle (display, flash_window, gc,
                0, 0, width, height);
    }
    XFlush (display);
}

int main (int argc, char **argv)
{
    char *display_name = getenv ("DISPLAY");
    Display *display;
    if (!display_name) display_name = ":0.0";

    display = XOpenDisplay (display_name);
    if (!display)
    {
        fprintf (stderr, "Could not connect to display!\n");
        exit (-1);
    }
    visual_bell_notify (display);
}
