%define plymouthdaemon_execdir /sbin
%define plymouthclient_execdir /bin
%define plymouth_libdir /%{_lib}

Summary: Plymouth Graphical Boot Animation and Logger
Name: plymouth
Version: 0.6.0
Release: 0.2008.10.21.2%{?dist}
License: GPLv2+
Group: System Environment/Base
Source0: http://freedesktop.org/software/plymouth/releases/%{name}-%{version}.tar.bz2
URL: http://freedesktop.org/software/plymouth/releases
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Obsoletes: rhgb < 1:10.0.0
Provides: rhgb = 1:10.0.0

Requires: system-logos >= 9.0.1
Requires: system-plymouth-plugin >= %{version}-%{release}
Requires(post): plymouth-scripts
Requires: initscripts >= 8.83-1

%description
Plymouth provides an attractive graphical boot animation in
place of the text messages that normally get shown.  Text
messages are instead redirected to a log file for viewing
after boot.

%package libs
Summary: Plymouth libraries
Group: Development/Libraries

%description libs
This package contains the libply and libplybootsplash libraries
used by Plymouth.

%package devel
Summary: Libraries and headers for writing Plymouth splash plugins
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the libply and libplybootsplash libraries
and headers needed to develop 3rd party splash plugins for Plymouth.

%package utils
Summary: Plymouth related utilities
Group: Applications/System
Requires: %{name} = %{version}-%{release}
BuildRequires: gtk2-devel

%description utils
This package contains utilities that integrate with Plymouth
including a boot log viewing application.

%package scripts
Summary: Plymouth related scripts
Group: Applications/System
Requires: nash

%description scripts
This package contains scripts that help integrate Plymouth with
the system.

%package gdm-hooks
Summary: Plymouth GDM integration
Group: Applications/System
Requires: gdm >= 1:2.22.0
Requires: plymouth-utils
Requires: %{name} = %{version}-%{release}

%description gdm-hooks
This package contains support files for integrating Plymouth with GDM
Namely, it adds hooks to show boot messages at the login screen in the
event start-up services fail.

%package plugin-label
Summary: Plymouth label plugin
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}
BuildRequires: pango-devel
BuildRequires: cairo-devel

%description plugin-label
This package contains the label control plugin for
Plymouth. It provides the ability to render text on
graphical boot splashes using pango and cairo.

%package plugin-fade-in
Summary: Plymouth "Fade-In" plugin
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}
Requires(post): %{_sbindir}/plymouth-set-default-plugin
BuildRequires: libpng-devel

%description plugin-fade-in
This package contains the "Fade-In" boot splash plugin for
Plymouth. It features a centered logo that fades in and out
while stars twinkle around the logo during system boot up.

%package plugin-pulser
Summary: Plymouth "Pulser" plugin
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}
Requires(post): %{_sbindir}/plymouth-set-default-plugin
BuildRequires: libpng-devel

%description plugin-pulser
This package contains the "Pulser" boot splash plugin for
Plymouth. It features a pulsing text progress indicator
centered in the screen during system boot up.

%package plugin-spinfinity
Summary: Plymouth "Spinfinity" plugin
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}
Requires: plymouth-plugin-label
BuildRequires: libpng-devel
Requires(post): %{_sbindir}/plymouth-set-default-plugin
Provides: system-plymouth-plugin = %{version}-%{release}

%description plugin-spinfinity
This package contains the "Spinfinity" boot splash plugin for
Plymouth. It features a centered logo and animated spinner that
spins in the shape of an infinity sign.

%package plugin-solar
Summary: Plymouth "Solar" plugin
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}
Requires: plymouth-plugin-label
Requires(post): %{_sbindir}/plymouth-set-default-plugin
BuildRequires: libpng-devel

%description plugin-solar
This package contains the "Solar" boot splash plugin for
Plymouth. It features a blue flamed sun with animated solar flares.

%package text-and-details-only
Summary: Plymouth base plugin set
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}
Provides: system-plymouth-plugin = %{version}-%{release}

