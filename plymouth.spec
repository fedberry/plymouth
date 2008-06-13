Summary: Plymouth Graphical Boot Animation and Logger
Name: plymouth
Version: 0.3.1
Release: 3%{?dist}
License: GPLv2+
Group: System Environment/Base
Source0: http://freedesktop.org/software/plymouth/releases/%{name}-%{version}.tar.bz2
URL: http://freedesktop.org/software/plymouth/releases
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Obsoletes: rhgb < 1:10.0.0
Provides: rhgb = 1:10.0.0

Requires: system-logos >= 9.0.1

%description
Plymouth provides an attractive graphical boot animation in
place of the text messages that normally get shown.  Text
messages are instead redirected to a log file for viewing
after boot.

%package libs
Summary: Plymouth libraries
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

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

%package plugin-fade-in
Summary: Plymouth "Fade-In" plugin
Group: System Environment/Base
Requires: %name = %{version}-%{release}
BuildRequires: libpng-devel

%description plugin-fade-in
This package contains the "Fade-In" boot splash plugin for
Plymouth. It features a centered logo that fades in and out
while stars twinkle around the logo during system boot up.

%package plugin-spinfinity
Summary: Plymouth "Spinfinity" plugin
Group: System Environment/Base
Requires: %name = %{version}-%{release}
BuildRequires: libpng-devel

%description plugin-spinfinity
This package contains the "Spinfinity" boot splash plugin for
Plymouth. It features a centered logo and animated spinner that
spins in the shape of an infinity sign.

%prep
%setup -q

%build
%configure --enable-tracing --disable-tests --without-boot-entry \
           --without-default-plugin                              \
           --with-logo=%{_datadir}/pixmaps/system-logo-white.png \
           --with-background-start-color-stop=0x0073B3           \
           --with-background-end-color-stop=0x00457E

make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} \;
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%preun
if [ $1 -eq 1 ]; then
    %{_sbindir}/plymouth-set-default-plugin --reset
fi

%post plugin-spinfinity
if [ $1 -eq 1 ]; then
    %{_sbindir}/plymouth-set-default-plugin spinfinity
fi

%postun plugin-spinfinity
if [ $1 -eq 0 ]; then
    %{_sbindir}/plymouth-set-default-plugin --reset
fi

%post plugin-fade-in
if [ $1 -eq 1 ]; then
    %{_sbindir}/plymouth-set-default-plugin fade-in
fi

%postun plugin-fade-in
if [ $1 -eq 0 ]; then
    %{_sbindir}/plymouth-set-default-plugin --reset
fi

%files
%defattr(-, root, root)
%doc AUTHORS NEWS README
%dir %{_datadir}/plymouth
%{_libexecdir}/plymouth/plymouthd
%{_libexecdir}/plymouth/plymouth-update-initrd
%{_libexecdir}/plymouth/plymouth-populate-initrd
%{_sbindir}/plymouth-set-default-plugin
%{_bindir}/plymouth
%{_bindir}/rhgb-client
%{_libdir}/plymouth/details.so
%{_libdir}/plymouth/text.so
%{_localstatedir}/run/plymouth

%files devel
%defattr(-, root, root)
%{_libdir}/libply.so
%{_libdir}/libplybootsplash.so
%{_libdir}/pkgconfig/plymouth-1.pc
%{_includedir}/plymouth-1

%files libs
%defattr(-, root, root)
%{_libdir}/libply.so.*
%{_libdir}/libplybootsplash.so.*

%files plugin-fade-in
%defattr(-, root, root)
%dir %{_datadir}/plymouth/fade-in
%{_datadir}/plymouth/fade-in/bullet.png
%{_datadir}/plymouth/fade-in/entry.png
%{_datadir}/plymouth/fade-in/lock.png
%{_datadir}/plymouth/fade-in/star.png
%{_libdir}/plymouth/fade-in.so

%files plugin-spinfinity
%defattr(-, root, root)
%dir %{_datadir}/plymouth/spinfinity
%{_datadir}/plymouth/spinfinity/box.png
%{_datadir}/plymouth/spinfinity/bullet.png
%{_datadir}/plymouth/spinfinity/entry.png
%{_datadir}/plymouth/spinfinity/lock.png
%{_datadir}/plymouth/spinfinity/throbber-[0-3][0-9].png
%{_libdir}/plymouth/spinfinity.so

%changelog
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
