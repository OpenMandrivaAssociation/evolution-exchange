%define major_version 3.4
%define evolution_version 3.4.1
%define eds_version 3.4.1
%define api_version 1.2

%define build_mono 1
%ifarch %arm %mips
%define build_mono 0
%endif

Name:		evolution-exchange
Summary:	Exchange Connector for Evolution
Version: 3.4.1
Release: 1
License: 	GPLv2
Group:		Networking/Mail
Source0: 	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.xz
URL: 		http://projects.gnome.org/evolution/
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
# (fc) 0.8-5mdk implicit dependency is not enough
Requires: evolution >= %{evolution_version}
BuildRequires: evolution-devel >= %{evolution_version}
BuildRequires: evolution-data-server-devel >= %eds_version
BuildRequires: libGConf2-devel GConf2
BuildRequires: db-devel
BuildRequires: openldap-devel 
BuildRequires: krb5-devel
BuildRequires: automake
BuildRequires: intltool
BuildRequires: gnome-common
%if %{build_mono}
BuildRequires: libmono-devel
%endif
BuildRequires: gtk-doc
#gw another .la dep 
BuildRequires: gnome-desktop-devel
Obsoletes: ximian-connector
Provides: ximian-connector

%description
This package is a connector to allow access to Exchange server 
for Evolution.

Currently, only Exchange 2000 and 2003 are supported.

%prep
%setup -q

%build
export CPPFLAGS="$CPPFLAGS -I%_includedir/libical"
%configure2_5x --with-openldap=yes --with-static-ldap=no --enable-gtk-doc --disable-static
%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std


#remove unpackaged files
rm -f %{buildroot}%{_libdir}/evolution/%{major_version}/*.{a,la} \
 %{buildroot}%{_libdir}/evolution-data-server-%{api_version}/camel-providers/*.{a,la} \
 %{buildroot}%{_libdir}/evolution/%{major_version}/evolution-mail-importers/*.{a,la} \
 %{buildroot}%{_libdir}/evolution/%{major_version}/evolution-calendar-importers/*.{a,la}

%{find_lang} %{name}-%{major_version} --with-gnome

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post
%post_install_gconf_schemas apps_exchange_addressbook-%{major_version}

%preun
%preun_uninstall_gconf_schemas apps_exchange_addressbook-%{major_version}

%files -f %{name}-%{major_version}.lang
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README
%_sysconfdir/gconf/schemas/apps_exchange_addressbook-%{major_version}.schemas
%{_bindir}/*
%{_libdir}/evolution-data-server-%{api_version}/camel-providers/*.so
%{_libdir}/evolution-data-server-%{api_version}/camel-providers/*.urls
%{_libdir}/evolution-data-server-%{api_version}/extensions/*
%_libdir/evolution/%major_version/plugins/*org-gnome-exchange*
%{_datadir}/evolution-exchange
%_datadir/gtk-doc/html/%name
%_datadir/evolution/%major_version/errors/*.error
