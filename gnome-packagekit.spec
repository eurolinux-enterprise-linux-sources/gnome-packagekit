Summary:   Session applications to manage packages
Name:      gnome-packagekit
Version:   3.14.3
Release:   7%{?dist}
License:   GPLv2+
Group:     Applications/System
URL:       http://www.packagekit.org
Source0:   http://download.gnome.org/sources/gnome-packagekit/3.14/%{name}-%{version}.tar.xz

# Upstream patch
Patch0:    0001-Avoid-registering-two-main-desktop-file-categories.patch

Patch5:    0001-Change-the-UI-policy-to-show-the-comps-tree.patch
Patch6:    0001-Use-the-pre-gnome-software-application-names.patch
Patch7:    gnome-packagekit-3.14.3-EL7.3_translations.patch

BuildRequires: glib2-devel >= 2.25.8
BuildRequires: gtk3-devel
BuildRequires: dbus-devel
BuildRequires: dbus-glib-devel
BuildRequires: libnotify-devel >= 0.7.0
BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: libtool
BuildRequires: cairo-devel
BuildRequires: startup-notification-devel
BuildRequires: perl(XML::Parser)
BuildRequires: PackageKit-devel >= 0.5.0
BuildRequires: intltool
BuildRequires: xorg-x11-proto-devel
BuildRequires: fontconfig-devel
BuildRequires: libcanberra-devel
BuildRequires: libgudev1-devel
BuildRequires: libxslt
BuildRequires: docbook-utils
BuildRequires: systemd-devel
BuildRequires: polkit-devel
BuildRequires: itstool

# the top level package depends on all the apps to make upgrades work
Requires: %{name}-installer
Requires: %{name}-updater

%description
gnome-packagekit provides session applications for the PackageKit API.
There are several utilities designed for installing, updating and
removing packages on your system.

%package common
Summary: Common files required for %{name}
Requires:  %{name}%{?_isa} = %{version}-%{release}
Requires:  adwaita-icon-theme
Requires:  dbus-x11%{?_isa} >= 1.1.2
Requires:  PackageKit%{?_isa} >= 0.5.0
Requires:  PackageKit-libs >= 0.5.0
Requires:  shared-mime-info
Requires:  iso-codes
Requires:  libcanberra%{?_isa} >= 0.10

# required because KPackageKit provides exactly the same interface
Provides: PackageKit-session-service

%description common
Files shared by all subpackages of %{name}

%package installer
Summary: PackageKit package installer
Requires: %{name}-common%{?_isa} = %{version}-%{release}

%description installer
A graphical package installer for PackageKit which is used to manage software
not shown in GNOME Software.

%package updater
Summary: PackageKit package updater
Requires: %{name}-common%{?_isa} = %{version}-%{release}

%description updater
A graphical package updater for PackageKit which is used to update packages
without rebooting.

%prep
%setup -q
%patch0 -p1 -b .desktop-file-category
%patch5 -p1 -b .category-groups
%patch6 -p1 -b .funky-name
%patch7 -p1 -b .funky-name-translations

%build
%configure --enable-systemd
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# nuke the ChangeLog file, it's huge
rm -f $RPM_BUILD_ROOT%{_datadir}/doc/gnome-packagekit-*/ChangeLog

# use gnome-software for installing local files
rm -f $RPM_BUILD_ROOT%{_datadir}/applications/gpk-install-local-file.desktop

%find_lang %name --with-gnome

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database %{_datadir}/applications &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi
update-desktop-database %{_datadir}/applications &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files
# nada

%files common -f %{name}.lang
%doc AUTHORS COPYING NEWS README
%{_bindir}/gpk-dbus-service
%{_bindir}/gpk-install-local-file
%{_bindir}/gpk-log
%{_bindir}/gpk-prefs
%dir %{_datadir}/gnome-packagekit
%{_datadir}/gnome-packagekit/gpk-client.ui
%{_datadir}/gnome-packagekit/gpk-error.ui
%{_datadir}/gnome-packagekit/gpk-eula.ui
%{_datadir}/gnome-packagekit/gpk-log.ui
%{_datadir}/gnome-packagekit/gpk-prefs.ui
%{_datadir}/gnome-packagekit/gpk-signature.ui
%dir %{_datadir}/gnome-packagekit/icons
%dir %{_datadir}/gnome-packagekit/icons/hicolor
%dir %{_datadir}/gnome-packagekit/icons/hicolor/*
%dir %{_datadir}/gnome-packagekit/icons/hicolor/*/*
%{_datadir}/gnome-packagekit/icons/hicolor/*/*/*.png
%{_datadir}/gnome-packagekit/icons/hicolor/scalable/*/*.svg*
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/icons/hicolor/scalable/*/*.svg*
%{_datadir}/man/man1/gpk-dbus-service.1.gz
%{_datadir}/man/man1/gpk-install-local-file.1.gz
%{_datadir}/man/man1/gpk-log.1.gz
%{_datadir}/man/man1/gpk-prefs.1.gz
%{_datadir}/applications/gpk-dbus-service.desktop
%{_datadir}/applications/gpk-log.desktop
%{_datadir}/applications/gpk-prefs.desktop
%{_datadir}/dbus-1/services/org.freedesktop.PackageKit.service
%{_datadir}/glib-2.0/schemas/org.gnome.packagekit.gschema.xml
%{_datadir}/GConf/gsettings/org.gnome.packagekit.gschema.migrate

