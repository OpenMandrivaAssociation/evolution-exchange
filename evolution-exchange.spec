%define major_version 3.4
%define evolution_version 3.4.1
%define eds_version 3.4.1
%define api_version 1.2

%define build_mono 1
%ifarch %arm %mips
%define build_mono 0
%endif

Summary:	Exchange Connector for Evolution
Name:		evolution-exchange
Version:	3.4.4
Release:	1
License:	GPLv2
Group:		Networking/Mail
URL:		https://projects.gnome.org/evolution/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.xz

BuildRequires:	gnome-common
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	db53-devel
BuildRequires:	krb5-devel
BuildRequires:	openldap-devel 
BuildRequires:	pkgconfig(evolution-shell-3.0)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(gnome-desktop-3.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libedata-book-1.2)
BuildRequires:	pkgconfig(libebackend-1.2)
BuildRequires:	pkgconfig(libedata-cal-1.2)
BuildRequires:	pkgconfig(libedataserverui-3.0)
%if %{build_mono}
BuildRequires:	libmono-devel
%endif

# (fc) 0.8-5mdk implicit dependency is not enough
Requires: evolution >= %{evolution_version}

%description
This package is a connector to allow access to Exchange server 
for Evolution.

Currently, only Exchange 2000 and 2003 are supported.

%prep
%setup -q

%build
export CPPFLAGS="$CPPFLAGS -I%{_includedir}/libical"
%configure2_5x \
	--with-openldap=yes \
	--with-static-ldap=no \
	--enable-gtk-doc \
	--disable-static

%make

%install
%makeinstall_std

#remove unpackaged files
rm -f %{buildroot}%{_libdir}/evolution/%{major_version}/*.{a,la} \
 %{buildroot}%{_libdir}/evolution-data-server-%{api_version}/camel-providers/*.{a,la} \
 %{buildroot}%{_libdir}/evolution/%{major_version}/evolution-mail-importers/*.{a,la} \
 %{buildroot}%{_libdir}/evolution/%{major_version}/evolution-calendar-importers/*.{a,la}

%find_lang %{name}-%{major_version} --with-gnome

%preun
%preun_uninstall_gconf_schemas apps_exchange_addressbook-%{major_version}

%files -f %{name}-%{major_version}.lang
%doc AUTHORS COPYING ChangeLog NEWS README
%_sysconfdir/gconf/schemas/apps_exchange_addressbook-%{major_version}.schemas
%{_bindir}/*
%{_libdir}/evolution/%{major_version}/plugins/*org-gnome-exchange*
%{_libdir}/evolution-exchange/%{major_version}
%{_libdir}/evolution-data-server/addressbook-backends/libebookbackendexchange.so
%{_libdir}/evolution-data-server/calendar-backends/libecalbackendexchange.so
%{_libdir}/evolution-data-server/camel-providers/libcamelexchange.*
%{_datadir}/evolution-exchange
%{_datadir}/gtk-doc/html/%{name}
%{_datadir}/evolution/%{major_version}/errors/*.error

