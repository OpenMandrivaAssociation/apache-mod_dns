#Module-Specific definitions
%define apache_version 2.2.6
%define mod_name mod_dns
%define mod_conf B24_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DNS Protocol module for Apache 2.x
Name:		apache-%{mod_name}
Version:	1.02
Release:	%mkrel 7
Group:		System/Servers
License:	Apache License
URL:		http://www.beamartyr.net/
Source0:	http://www.beamartyr.net/mod-dns-%{version}.tar.bz2
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= %{apache_version}
Requires(pre):	apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:	apache-devel >= %{apache_version}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
DNS Protocol module for Apache 2.x
 
%prep

%setup -q -n mod-dns

cp %{SOURCE1} %{mod_conf}

%build

%{_sbindir}/apxs -c mod_dns.c buckets.c errors.c protocol.c rr/*.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}

