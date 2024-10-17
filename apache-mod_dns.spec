#Module-Specific definitions
%define apache_version 2.2.6
%define mod_name mod_dns
%define mod_conf B24_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DNS Protocol module for Apache 2.x
Name:		apache-%{mod_name}
Version:	1.02
Release:	12
Group:		System/Servers
License:	Apache License
URL:		https://www.beamartyr.net/
Source0:	http://www.beamartyr.net/mod-dns-%{version}.tar.bz2
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= %{apache_version}
Requires(pre):	apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:	apache-devel >= %{apache_version}

%description
DNS Protocol module for Apache 2.x
 
%prep

%setup -q -n mod-dns

cp %{SOURCE1} %{mod_conf}

%build

%{_bindir}/apxs -c mod_dns.c buckets.c errors.c protocol.c rr/*.c

%install

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%postun
if [ "$1" = "0" ]; then
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%clean

%files
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}



%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1.02-10mdv2012.0
+ Revision: 772618
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.02-9
+ Revision: 678304
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.02-8mdv2011.0
+ Revision: 587962
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1.02-7mdv2010.1
+ Revision: 516090
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.02-6mdv2010.0
+ Revision: 406574
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1.02-5mdv2009.1
+ Revision: 325693
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1.02-4mdv2009.0
+ Revision: 234930
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.02-3mdv2009.0
+ Revision: 215569
- fix rebuild
- fix buildroot

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 1.02-2mdv2008.1
+ Revision: 181718
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Nov 14 2007 Oden Eriksson <oeriksson@mandriva.com> 1.02-1mdv2008.1
+ Revision: 108778
- import apache-mod_dns


* Wed Nov 14 2007 Oden Eriksson <oeriksson@mandriva.com> 1.02-1mdv2008.1
- initial Mandriva package
