%global plymouthdaemon_execdir %{_sbindir}
%global plymouthclient_execdir %{_bindir}
%global plymouth_libdir %{_libdir}
%global plymouth_initrd_file /boot/initrd-plymouth.img

# Set to 1 if building from snapshots.
%global snapshot_build 0

%if %{snapshot_build}
%global snapshot_date 20160620
%global snapshot_hash 0e65b86c
%global snapshot_rel  %{?snapshot_date}git%{?snapshot_hash}
%endif

Summary: Graphical Boot Animation and Logger
Name: plymouth
Version: 0.9.3
Release: 3%{?snapshot_rel}%{?dist}
License: GPLv2+
URL: http://www.freedesktop.org/wiki/Software/Plymouth
Group: System Environment/Base

Source0: http://freedesktop.org/software/plymouth/releases/%{name}-%{version}.tar.xz
Source1: boot-duration
Source2: charge.plymouth
Source3: plymouth-update-initrd
# Only allow framebuffer 0 to be used.
Patch0: 01-fb0-only.patch
Patch1: 02-update-script-colours.patch

BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(libudev)
BuildRequires: kernel-headers
BuildRequires: libpng-devel
BuildRequires: libxslt, docbook-style-xsl
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pango-devel >= 1.21.0
BuildRequires: cairo-devel

Requires(post): plymouth-scripts
Requires: initscripts >= 8.83-1

%description
Plymouth provides an attractive graphical boot animation in
place of the text messages that normally get shown.  Text
messages are instead redirected to a log file for viewing
after boot.

%package system-theme
Summary: Plymouth default theme
Group: System Environment/Base
Requires: plymouth(system-theme) = %{version}-%{release}

%description system-theme
This metapackage tracks the current distribution default theme.

%package core-libs
Summary: Plymouth core libraries
Group: Development/Libraries

%description core-libs
This package contains the libply and libply-splash-core libraries
used by Plymouth.

%package graphics-libs
Summary: Plymouth graphics libraries
Group: Development/Libraries
Requires: %{name}-core-libs = %{version}-%{release}
Requires: system-logos

%description graphics-libs
This package contains the libply-splash-graphics library
used by graphical Plymouth splashes.

%package devel
Summary: Libraries and headers for writing Plymouth splash plugins
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the libply and libplybootsplash libraries
and headers needed to develop 3rd party splash plugins for Plymouth.

%package scripts
Summary: Plymouth related scripts
Group: Applications/System
Requires: findutils, coreutils, gzip, cpio, dracut, plymouth

%description scripts
This package contains scripts that help integrate Plymouth with
the system.

%package plugin-label
Summary: Plymouth label plugin
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}
Requires: %{name}-graphics-libs = %{version}-%{release}

%description plugin-label
This package contains the label control plugin for
Plymouth. It provides the ability to render text on
graphical boot splashes using pango and cairo.

%package plugin-fade-throbber
Summary: Plymouth "Fade-Throbber" plugin
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}
Requires: %{name}-graphics-libs = %{version}-%{release}

%description plugin-fade-throbber
This package contains the "Fade-In" boot splash plugin for
Plymouth. It features a centered image that fades in and out
while other images pulsate around during system boot up.

%package theme-fade-in
Summary: Plymouth "Fade-In" theme
Group: System Environment/Base
Requires: %{name}-plugin-fade-throbber = %{version}-%{release}
Requires(post): plymouth-scripts

%description theme-fade-in
This package contains the "Fade-In" boot splash theme for
Plymouth. It features a centered logo that fades in and out
while stars twinkle around the logo during system boot up.

%package plugin-throbgress
Summary: Plymouth "Throbgress" plugin
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}
Requires: %{name}-graphics-libs = %{version}-%{release}
Requires: plymouth-plugin-label

%description plugin-throbgress
This package contains the "throbgress" boot splash plugin for
Plymouth. It features a centered logo and animated spinner that
spins repeatedly while a progress bar advances at the bottom of
the screen.

%package theme-spinfinity
Summary: Plymouth "Spinfinity" theme
Group: System Environment/Base
Requires: %{name}-plugin-throbgress = %{version}-%{release}
Requires(post): plymouth-scripts

%description theme-spinfinity
This package contains the "Spinfinity" boot splash theme for
Plymouth. It features a centered logo and animated spinner that
spins in the shape of an infinity sign.

