%define name seahorse-plugins
%define version 2.24.0
%define release %mkrel 3

%define epiphany 2.24
%define build_epiphany 1

Name:		%{name}
Summary:	Plugins and utilities for encryption in GNOME
Version:	%{version}
Release:	%{release}
License:	GPLv2+ and GFDL
Group:		Graphical desktop/GNOME
URL:		http://seahorse.sourceforge.net/
Source:		http://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.bz2
#gw from Fedora, start seahorse-agent from xinit
Source1:	seahorse-agent.sh
BuildRoot:	%{_tmppath}/%{name}-%{version}
BuildRequires:  libseahorse-devel
BuildRequires:  libgpgme-devel
BuildRequires:  gnome-keyring-devel
BuildRequires:  evolution-data-server-devel
BuildRequires:  gnome-panel-devel
BuildRequires:  gedit-devel
BuildRequires:  libnautilus-devel
BuildRequires:  gnome-doc-utils
BuildRequires:  intltool
BuildRequires:  gnome-common
Requires: seahorse >= 2.23.5
Requires(post): scrollkeeper shared-mime-info
Requires(postun):scrollkeeper shared-mime-info


%description
Seahorse is a GNOME2 frontend for the GNU Privacy Guard ecryption tool. It can 
be used for file encryption and decryption and for digitally signing files and 
for verifying those signatures. Key management options are also included.


%if %build_epiphany 
%package -n seahorse-epiphany
Group: Networking/WWW
Summary: Seahorse GnuPG plugin for Epiphany 
Requires: %name = %version
Requires: epiphany >= %epiphany
BuildRequires:  epiphany-devel >= %epiphany


%description -n seahorse-epiphany
Seahorse is a GNOME2 frontend for the GNU Privacy Guard ecryption tool. It can 
be used for file encryption and decryption and for digitally signing files and 
for verifying those signatures.

This package integrates Seahorse with the Epiphany web browser.
%endif




%prep

%setup -q

%build
export CPPFLAGS="$CPPFLAGS -DLIBCRYPTUI_API_SUBJECT_TO_CHANGE"
%configure2_5x --enable-fast-install --disable-update-mime-database
%make

%install
rm -rf $RPM_BUILD_ROOT seahorse*.lang

GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std _ENABLE_SK=false
rm -f %buildroot%_libdir/{gedit-2/plugins/libseahorse-pgp.a,nautilus/extensions-2.0/*.a}


%{find_lang} %name --with-gnome
%{find_lang} seahorse-applet --with-gnome
cat seahorse-applet.lang >> %name.lang
for omf in %buildroot%_datadir/omf/*/*-??*.omf;do 
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %name.lang
done

# gw conflict with seahorse
rm -f %buildroot%_datadir/icons/hicolor/48x48/apps/seahorse.png
rm -f %buildroot%_datadir/icons/hicolor/48x48/apps/seahorse-preferences.png

mkdir -p $RPM_BUILD_ROOT%_sysconfdir/X11/xinit.d/
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%_sysconfdir/X11/xinit.d/seahorse-agent.sh

 
%post
%if %mdkversion < 200900
%{update_menus}
%endif
%define schemas seahorse-plugins seahorse-gedit
%if %mdkversion < 200900
%post_install_gconf_schemas %schemas
%update_desktop_database
%update_icon_cache hicolor
%update_scrollkeeper
%update_mime_database
%endif

%preun
%preun_uninstall_gconf_schemas %schemas

%if %mdkversion < 200900
%postun
%{clean_menus} 
%clean_desktop_database
%clean_icon_cache hicolor
%clean_scrollkeeper
%clean_mime_database
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%files -f %name.lang
%defattr(-,root,root,0755)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README
%_sysconfdir/X11/xinit.d/seahorse-agent.sh
%{_sysconfdir}/gconf/schemas/seahorse-plugins.schemas
%{_sysconfdir}/gconf/schemas/seahorse-gedit.schemas
%_bindir/seahorse-agent
%_bindir/seahorse-preferences
%_bindir/seahorse-tool
%_libdir/bonobo/servers/GNOME_SeahorseApplet.server
%_libdir/gedit-2/plugins/libseahorse-pgp.*
%_libdir/gedit-2/plugins/seahorse-pgp.gedit-plugin
%_libdir/nautilus/extensions-2.0/libnautilus-seahorse.*
%_libexecdir/seahorse/seahorse-applet
%_datadir/applications/seahorse-pgp*
%_datadir/gnome-2.0/ui/GNOME_SeahorseApplet.xml
%_datadir/mime/packages/seahorse.xml
%_datadir/%name
%_mandir/man1/*
%_datadir/pixmaps/*
#%dir %{_datadir}/omf/seahorse-plugins/
%dir %{_datadir}/seahorse/
%dir %{_datadir}/seahorse/glade/
#%{_datadir}/omf/seahorse/seahorse-C.omf
%{_datadir}/seahorse/glade/*
%_datadir/icons/hicolor/*/apps/*

%if %build_epiphany
%files -n seahorse-epiphany
%defattr(-,root,root,0755)
%_libdir/epiphany/%epiphany/extensions/*
%endif
