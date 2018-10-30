%define Werror_cflags %nil

Name:       virtuoso-opensource
Version:    7.2.4.2
Release:    3
License:    GPLv2
Summary:    OpenLink Virtuoso Database System Open-Source Edition
Group:      Development/Databases
Source0:    http://downloads.sourceforge.net/project/virtuoso/virtuoso/%{version}/%{name}-%{version}.tar.gz
# https://github.com/openlink/virtuoso-opensource/pull/583
Patch0:     https://github.com/openlink/virtuoso-opensource/commit/e563d45e839d9b11565d28e8b605272f6dbf385c.patch
Patch1:     virtuoso-7.2.4.2-clang-bug-33589.patch
Patch2:     virtuoso-7.2.4.2-openssl-1.1-part2.patch
Patch4:     virtuoso-opensource-6.1.0-extern-iodbc.patch
Url:        http://virtuoso.openlinksw.com/
BuildRequires: openssl
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: bison
BuildRequires: flex
BuildRequires: gperf
BuildRequires: libxml2-devel
BuildRequires: openssl-devel
BuildRequires: iodbc-devel
# temporary solution until
# libtiprc not fixed
%ifarch	%armx mips
BuildRequires: tirpc-devel
%endif
Obsoletes:     %name-conductor < 6.1.0
Conflicts:     %name-applications < 6.1.0-3
# Virtuoso 7.x is 64bit only. For 32bit platforms, use 6.x
ExclusiveArch:	x86_64 aarch64

%description
Virtuoso is a scalable cross-platform server that combines SQL/RDF/XML
Data Management with Web Application Server and Web Services Platform
functionality.

Virtuoso is at the core a high performance object-relational SQL
database. As a database, it provides transactions, a smart SQL
compiler, powerful stored procedure language with optional Java and
.Net server side hosting, hot backup, SQL 99 and more. It has all
major data access interfaces, as in ODBC, JDBC, ADO .Net and OLE/DB.

Virtuoso has a built-in web server which can serve dynamic web pages
written in Virtuoso's web page language as well as PHP, ASP .Net and
others. This same web server provides SOAP and REST access to Virtuoso
stored procedures, supporting a broad set of WS protocols such as
WS-Security, WS-Reliable Messaging and others. A BPEL4WS run time is
also available as part of Virtuoso's SOA suite.

%files -n %name
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_bindir}/virtuoso-t
%{_sysconfdir}/virtuoso/virtuoso.ini
%{_var}/lib/virtuoso
%attr(0755,root,root) %{_libdir}/virtuoso/plugins/virtodbc*.*
#attr(0755,root,root) %{_libdir}/virtuoso/hosting/im.so

#--------------------------------------------------------------------

%package -n  %name-applications
Summary:     Virtuoso open source applications
Group:       Development/Databases
Conflicts:   %name < 6.1.0-2

%description -n %name-applications
Virtuoso is a scalable cross-platform server that combines SQL/RDF/XML
Data Management with Web Application Server and Web Services Platform
functionality.

%files -n %name-applications
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_bindir}/inifile
%attr(0755,root,root) %{_bindir}/isql-iodbc
%attr(0755,root,root) %{_bindir}/isqlw
%attr(0755,root,root) %{_bindir}/isqlw-iodbc
%attr(0755,root,root) %{_bindir}/odbc_mail
%attr(0755,root,root) %{_bindir}/virt_mail
%{_datadir}/virtuoso/doc
%exclude %{_libdir}/virtuoso/plugins/virtodbc*.*

#--------------------------------------------------------------------

%package -n %name-jars
Summary: Virtuoso open source jar files
Group: Development/Databases

%description -n %name-jars
Virtuoso is a scalable cross-platform server that combines SQL/RDF/XML
Data Management with Web Application Server and Web Services Platform
functionality.

%files -n %name-jars
%defattr(0644,root,root,0755)
%{_libdir}/virtuoso/jars/jdbc2.0/*.jar
%{_libdir}/virtuoso/jars/jdbc3.0/*.jar
%{_libdir}/virtuoso/jars/jdbc4.0/*.jar
%{_libdir}/virtuoso/jars/jdbc4.1/*.jar
%{_libdir}/virtuoso/jars/jdbc4.2/*.jar
%{_libdir}/virtuoso/jars/jena/*.jar
%{_libdir}/virtuoso/jars/jena2/*.jar
%{_libdir}/virtuoso/jars/jena3/*.jar
%{_libdir}/virtuoso/jars/sesame/*
%{_libdir}/hibernate/virt_dialect.jar

#--------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}
%apply_patches

%build
# autogen.sh because of patching Makefile.am and configure to unixODBC
./autogen.sh

%configure2_5x \
	--with-iodbc=%_prefix --disable-all-vads 

%ifarch %{ix86} x86_64
%make
%endif
%ifarch %armx %mips
%make LIBS="-ltirpc -lz -lm"
%endif


%install
%makeinstall_std 
mkdir -p %{buildroot}%{_libdir}/virtuoso/plugins
#cp -f %{buildroot}%{_libdir}/virtuoso/plugins/* %{buildroot}%{_libdir}/

rm -fr %{buildroot}%{_libdir}/*.a
mv %{buildroot}%{_libdir}/*.so %{buildroot}%{_libdir}/virtuoso/plugins/
mkdir -p %{buildroot}%{_libdir}/virtuoso/jars
mv %{buildroot}%{_libdir}/jdbc-2.0 %{buildroot}%{_libdir}/virtuoso/jars/jdbc2.0
mv %{buildroot}%{_libdir}/jdbc-3.0 %{buildroot}%{_libdir}/virtuoso/jars/jdbc3.0
mv %{buildroot}%{_libdir}/jdbc-4.0 %{buildroot}%{_libdir}/virtuoso/jars/jdbc4.0
mv %{buildroot}%{_libdir}/jdbc-4.1 %{buildroot}%{_libdir}/virtuoso/jars/jdbc4.1
mv %{buildroot}%{_libdir}/jdbc-4.2 %{buildroot}%{_libdir}/virtuoso/jars/jdbc4.2
mv %{buildroot}%{_libdir}/jena %{buildroot}%{_libdir}/virtuoso/jars/jena
mv %{buildroot}%{_libdir}/jena2 %{buildroot}%{_libdir}/virtuoso/jars/jena2
mv %{buildroot}%{_libdir}/jena3 %{buildroot}%{_libdir}/virtuoso/jars/jena3
mv %{buildroot}%{_libdir}/sesame %{buildroot}%{_libdir}/virtuoso/jars/sesame
mkdir -p %{buildroot}%{_sysconfdir}/virtuoso
mv %{buildroot}%{_var}/lib/virtuoso/db/virtuoso.ini %{buildroot}%{_sysconfdir}/virtuoso/

#conflicts with unixODBC
rm -f  %{buildroot}%{_bindir}/isql
rm -f  %{buildroot}%{_libdir}/*.la
rm -f  %{buildroot}%{_libdir}/virtuoso/hosting/*.*a
