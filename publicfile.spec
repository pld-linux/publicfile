Summary:	DJB Publicfile - httpd & ftpd servers
Summary(pl):	DJB Publicfile - serwery httpd i ftpd
Name:		publicfile
Version:	0.52
Release:	1
License:	DJB (free to use, see http://cr.yp.to/distributors.html)
Group:		Networking/Daemons
Source0:	http://cr.yp.to/publicfile/%{name}-%{version}.tar.gz
# Source0-md5:	e493d69627b4fb2c7c764c0ff34330d7
URL:		http://cr.yp.to/publicfile.html
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/userdel
Requires:	daemontools
Requires:	ucspi-tcp
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
publicfile supplies files to the public through HTTP and FTP.

%description -l pl
publicfile s³u¿y do publikacji plików przez protoko³y HTTP i FTP.

%prep
%setup -q

%build
echo %{__cc} %{rpmcflags} > conf-cc
echo %{_libdir}/%{name} > conf-home
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}/bin

install configure	$RPM_BUILD_ROOT%{_libdir}/%{name}/bin
install	ftpd		$RPM_BUILD_ROOT%{_libdir}/%{name}/bin
install httpd		$RPM_BUILD_ROOT%{_libdir}/%{name}/bin

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`id -u ftplog`" ]; then
	if [ "`id -u ftplog`" != "39" ]; then
		echo "Error: user ftplog doesn't have uid=39. Correct this before installing publicfile." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u 39 -g ftp -s /dev/null ftplog
fi

%postun
if [ "$1" = "0" ]; then
	/usr/sbin/userdel ftplog
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}