%package plugin-space-flares
Summary: Plymouth "space-flares" plugin
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}
Requires: %{name}-graphics-libs = %{version}-%{release}
Requires: plymouth-plugin-label

%description plugin-space-flares
This package contains the "space-flares" boot splash plugin for
Plymouth. It features a corner image with animated flares.

%package theme-solar
Summary: Plymouth "Solar" theme
Group: System Environment/Base
Requires: %{name}-plugin-space-flares = %{version}-%{release}
Requires(post): plymouth-scripts

%description theme-solar
This package contains the "Solar" boot splash theme for
Plymouth. It features a blue flamed sun with animated solar flares.

%package plugin-two-step
Summary: Plymouth "two-step" plugin
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}
Requires: %{name}-graphics-libs = %{version}-%{release}
Requires: plymouth-plugin-label

%description plugin-two-step
This package contains the "two-step" boot splash plugin for
Plymouth. It features a two phased boot process that starts with
a progressing animation synced to boot time and finishes with a
short, fast one-shot animation.

%package theme-charge
Summary: Plymouth "Charge" plugin
Group: System Environment/Base
Requires: %{name}-plugin-two-step = %{version}-%{release}
Requires(post): plymouth-scripts
Provides: plymouth(system-theme) = %{version}-%{release}

%description theme-charge
This package contains the "charge" boot splash theme for
Plymouth. It features the shadowy hull of a Fedora logo charge up and
and finally burst into full form.

%package plugin-script
Summary: Plymouth "script" plugin
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}
Requires: %{name}-graphics-libs = %{version}-%{release}

%description plugin-script
This package contains the "script" boot splash plugin for
Plymouth. It features an extensible, scriptable boot splash
language that simplifies the process of designing custom
boot splash themes.

%package theme-script
Summary: Plymouth "Script" plugin
Group: System Environment/Base
Requires: %{name}-plugin-script = %{version}-%{release}
Requires(post): %{_sbindir}/plymouth-set-default-theme

%description theme-script
This package contains the "script" boot splash theme for
Plymouth. It it is a simple example theme the uses the "script"
plugin.

%package theme-spinner
Summary: Plymouth "Spinner" theme
Group: System Environment/Base
Requires: %{name}-plugin-two-step = %{version}-%{release}
Requires(post): plymouth-scripts

%description theme-spinner
This package contains the "spinner" boot splash theme for
Plymouth. It features a small spinner on a dark background.

%prep
%setup -q

%patch0 -p1
%patch1 -p1

# Change plymouth defaults
sed -i -e 's/spinner/charge/g' -e 's/ShowDelay=5/ShowDelay=0/g' \
-e 's/DeviceTimeout=5/DeviceTimeout=1/g' src/plymouthd.defaults

%build
%configure --enable-tracing --disable-tests\
           --with-logo=%{_datadir}/pixmaps/system-logo-white.png\
           --with-background-start-color-stop=0x000000\
           --with-background-end-color-stop=0x333333\
           --with-background-color=0x212121\
           --disable-gdm-transition\
           --enable-systemd-integration\
           --without-system-root-install\
           --without-log-viewer\
           --without-rhgb-compat-link\
           --disable-libkms

make

%install
make install DESTDIR=$RPM_BUILD_ROOT

# Glow isn't quite ready for primetime
rm -rf $RPM_BUILD_ROOT%{_datadir}/plymouth/glow/
rm -f $RPM_BUILD_ROOT%{_libdir}/plymouth/glow.so

find $RPM_BUILD_ROOT -name '*.a' -delete
find $RPM_BUILD_ROOT -name '*.la' -delete

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/plymouth
cp $RPM_SOURCE_DIR/boot-duration $RPM_BUILD_ROOT%{_datadir}/plymouth/default-boot-duration
cp -f $RPM_SOURCE_DIR/plymouth-update-initrd $RPM_BUILD_ROOT%{_libexecdir}/plymouth

# Add charge, our new default
mkdir -p $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge
cp %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge
cp $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/glow/{box,bullet,entry,lock}.png $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge

# Drop glow, it's not very Fedora-y
rm -rf $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/glow


%postun
if [ $1 -eq 0 ]; then
    rm -f %{_libdir}/plymouth/default.so
    rm -f /boot/initrd-plymouth.img
fi

%ldconfig_scriptlets core-libs

%ldconfig_scriptlets graphics-libs

