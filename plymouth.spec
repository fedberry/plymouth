Summary: Plymouth Graphical Boot Animation and Logger
Name: plymouth
Version: 0.1.0
Release: 1%{?dist}
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
           --with-logo=%{_datadir}/pixmaps/system-logo-white.png \
           --with-background-color=0x005391

make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} \;
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} \;

rm -f $RPM_BUILD_ROOT%{_libdir}/libply.so

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc AUTHORS NEWS README
%dir %{_datadir}/plymouth
%{_libexecdir}/plymouth/plymouthd
%{_libexecdir}/plymouth/plymouth-update-initrd
%{_libdir}/libply.so.*
%{_bindir}/plymouth
%{_bindir}/rhgb-client
%{_libdir}/plymouth/details.so
%{_libdir}/plymouth/text.so
%{_localstatedir}/run/plymouth

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
* Fri May 30 2008 Ray Strode <rstrode@redhat.com> - 0.1.0-1
- Initial import, version 0.1.0