%files installer
%defattr(-,root,root,-)
%{_bindir}/gpk-application
%{_datadir}/appdata/gpk-application.appdata.xml
%{_datadir}/applications/gpk-application.desktop
%{_datadir}/gnome-packagekit/gpk-application.ui
%{_datadir}/man/man1/gpk-application.1.gz

%files updater
%defattr(-,root,root,-)
%{_bindir}/gpk-update-viewer
%{_datadir}/appdata/gpk-update-viewer.appdata.xml
%{_datadir}/applications/gpk-update-viewer.desktop
%{_datadir}/gnome-packagekit/gpk-update-viewer.ui
%{_datadir}/man/man1/gpk-update-viewer.1.gz

%changelog
* Wed Jun 29 2016 Richard Hughes <rhughes@redhat.com> - 3.14.3-7
- Update translations.
- Resolves: #1304279

* Wed May 18 2016 Richard Hughes <rhughes@redhat.com> - 3.14.3-6
- Create a -common subpackage and make the "parent" package depend on all
  the split out applications. This fixes upgrades from old versions.
- Resolves: #1290868

* Fri Jul 17 2015 Kalev Lember <klember@redhat.com> - 3.14.3-5
- Avoid registering two main desktop file categories
- Resolves: #1226036

* Thu Jul 09 2015 Richard Hughes <rhughes@redhat.com> - 3.14.3-4
- Use a different application name in the menu.
- Resolves: #1174550

* Thu Jun 18 2015 Richard Hughes <rhughes@redhat.com> - 3.14.3-3
- Re-apply the fix "Change the UI policy to show the comps tree" as it was
  lost in the rebase process.
- Resolves: #1174550

* Thu Jun 18 2015 Richard Hughes <rhughes@redhat.com> - 3.14.3-2
- Rebuild against the new PackageKit to avoid installing the compat library.
- Resolves: #1174550

* Wed May 27 2015 Richard Hughes <rhughes@redhat.com> - 3.14.3-1
- Update to 3.14.3
- Resolves: #1174550

* Thu Mar 06 2014 Richard Hughes <rhughes@redhat.com> - 3.8.2-10
- Change the UI policy to show the comps tree
- Resolves: #959983

* Fri Feb 28 2014 Matthias Clasen <mclasen@redhat.com> - 3.8.2-9
- Rebuild
- Resolves: #1070810

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 3.8.2-8
- Mass rebuild 2014-01-24

* Mon Jan 13 2014 Richard Hughes <rhughes@redhat.com> - 3.8.2-7
- Don't hide titlebar when maximized
- Resolves: #1047486

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.8.2-6
- Mass rebuild 2013-12-27

* Thu Dec 12 2013 Matthias Clasen <mclasen@redhat.com> - 3.8.2-5
- Update translations
- Resolves: #1030344

* Mon Nov 25 2013 Richard Hughes <rhughes@redhat.com> - 3.8.2-4
- Don't show missing icons for comps groups
- Resolves: #959983

* Mon Nov 25 2013 Richard Hughes <rhughes@redhat.com> - 3.8.2-3
- Show the update and installer items in a KDE desktop as RHEL does not
  ship Apper.
- Resolves: #1033672

* Tue Jun 18 2013 Richard Hughes <rhughes@redhat.com> - 3.8.2-2
- Ignore package progress updates when the transaction is being simulated which
  fixes the 100% CPU issue when trying to update a large number of packages.
- Resolves: #969852

* Mon May 13 2013 Richard Hughes <rhughes@redhat.com> - 3.8.2-1
- Update to 3.8.2

* Mon Apr 15 2013 Richard Hughes <rhughes@redhat.com> - 3.8.1-1
- Update to 3.8.1

* Thu Apr 11 2013 Richard Hughes <rhughes@redhat.com> - 3.8.0-2
- Rebuild to hopefully pick up translations:
  https://bugzilla.gnome.org/show_bug.cgi?id=696976

* Tue Mar 26 2013 Richard Hughes <rhughes@redhat.com> - 3.8.0-1
- Update to 3.8.0

* Tue Mar 19 2013 Richard Hughes <rhughes@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Wed Feb 06 2013 Richard Hughes <rhughes@redhat.com> - 3.7.5-1
- Update to 3.7.5

* Wed Nov 28 2012 Richard Hughes <hughsient@gmail.com> - 3.6.1-2
- Don't crash if the window that invoked the task exits before
  the task starts up.
- Resolves: #756208

* Wed Nov 14 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.1-1
- Update to 3.6.1
- Minor spec file cleanup

* Fri Sep 28 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 3.6.0-2
- Depend on gnome-settings-daemon-updates. #699348
- Drop ancient obsoletes

* Tue Sep 25 2012 Matthias Clasen <mclasen@redhat.com> - 3.6.0-1
- Update to 3.6.0

* Tue Aug 28 2012 Richard Hughes <hughsient@gmail.com> - 3.5.90-1
- Update to 3.5.90

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 3.5.4-1
- Update to 3.5.4

* Tue Jun 26 2012 Richard Hughes <hughsient@gmail.com> - 3.5.3-1
- Update to 3.5.3

* Thu May 17 2012 Richard Hughes <hughsient@gmail.com> - 3.5.1-1
- Update to 3.5.1

* Mon Mar 26 2012 Richard Hughes <rhughes@redhat.com> - 3.4.0-1
- New upstream version.

* Sun Mar 18 2012 Richard Hughes <rhughes@redhat.com> - 3.3.92-1
- New upstream version.
- Many updated translations.

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.5-2
- Use systemd for session tracking

* Mon Feb 06 2012 Richard Hughes <rhughes@redhat.com> - 3.3.5-1
- New upstream version.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild
