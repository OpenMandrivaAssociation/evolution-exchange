%define major_version 2.10
%define evolution_version 2.9.2
%define api_version 1.2

Name:		evolution-exchange
Summary:	Exchange Connector for Evolution
Version: 2.10.0
Release: %mkrel 1
License: 	GPL
Group:		Networking/Mail
Source0: 	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
URL: 		http://www.ximian.com/products/ximian_evolution/
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

# (fc) 0.8-5mdk implicit dependency is not enough
Requires: evolution >= %{evolution_version}
BuildRequires: evolution-devel >= %{evolution_version}
BuildRequires: evolution-data-server-devel >= 1.9.6
BuildRequires: db4.2-devel
BuildRequires: openldap-devel 
BuildRequires: krb5-devel
BuildRequires: libgnomeprintui-devel
BuildRequires: libgtkhtml-3.14-devel
BuildRequires: perl-XML-Parser
BuildRequires: automake1.9
BuildRequires: intltool
BuildRequires: gnome-common
BuildRequires: libmono-devel
Obsoletes: ximian-connector
Provides: ximian-connector

%description
This package is a connector to allow access to Exchange server 
for Evolution.

Currently, only Exchange 2000 and 2003 are supported.

%prep
%setup -q 

#fix build 
intltoolize --force
aclocal-1.9
automake-1.9
autoconf

%build

%configure2_5x --with-openldap=yes --with-static-ldap=no \
--with-krb5=%{_prefix} --with-krb5-libs=%{_libdir}

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
%post_install_gconf_schemas apps_exchange_addressbook-2.10

%preun
%preun_uninstall_gconf_schemas apps_exchange_addressbook-2.10

%files -f %{name}-%{major_version}.lang
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README
%_sysconfdir/gconf/schemas/apps_exchange_addressbook-2.10.schemas
%{_bindir}/*
%{_libdir}/bonobo/servers/*
%{_libexecdir}/evolution/%{major_version}/evolution-exchange-storage
%{_libdir}/evolution-data-server-%{api_version}/camel-providers/*.so
%{_libdir}/evolution-data-server-%{api_version}/camel-providers/*.urls
%{_datadir}/gtk-doc/html/ximian-connector
%{_datadir}/evolution-exchange