%description text-and-details-only
This package enables users to remove the default graphical plugin
from their system.  This is useful for embedded devices or servers
where the graphical plugin's dependencies are undesirable.

%prep
%setup -q

%build
%configure --enable-tracing --disable-tests --without-boot-entry \
           --without-default-plugin                              \
           --with-logo=%{_datadir}/pixmaps/system-logo-white.png \
           --with-background-start-color-stop=0x0073B3           \
           --with-background-end-color-stop=0x00457E             \
           --with-background-color=0x3391cd                      \
           --enable-gdm-transition                               \
           --with-system-root-install                            \
           --with-rhgb-compat-link

make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} \;
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} \;

# Temporary symlink until rc.sysinit is fixed
(cd $RPM_BUILD_ROOT%{_bindir}; ln -s ../../bin/plymouth)

%clean
rm -rf $RPM_BUILD_ROOT

%postun
if [ $1 -eq 0 ]; then
    rm -f %{_libdir}/plymouth/default.so
fi

%post
if [ $1 -eq 1 ]; then
    %{_sbindir}/plymouth-set-default-plugin text
fi

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post plugin-spinfinity
if [ $1 -eq 1 ]; then
    %{_sbindir}/plymouth-set-default-plugin spinfinity
fi

%postun plugin-spinfinity
if [ $1 -eq 0 ]; then
    if [ "$(%{_sbindir}/plymouth-set-default-plugin)" == "spinfinity" ]; then
        %{_sbindir}/plymouth-set-default-plugin text
    fi
fi

%postun plugin-fade-in
if [ $1 -eq 0 ]; then
    if [ "$(%{_sbindir}/plymouth-set-default-plugin)" == "fade-in" ]; then
        %{_sbindir}/plymouth-set-default-plugin --reset
    fi
fi

%postun plugin-solar
if [ $1 -eq 0 ]; then
    if [ "$(%{_sbindir}/plymouth-set-default-plugin)" == "solar" ]; then
        %{_sbindir}/plymouth-set-default-plugin --reset
    fi
fi

%postun plugin-pulser
if [ $1 -eq 0 ]; then
    if [ "$(%{_sbindir}/plymouth-set-default-plugin)" == "pulser" ]; then
        %{_sbindir}/plymouth-set-default-plugin --reset
    fi
fi

%files
%defattr(-, root, root)
%doc AUTHORS NEWS README
%dir %{_datadir}/plymouth
%dir %{_libexecdir}/plymouth
%dir %{_libdir}/plymouth
%{plymouthdaemon_execdir}/plymouthd
%{plymouthclient_execdir}/plymouth
%{_bindir}/plymouth
%{_bindir}/rhgb-client
%{_libdir}/plymouth/details.so
%{_libdir}/plymouth/text.so
%{_localstatedir}/run/plymouth
%{_localstatedir}/spool/plymouth
%{_localstatedir}/lib/plymouth

%files devel
%defattr(-, root, root)
%{plymouth_libdir}/libply.so
%{_libdir}/libplybootsplash.so
%{_libdir}/pkgconfig/plymouth-1.pc
%{_includedir}/plymouth-1

%files libs
%defattr(-, root, root)
%{plymouth_libdir}/libply.so.*
%{_libdir}/libplybootsplash.so.*

%files scripts
%defattr(-, root, root)
%{_sbindir}/plymouth-set-default-plugin
%{_libexecdir}/plymouth/plymouth-update-initrd
%{_libexecdir}/plymouth/plymouth-populate-initrd

%files utils
%defattr(-, root, root)
%{_bindir}/plymouth-log-viewer

%files gdm-hooks
%defattr(-, root, root)
%{_datadir}/gdm/autostart/LoginWindow/plymouth-log-viewer.desktop

%files plugin-label
%defattr(-, root, root)
%{_libdir}/plymouth/label.so

