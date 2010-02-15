%define Werror_cflags %nil

Name:       virtuoso-opensource
Version:    6.1.0
Release:    %mkrel 1
License:    GPLv2
Summary:    OpenLink Virtuoso Database System Open-Source Edition
Group:      Development/Databases
Source0:    %{name}-%{version}.tar.gz
Patch4:     virtuoso-opensource-6.1.0-extern-iodbc.patch
Patch5:     virtuoso-opensource-6.1.0-nodemos_buildfix.patch
URL:        http://virtuoso.openlinksw.com/
BuildRoot:  %{_tmppath}/%{name}-%{version}
BuildRequires: openssl
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: bison
BuildRequires: flex
BuildRequires: gperf
BuildRequires: libxml2-devel
BuildRequires: openssl-devel
BuildRequires: iodbc-devel

Requires:       %name-applications

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
%doc AUTHORS CREDITS ChangeLog NEWS README
%attr(0755,root,root) %{_bindir}/*
%doc %{_datadir}/virtuoso/doc
#conflicts with unixODBC
%exclude %{_bindir}/isql
%{_sysconfdir}/virtuoso/virtuoso.ini

#--------------------------------------------------------------------

%package -n %name-conductor
Summary: Virtuoso open source edition Server Pages
Group: Development/Databases

%description -n %name-conductor
Virtuoso is a scalable cross-platform server that combines SQL/RDF/XML
Data Management with Web Application Server and Web Services Platform
functionality.

%files -n %name-conductor
%defattr(0644,root,root,0755)
%{_var}/lib/virtuoso/vsp/*.css
%{_var}/lib/virtuoso/vsp/*.html
%{_var}/lib/virtuoso/vsp/robots.txt
%{_var}/lib/virtuoso/vsp/admin/index_left.vsp
%{_var}/lib/virtuoso/vsp/images/*.gif
%{_var}/lib/virtuoso/vsp/images/*.jpg
%{_var}/lib/virtuoso/vsp/images/*.png
%{_var}/lib/virtuoso/vsp/vsmx/*.gif
%{_var}/lib/virtuoso/vsp/vsmx/*.jpg
%{_var}/lib/virtuoso/vsp/vsmx/*.vspx
%{_var}/lib/virtuoso/vsp/vsmx/*.xsl
%{_var}/lib/virtuoso/vsp/vsmx/*.css

#--------------------------------------------------------------------

%package -n %name-applications
Summary: Virtuoso open source applications
Group: Development/Databases

%description -n %name-applications
Virtuoso is a scalable cross-platform server that combines SQL/RDF/XML
Data Management with Web Application Server and Web Services Platform
functionality.

%files -n %name-applications
%defattr(0644,root,root,0755)
#%{_datadir}/virtuoso/doc
#%{_libdir}/virtuoso/plugins/*.a
%{_libdir}/virtuoso/hosting/*.a
%attr(0755,root,root) %{_libdir}/virtuoso/plugins/*.la
%attr(0755,root,root) %{_libdir}/*.la
%attr(0755,root,root) %{_libdir}/virtuoso/hosting/*.la
%attr(0755,root,root) %{_libdir}/virtuoso/hosting/*.so
%attr(0755,root,root) %{_libdir}/virtuoso/plugins/*.so

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
%{_libdir}/virtuoso/jars/jena/*.jar
%{_libdir}/virtuoso/jars/sesame/*.jar

#--------------------------------------------------------------------

%prep

%setup -q -n %{name}-%{version}
%patch4 -p0 -b .iodbc
%patch5 -p0

%build
# autogen.sh because of patching Makefile.am and configure to unixODBC
./autogen.sh

%configure2_5x \
	--with-iodbc=%_prefix --disable-all-vads 

%make

%install
rm -rf %{buildroot}

%makeinstall_std 
mkdir -p %{buildroot}%{_libdir}/virtuoso/plugins
mv %{buildroot}%{_libdir}/*.la %{buildroot}%{_libdir}/virtuoso/plugins/
cp -f %{buildroot}%{_libdir}/virtuoso/plugins/* %{buildroot}%{_libdir}/

rm -fr %{buildroot}%{_libdir}/*.a
mv %{buildroot}%{_libdir}/*.so %{buildroot}%{_libdir}/virtuoso/plugins/
mkdir -p %{buildroot}%{_libdir}/virtuoso/jars
mv %{buildroot}%{_libdir}/jdbc-2.0 %{buildroot}%{_libdir}/virtuoso/jars/jdbc2.0
mv %{buildroot}%{_libdir}/jdbc-3.0 %{buildroot}%{_libdir}/virtuoso/jars/jdbc3.0
mv %{buildroot}%{_libdir}/jdbc-4.0 %{buildroot}%{_libdir}/virtuoso/jars/jdbc4.0
mv %{buildroot}%{_libdir}/jena %{buildroot}%{_libdir}/virtuoso/jars/jena
mv %{buildroot}%{_libdir}/sesame %{buildroot}%{_libdir}/virtuoso/jars/sesame
mkdir -p %{buildroot}%{_sysconfdir}/virtuoso
mv %{buildroot}%{_var}/lib/virtuoso/db/virtuoso.ini %{buildroot}%{_sysconfdir}/virtuoso/

%clean
rm -rf %{buildroot}
