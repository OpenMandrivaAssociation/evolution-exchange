%define major_version 2.26
%define evolution_version 2.23
%define api_version 1.2

# caused by e-d-s which can't be fixed for now
%define _disable_ld_no_undefined 1
%define _disable_ld_as_needed 1

Name:		evolution-exchange
Summary:	Exchange Connector for Evolution
Version: 2.25.92
Release: %mkrel 1
License: 	GPLv2
Group:		Networking/Mail
Source0: 	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
Patch: evolution-exchange-2.25.3-format-string.patch
URL: 		http://www.ximian.com/products/ximian_evolution/
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

# (fc) 0.8-5mdk implicit dependency is not enough
Requires: evolution >= %{evolution_version}
BuildRequires: evolution-devel >= %{evolution_version}
BuildRequires: evolution-data-server-devel >= 2.25.92
BuildRequires: gnome-pilot-devel
BuildRequires: db4-devel
BuildRequires: openldap-devel 
BuildRequires: krb5-devel
BuildRequires: automake1.9
BuildRequires: intltool
BuildRequires: gnome-common
BuildRequires: libmono-devel
BuildRequires: gtk-doc
#gw this is only required because it is in libgpilotd.la
BuildRequires: hal-devel
Obsoletes: ximian-connector
Provides: ximian-connector

%description
This package is a connector to allow access to Exchange server 
for Evolution.

Currently, only Exchange 2000 and 2003 are supported.

%prep
%setup -q 
%patch -p1

%build
export CPPFLAGS="$CPPFLAGS -I%_includedir/libical"
%configure2_5x --with-openldap=yes --with-static-ldap=no --enable-gtk-doc

%make

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%makeinstall_std


#remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/evolution/%{major_version}/*.{a,la} \
 $RPM_BUILD_ROOT%{_libdir}/evolution-data-server-%{api_version}/camel-providers/*.{a,la} \
 $RPM_BUILD_ROOT%{_libdir}/evolution/%{major_version}/evolution-mail-importers/*.{a,la} \
 $RPM_BUILD_ROOT%{_libdir}/evolution/%{major_version}/evolution-calendar-importers/*.{a,la}

%{find_lang} %{name}-%{major_version} --with-gnome

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%post
%post_install_gconf_schemas apps_exchange_addressbook-%major_version

%preun
%preun_uninstall_gconf_schemas apps_exchange_addressbook-%major_version

%files -f %{name}-%{major_version}.lang
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README
%_sysconfdir/gconf/schemas/apps_exchange_addressbook-%major_version.schemas
%{_bindir}/*
%{_libdir}/bonobo/servers/*
%{_libexecdir}/evolution/%{major_version}/evolution-exchange-storage
%{_libdir}/evolution-data-server-%{api_version}/camel-providers/*.so
%{_libdir}/evolution-data-server-%{api_version}/camel-providers/*.urls
%{_datadir}/evolution-exchange
%_datadir/gtk-doc/html/%name