%files plugin-fade-in
%defattr(-, root, root)
%dir %{_datadir}/plymouth/fade-in
%{_datadir}/plymouth/fade-in/bullet.png
%{_datadir}/plymouth/fade-in/entry.png
%{_datadir}/plymouth/fade-in/lock.png
%{_datadir}/plymouth/fade-in/star.png
%{_libdir}/plymouth/fade-in.so

%files plugin-pulser
%defattr(-, root, root)
%{_libdir}/plymouth/pulser.so

%files plugin-spinfinity
%defattr(-, root, root)
%dir %{_datadir}/plymouth/spinfinity
%{_datadir}/plymouth/spinfinity/box.png
%{_datadir}/plymouth/spinfinity/bullet.png
%{_datadir}/plymouth/spinfinity/entry.png
%{_datadir}/plymouth/spinfinity/lock.png
%{_datadir}/plymouth/spinfinity/throbber-[0-3][0-9].png
%{_libdir}/plymouth/spinfinity.so

%files plugin-solar
%defattr(-, root, root)
%dir %{_datadir}/plymouth/solar
%{_datadir}/plymouth/solar/*.png
%{_libdir}/plymouth/solar.so

%changelog
* Wed Oct 22 2008 Ray Strode <rstrode@redhat.com> 0.5.0-0.2008.10.21.2
- add text-and-details-only subpackage so davej can uninstall
  spinfinity, pango, cairo etc from his router.

* Tue Oct 21 2008 Ray Strode <rstrode@redhat.com> 0.5.0-0.2008.10.21.1
- Minor event loop changes
- drop upstream patches
- Charlie Brej fix for progress bar resetting when escape gets pressed

* Tue Oct 21 2008 Ray Strode <rstrode@redhat.com> 0.5.0-0.2008.10.17.4
- Don't make plymouth-libs require plymouth (more fun with 467356)

* Mon Oct 20 2008 Ray Strode <rstrode@redhat.com> 0.5.0-0.2008.10.17.3
- Add initscripts requires (bug 461322)

* Mon Oct 20 2008 Ray Strode <rstrode@redhat.com> 0.5.0-0.2008.10.17.2
- Put tty1 back in "cooked" mode when going into runlevel 3
  (bug 467207)

* Fri Oct 17 2008 Ray Strode <rstrode@redhat.com> 0.5.0-0.2008.10.17.1
- Clear screen in details plugin when it's done
- Make plymouth-update-initrd a small wrapper around mkinitrd instead
  of the broken monstrosity it was before.

* Fri Oct 17 2008 Ray Strode <rstrode@redhat.com> 0.5.0-0.2008.10.15.3
- Move plymouth-set-default-plugin, plymouth-update-initrd, and
  plymouth-populate-initrd to plymouth-scripts subpackage
  (the last fix didn't actually help with bug 467356)

* Fri Oct 17 2008 Ray Strode <rstrode@redhat.com> 0.5.0-0.2008.10.15.2
- Move plymouth-set-default-plugin to -libs (might help with bug 467356)
- Fix up requires, provides and postun scripts

* Wed Oct 15 2008 Ray Strode <rstrode@redhat.com> 0.5.0-0.2008.10.15.1
- Don't free windows on --hide-splash (fix from Jeremy)

* Tue Oct 14 2008 Ray Strode <rstrode@redhat.com> 0.5.0-0.2008.10.14.1
- Solar fixes from Charlie Brej
- Better cpu usage from Charlie

* Fri Oct 10 2008 Ray Strode <rstrode@redhat.com> 0.5.0-0.2008.10.08.2
- Add Requires(post): nash (bug 466500)

* Wed Oct 08 2008 Ray Strode <rstrode@redhat.com> 0.5.0-0.2008.10.08.1
- Rework how "console=" args done again, to hopefully fix
  bug 460565

* Mon Oct 06 2008 Ray Strode <rstrode@redhat.com> 0.5.0-0.2008.10.06.1
- Add "Solar" plugin from Charles Brej
- Move things around so computers with separate /usr boot
  (hopefully this won't break things, but it probably will)
- Make GDM show up on vt1 for all plugins

* Tue Sep 30 2008 Jeremy Katz <katzj@redhat.com> 0.5.0-0.2008.09.25.2
- Remove mkinitrd requires to break the dep loop and ensure things
  get installed in the right order

* Thu Sep 25 2008 Ray Strode <rstrode@redhat.com> 0.5.0-0.2008.09.25.1
- Add new snapshot to fold in Will Woods progress bar, and
  move ajax's splash upstream, putting the old text splash
  in a "pulser" subpackage

* Tue Sep 23 2008 Ray Strode <rstrode@redhat.com> 0.5.0-0.2008.09.23.1
- Last snapshot was broken

* Mon Sep 22 2008 Ray Strode <rstrode@redhat.com> 0.5.0-0.2008.09.22.1
- Update to latest snapshot to get better transition support

* Fri Sep 19 2008 Ray Strode <rstrode@redhat.com> 0.5.0-0.2008.09.15.2
- Turn on gdm trigger for transition

* Mon Sep 15 2008 Ray Strode <rstrode@redhat.com> 0.5.0-0.2008.09.15.1
- add quit command with --retain-splash option to client

* Wed Sep 10 2008 Ray Strode <rstrode@redhat.com> 0.5.0-0.2008.09.10.1
- Fix text rendering for certain machines

* Mon Sep  8 2008 Ray Strode <rstrode@redhat.com> 0.5.0-0.2008.09.05.4
- More serial console fixes (bug 460565 again)

* Fri Sep  5 2008 Bill Nottingham <notting@redhat.com> 0.6.0-0.2008.09.05.3
- make the text plugin use the system release info rather than a hardcoded 'Fedora 10'

* Fri Sep  5 2008 Ray Strode <rstrode@redhat.com> 0.5.0-0.2008.09.05.2
- Try to support multiple serial consoles better
  (bug 460565)

* Fri Sep  5 2008 Ray Strode <rstrode@redhat.com> 0.5.0-0.2008.09.05.1
- Fix some confusion with password handling in details plugin

* Wed Aug 27 2008 Ray Strode <rstrode@redhat.com> 0.5.0-0.2008.08.27.1
- Fix another crasher for users with encrypted disks (this time in
  the text plugin, not the client)

* Wed Aug 27 2008 Ray Strode <rstrode@redhat.com> 0.5.0-0.2008.08.27
- Update to latest snapshot
- Add the ability to show text prompts in graphical plugin
- Fix crasher for users with encrypted disks

* Fri Aug 23 2008 Ray Strode <rstrode@redhat.com> 0.5.0-0.2008.08.22
- Update to latest snapshot

* Wed Aug 13 2008 Ray Strode <rstrode@redhat.com> 0.5.0-20.2008.08.13
- Update previous patch to remove some assertions

* Wed Aug 13 2008 Ray Strode <rstrode@redhat.com> 0.5.0-19.2008.08.13
- add a patch that may help serial console users

* Wed Aug 13 2008 Ray Strode <rstrode@redhat.com> 0.5.0-18.2008.08.13
- add spool directory to file list

* Wed Aug 13 2008 Ray Strode <rstrode@redhat.com> 0.5.0-17.2008.08.13
- Make plymouth-gdm-hooks require plymouth-utils

* Wed Aug 13 2008 Ray Strode <rstrode@redhat.com> 0.5.0-16.2008.08.13
- Add a boot failure viewer to login screen (written by Matthias)

* Tue Aug 12 2008 Adam Jackson <ajax@redhat.com> 0.5.0-15.2008.08.08
- plymouth-0.5.0-textbar-hotness.patch: Change the text plugin to a slightly
  more traditional progress bar, to maintain the illusion of progress better
  than the eternally oscillating cylon. Note: still incomplete.

* Fri Aug  8 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-14.2008.08.08
- Don't require a modifiable text color map (may fix serial consoles)

* Thu Aug  7 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-13.2008.08.07
- Update to new snapshot which when combined with a new mkinitrd should
  make unlocking encrypted root partitions work again

* Wed Aug  6 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-12.2008.08.06
- Update to new snapshot which fixes some assertion failures in the
  client code

* Wed Aug  6 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-11.2008.08.01
- Add Requires(post): plymouth to plugins so they get plymouth-set-default-plugin (bug 458071)

* Tue Aug  5 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-10.2008.08.01
- Add plymouth dirs to file list (bug 457871)

* Fri Aug  1 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-9.2008.08.01
- new plymout-populate-initrd features don't work with the set -e at the
  top of it.

* Thu Jul 31 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-8.2008.08.01
- Update to another snapshot to actually get new
  plymouth-populate-initrd features

* Thu Jul 31 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-8.2008.07.31
- Update to snapshot to get new plymouth-populate-initrd features
- Make removing rhgb use details plugin instead of exiting

* Thu Jul 31 2008 Peter Jones <pjones@redhat.com> - 0.5.0-7
- Make it a mkinitrd requires instead of a nash requires (that will
  still pull in nash, but we need mkinitrd for newer plymouth-populate-initrd)

* Wed Jul 30 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-6
- Add nash requires

* Wed Jul  9 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-5
- Use a new heuristic for finding libdir, since the old
  one falls over on ia64

* Wed Jul  9 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-4
- add ctrl-r to rotate text color palette back to stock values

* Tue Jul  8 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-3
- Fix populate script on ppc (bug 454353)

* Tue Jul  1 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-2
- Pull in spinfinity by default.  This whole "figure out
  which plugin to use" set of scripts and scriptlets
  needs work.  We need to separate distro default from
  user choice.

* Thu Jul  1 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-1
- Add new client "ask-for-password" command which feeds
  the user input to a program instead of standard output,
  and loops when the program returns non-zero exit status.

* Thu Jun 26 2008 Ray Strode <rstrode@redhat.com> - 0.4.5-1
- Update to version 0.4.5
- Make text plugin blue and less 80s

* Wed Jun 25 2008 Ray Strode <rstrode@redhat.com> - 0.4.0-4
- Make "Password: " show up correctly in text plugin

* Wed Jun 25 2008 Ray Strode <rstrode@redhat.com> - 0.4.0-3
- Require elfutils (bug 452797)

* Sun Jun 22 2008 Ray Strode <rstrode@redhat.com> - 0.4.0-2
- Make plymouth-set-default-plugin --reset choose the latest
  installed plugin, not the earliest

* Sun Jun 22 2008 Ray Strode <rstrode@redhat.com> - 0.4.0-1
- Update to version 0.4.0
- Only run if rhgb is on kernel command line
- Make text plugin more animated

* Mon Jun 16 2008 Ray Strode <rstrode@redhat.com> - 0.3.2-2
- dont go back to text mode on exit

* Mon Jun 16 2008 Ray Strode <rstrode@redhat.com> - 0.3.2-1
- Update to version 0.3.2
- show gradient in spinfinity plugin
- Drop fade out in spinfinity plugin
- fix throbber placement
- rename graphical.so to default.so

* Thu Jun 12 2008 Ray Strode <rstrode@redhat.com> - 0.3.1-3
- scriplet should be preun, not postun

* Thu Jun 12 2008 Ray Strode <rstrode@redhat.com> - 0.3.1-2
- Fix postun scriptlet

* Thu Jun 12 2008 Ray Strode <rstrode@redhat.com> - 0.3.1-1
- Update to version 0.3.1
- Don't ship generated initrd scripts in tarball

* Thu Jun 12 2008 Ray Strode <rstrode@redhat.com> - 0.3.0-1
- Update to version 0.3.0
- Better plugin handling
- Better integration with mkinitrd (pending mkinitrd changes)
- random bug fixes

* Mon Jun  9 2008 Ray Strode <rstrode@redhat.com> - 0.2.0-1
- Update to version 0.2.0
- Integrate more tightly with nash (pending nash changes)
- ship libs for out of tree splash plugins
- gradient support
- random bug fixes

* Fri May 30 2008 Ray Strode <rstrode@redhat.com> - 0.1.0-1
- Initial import, version 0.1.0