%postun theme-spinfinity
export LIB=%{_lib}
if [ $1 -eq 0 ]; then
    if [ "$(%{_sbindir}/plymouth-set-default-theme)" == "spinfinity" ]; then
        %{_sbindir}/plymouth-set-default-theme text
    fi
fi

%postun theme-fade-in
export LIB=%{_lib}
if [ $1 -eq 0 ]; then
    if [ "$(%{_sbindir}/plymouth-set-default-theme)" == "fade-in" ]; then
        %{_sbindir}/plymouth-set-default-theme --reset
    fi
fi

%postun theme-spinner
export LIB=%{_lib}
if [ $1 -eq 0 ]; then
    if [ "$(%{_sbindir}/plymouth-set-default-theme)" == "spinner" ]; then
        %{_sbindir}/plymouth-set-default-theme --reset
    fi
fi

%postun theme-solar
export LIB=%{_lib}
if [ $1 -eq 0 ]; then
    if [ "$(%{_sbindir}/plymouth-set-default-theme)" == "solar" ]; then
        %{_sbindir}/plymouth-set-default-theme --reset
    fi
fi

%post theme-charge
export LIB=%{_lib}
if [ $1 -eq 1 ]; then
    %{_sbindir}/plymouth-set-default-theme charge
else
    if [ "$(%{_sbindir}/plymouth-set-default-theme)" == "solar" ]; then
        %{_sbindir}/plymouth-set-default-theme charge
    fi
fi

%postun theme-charge
export LIB=%{_lib}
if [ $1 -eq 0 ]; then
    if [ "$(%{_sbindir}/plymouth-set-default-theme)" == "charge" ]; then
        %{_sbindir}/plymouth-set-default-theme --reset
    fi
fi

%files
%license COPYING
%doc AUTHORS README
%dir %{_datadir}/plymouth
%dir %{_datadir}/plymouth/themes
%dir %{_datadir}/plymouth/themes/details
%dir %{_datadir}/plymouth/themes/text
%dir %{_libexecdir}/plymouth
%dir %{_localstatedir}/lib/plymouth
%dir %{_libdir}/plymouth/renderers
%dir %{_sysconfdir}/plymouth
%config(noreplace) %{_sysconfdir}/plymouth/plymouthd.conf
%{plymouthdaemon_execdir}/plymouthd
%{plymouthclient_execdir}/plymouth
%{_bindir}/plymouth
%{_libdir}/plymouth/details.so
%{_libdir}/plymouth/text.so
%{_libdir}/plymouth/tribar.so
%{_libdir}/plymouth/renderers/frame-buffer*
%{_datadir}/plymouth/default-boot-duration
%{_datadir}/plymouth/themes/details/details.plymouth
%{_datadir}/plymouth/themes/text/text.plymouth
%{_datadir}/plymouth/themes/tribar/tribar.plymouth
%{_datadir}/plymouth/plymouthd.defaults
%{_localstatedir}/run/plymouth
%{_localstatedir}/spool/plymouth
%{_mandir}/man?/*
%{_prefix}/lib/systemd/system/*
%{_prefix}/lib/systemd/system/

%files devel
%{plymouth_libdir}/libply.so
%{plymouth_libdir}/libply-splash-core.so
%{_libdir}/libply-boot-client.so
%{_libdir}/libply-splash-graphics.so
%{_libdir}/pkgconfig/ply-splash-core.pc
%{_libdir}/pkgconfig/ply-splash-graphics.pc
%{_libdir}/pkgconfig/ply-boot-client.pc
%{_libdir}/plymouth/renderers/x11*
%{_includedir}/plymouth-1

%files core-libs
%{plymouth_libdir}/libply.so.*
%{plymouth_libdir}/libply-splash-core.so.*
%{_libdir}/libply-boot-client.so.*
%dir %{_libdir}/plymouth

%files graphics-libs
%{_libdir}/plymouth/renderers/drm*
%{_libdir}/libply-splash-graphics.so.*

%files scripts
%{_sbindir}/plymouth-set-default-theme
%{_libexecdir}/plymouth/plymouth-update-initrd
%{_libexecdir}/plymouth/plymouth-generate-initrd
%{_libexecdir}/plymouth/plymouth-populate-initrd

%files plugin-label
%{_libdir}/plymouth/label.so

%files plugin-fade-throbber
%{_libdir}/plymouth/fade-throbber.so

%files theme-fade-in
%dir %{_datadir}/plymouth/themes/fade-in
%{_datadir}/plymouth/themes/fade-in/bullet.png
%{_datadir}/plymouth/themes/fade-in/entry.png
%{_datadir}/plymouth/themes/fade-in/lock.png
%{_datadir}/plymouth/themes/fade-in/star.png
%{_datadir}/plymouth/themes/fade-in/fade-in.plymouth

%files theme-spinner
%dir %{_datadir}/plymouth/themes/spinner
%{_datadir}/plymouth/themes/spinner/*.png
%{_datadir}/plymouth/themes/spinner/spinner.plymouth

%files plugin-throbgress
%{_libdir}/plymouth/throbgress.so

%files theme-spinfinity
%dir %{_datadir}/plymouth/themes/spinfinity
%{_datadir}/plymouth/themes/spinfinity/box.png
%{_datadir}/plymouth/themes/spinfinity/bullet.png
%{_datadir}/plymouth/themes/spinfinity/entry.png
%{_datadir}/plymouth/themes/spinfinity/lock.png
%{_datadir}/plymouth/themes/spinfinity/throbber-[0-3][0-9].png
%{_datadir}/plymouth/themes/spinfinity/spinfinity.plymouth

%files plugin-space-flares
%{_libdir}/plymouth/space-flares.so

%files theme-solar
%dir %{_datadir}/plymouth/themes/solar
%{_datadir}/plymouth/themes/solar/*.png
%{_datadir}/plymouth/themes/solar/solar.plymouth

%files plugin-two-step
%{_libdir}/plymouth/two-step.so

%files theme-charge
%dir %{_datadir}/plymouth/themes/charge
%{_datadir}/plymouth/themes/charge/*.png
%{_datadir}/plymouth/themes/charge/charge.plymouth

%files plugin-script
%{_libdir}/plymouth/script.so

%files theme-script
%dir %{_datadir}/plymouth/themes/script
%{_datadir}/plymouth/themes/script/*.png
%{_datadir}/plymouth/themes/script/script.script
%{_datadir}/plymouth/themes/script/script.plymouth

%files system-theme

%changelog
* Sun Dec 03 2017 Vaughan Agrez <devel@agrez.net> - 0.9.3-3
- New release - 0.9.3
- Update spec & bump release

* Sun Apr 09 2017 Vaughan Agrez <devel@agrez.net> - 0.9.3-0.8.git
- Only allow framebuffer 0 to be used (Patch0)
- Update plymouthd.defaults
- Disable plymouth-update-initrd (we don't use an initrd)
- Modify charge theme for use with FedBerry
- Change background colours
- Update 'script' theme colours (Patch1)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-0.7.20160620git0e65b86c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jun 20 2016 Ray Strode <rstrode@redhat.com> - 0.9.3-0.6.git
- Fix color palette issue
- Fix splash at shutdown (if shutdown takes longer than 5 secs)
- Make sure text based splashes update terminal size when fbcon loads

* Thu Jun 16 2016 Ray Strode <rstrode@redhat.com> - 0.9.3-0.5.git
- really (?) fix password prompt on text plugin
  Resolves: #1344141

* Tue Jun 14 2016 Ray Strode <rstrode@redhat.com> - 0.9.3-0.4.git
- fix password prompt on text plugin
  Resolves: #1344141

* Wed Jun 08 2016 Ray Strode <rstrode@redhat.com> - 0.9.3-0.3.git
- new release versioning scheme to be more guideliney

* Tue Jun 07 2016 Ray Strode <rstrode@redhat.com> - 0.9.3-0.1.
- Update to latest git snapshot
- Fixes use after free
  Related: #1342673

* Tue May 24 2016 Ray Strode <rstrode@redhat.com> - 0.9.3-0.1.20160524
- Update to latest git snapshot
- Drop plymouth-generate-initrd scriptlets

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.9-17.2013.08.14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Nov 15 2015 Ray Strode <rstrode@redhat.com> 0.8.9-16.2013.08.14
- Fix plymouth-update-initrd script

* Mon Oct 26 2015 Ray Strode <rstrode@redhat.com> 0.8.9-15.2013.08.15
- Fix updates with script and spinner themes
  Resolves: #1267949

* Mon Aug 24 2015 Kalev Lember <klember@redhat.com> 0.8.9-13.2013.08.14
- Fix a typo in Requires

* Mon Aug 24 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.9-12.2013.08.14
- Fix Requires for various libs subpackages

* Sun Aug 23 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.9-11.2013.08.14
- Use %%license
- Cleanup spec
- Move drm render driver to graphics-libs sub package

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.9-10.2013.08.14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 20 2015 Will Woods <wwoods@redhat.com> 0.8.9-9.2013.08.14
- Fix theme override using PLYMOUTH_THEME_NAME (#1223344)

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.8.9-8.2013.08.14
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.9-7.2013.08.14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.9-6.2013.08.14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 31 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.9-4.2013.08.15
- Move system-logos dep to graphics-libs (no use on text/serial console minimal installs)

* Thu Feb 20 2014 Ray Strode <rstrode@redhat.com> 0.8.9-4.2013.08.14
- Fix splash after change in /sys/class/tty/console/active

* Thu Oct 31 2013 Ray Strode <rstrode@redhat.com> 0.8.9-3.2013.08.14
- Don't timeout plymouth quit waiting
  Related: #967521

* Wed Oct 16 2013 Ray Strode <rstrode@redhat.com> 0.8.9-2.2013.08.14
- Drop rhgb-client compat link

* Sun Oct 06 2013 Kalev Lember <kalevlember@gmail.com> - 0.8.9-1.2013.08.14
- Make sure the release number compares higher than the previous builds

* Wed Aug 14 2013 Ray Strode <rstrode@redhat.com> 0.8.9-0.1.2013.08.14.0
- Update to snapshot to fix system units

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.9-0.2014.03.26.0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Ray Strode <rstrode@redhat.com> 0.8.9-0.2013.03.26.0
- Update to snapshot to fix systemd vconsole issue

* Thu Feb 21 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.8-6
- Merge newer F18 release into rawhide

* Thu Dec 13 2012 Ray Strode <rstrode@redhat.com> 0.8.8-5
- Ensure fedup gets right splash screen
  Related: #879295

* Thu Nov 15 2012 Ray Strode <rstrode@redhat.com> 0.8.8-4
- Drop set-default-plugin compat script
- Just use upstream update-initrd

* Fri Nov 02 2012 Ray Strode <rstrode@redhat.com> 0.8.8-3
- More boot blocking fixes
  Related: #870695

* Thu Nov 01 2012 Ray Strode <rstrode@redhat.com> 0.8.8-2
- Fix crash when deactivating multiple times
  Related: #870695

* Fri Oct 26 2012 Ray Strode <rstrode@redhat.com> 0.8.8-1
- Latest upstream release
- includes systemd fixes and system update fixes

* Tue Aug 21 2012 Ray Strode <rstrode@redhat.com> 0.8.7-1
- Latest upstream release
- includes systemd fixes

* Tue Aug 21 2012 Dave Airlie <airlied@redhat.com> 0.8.6.2-1.2012.07.23
- fix plymouth race at bootup breaking efi/vesa handoff.
- fix version number - its against fedora package policy to have 0.year

* Mon Jul 23 2012 Ray Strode <rstrode@redhat.com> 0.8.6.2-0.2012.07.23
- One more crack at #830482 (will probably need additional fixes tomorrow)

* Mon Jul 23 2012 Tom Callaway <spot@fedoraproject.org> - 0.8.6.1-3
- fix bz704658 (thanks to Ian Pilcher for the patch), resolves issue where spinfinity theme
  never goes idle and thus, never exits to gdm

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Ray Strode <rstrode@redhat.com> 0.8.6.1-1
- Update to 0.8.6.1 since I mucked up 0.8.6
  Resolves: #830482

* Mon Jul 09 2012 Ray Strode <rstrode@redhat.com> 0.8.6-1
- Update to 0.8.6
- Fixes encrypted fs bug
  Resolves: #830482
- Adds support for offline package updates

* Mon Jun 25 2012 Adam Jackson <ajax@redhat.com> 0.8.5.1-3
- Rebuild without libkms

* Wed Jun 06 2012 Ray Strode <rstrode@redhat.com> 0.8.5.1-2
- Add %%{_prefix} to systemd service path

* Wed Jun 06 2012 Ray Strode <rstrode@redhat.com> 0.8.5.1-1
- Update to latest release
- Ship systemd service files
- Conflict with old systemd

* Tue Apr 24 2012 Richard Hughes <rhughes@redhat.com> 0.8.4-0.20120319.3
- Disable the nouveau driver as I've broken it with the new libdrm ABI

* Tue Mar 20 2012 Daniel Drake <dsd@laptop.org> 0.8.4-0.20120319.1
- Don't try to build against libdrm_intel on non-intel architectures

* Mon Mar 19 2012 Ray Strode <rstrode@redhat.com> 0.8.4-0.20120319.1
- Update to latest snapshot

* Mon Mar 12 2012 Ray Strode <rstrode@redhat.com> 0.8.4-0.20110810.6
- Don't require libdrm_intel on non intel arches

* Mon Feb 20 2012 Adam Williamson <awilliam@redhat.com> 0.8.4-0.20110810.5
- make plymouth-scripts require plymouth (RH #794894)

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 0.8.4-0.20110810.4
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.4-0.20110810.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 15 2011 Ray Strode <rstrode@redhat.com> 0.8.4-0.20110809.3
- Change spec based on suggestion from Nicolas Chauvet <kwizart@gmail.com>
  to fix scriptlet error during livecd creation
  Resolves: #666419

* Tue Nov 08 2011 Adam Jackson <ajax@redhat.com> 0.8.4-0.20110822.3
- Rebuild for libpng 1.5

* Fri Sep 02 2011 Ray Strode <rstrode@redhat.com> 0.8.4-0.20110822.2
- Make plymouth background dark gray at the request of Mo / design
  team.

* Mon Aug 22 2011 Ray Strode <rstrode@redhat.com> 0.8.4-0.20110822.1
- Update to latest git snapshot
- Reintroduce accidentally dropped spinner theme and systemd integration

* Tue Aug 09 2011 Ray Strode <rstrode@redhat.com> 0.8.4-0.20110809.1
- Rebuild

* Fri Mar 04 2011 Ray Strode <rstrode@redhat.com> 0.8.4-0.1.20110304.1
- retry reopening tty if we get EIO
  Hopefully Resolves: #681167

* Fri Feb 18 2011 Ray Strode <rstrode@redhat.com> 0.8.4-0.20110419.1
- unlock tty when reopening in case it spontaenously goes bonkers
  and we need to fix it up
  Resolves: #655538

* Wed Feb 09 2011 Christopher Aillon <caillon@redhat.com> 0.8.4-0.20110209.2
- Fix up obsoletes typo

* Wed Feb 09 2011 Ray Strode <rstrode@redhat.com> 0.8.4-0.20110209.1
- Update to latest snapshot

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.4-0.20101120.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Ray Strode <rstrode@redhat.com> 0.8.4-0.20101119.4
- Drop log viewer

* Sat Jan 29 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.8.4-0.20101119.3
- Dir ownership fixes (#645044).

* Fri Nov 19 2010 Ray Strode <rstrode@redhat.com> 0.8.4-0.20101119.2
- Fix serial console issue eparis was seeing

* Fri Nov 19 2010 Ray Strode <rstrode@redhat.com> 0.8.4-0.20101119.1
- Update to recent snapshot

* Tue Nov 02 2010 Ray Strode <rstrode@redhat.com> 0.8.4-0.20101002.1
- Update to recent snapshot

* Wed Sep 01 2010 Ray Strode <rstrode@redhat.com> 0.8.4-0.20100823.4
- Add more Requirse

* Thu Aug 26 2010 Ray Strode <rstrode@redhat.com> 0.8.4-0.20100823.3
- Add more Requires

* Thu Aug 26 2010 Ray Strode <rstrode@redhat.com> 0.8.4-0.20100823.2
- Fix plymouth-update-initrd
  It's regressed to the pre-dracut version.  This commit fixes that.

* Mon Aug 23 2010 Ray Strode <rstrode@redhat.com> 0.8.4-0.20100823.1
- Update to newer pre-release snapshot of 0.8.4
- Generate separate initrd in /boot

* Sat Aug 21 2010 Ray Strode <rstrode@redhat.com> 0.8.4-0.20100821.1
- Update to newer pre-release snapshot of 0.8.4
- Fix bizarre-o animation during boot up.

* Fri Jul 23 2010 Ray Strode <rstrode@redhat.com> 0.8.4-0.20100723.1
- Update to pre-release snapshot of 0.8.4

* Thu Jan 14 2010 Ray Strode <rstrode@redhat.com> 0.8.0-0.20100114.2
- Don't link plymouthd against libpng either

* Thu Jan 14 2010 Ray Strode <rstrode@redhat.com> 0.8.0-0.20100114.1
- Make it possible to do a basic plymouth installations without
  libpng

* Thu Jan 07 2010 Ray Strode <rstrode@redhat.com> 0.8.0-0.2009129.2
- Drop nash dep
