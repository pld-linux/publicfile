Summary:	DJB Publicfile - httpd & ftpd servers
Summary(pl):	DJB Publicfile - serwery httpd i ftpd
Name:		publicfile
Version:	0.52
Release:	3
License:	DJB (free to use, see http://cr.yp.to/distributors.html)
Group:		Networking/Daemons
Source0:	http://cr.yp.to/publicfile/%{name}-%{version}.tar.gz
# Source0-md5:	e493d69627b4fb2c7c764c0ff34330d7
Patch0:		%{name}-glibc.patch
Patch1:		%{name}-PASV.patch
URL:		http://cr.yp.to/%{name}.html
BuildRequires:	rpmbuild(macros) >= 1.159
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/userdel
Requires:	daemontools
Requires:	ucspi-tcp
Provides:	user(ftplog)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
publicfile supplies files to the public through HTTP and FTP.

%description -l pl
publicfile s³u¿y do publikacji plików przez protoko³y HTTP i FTP.

%prep
%setup -q
%patch0
%patch1

%build
echo %{__cc} %{rpmcflags} > conf-cc
echo %{_libdir}/%{name} > conf-home
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}/bin

### STANDARD BINARIES ###

install configure	$RPM_BUILD_ROOT%{_libdir}/%{name}/bin
install	ftpd		$RPM_BUILD_ROOT%{_libdir}/%{name}/bin
install httpd		$RPM_BUILD_ROOT%{_libdir}/%{name}/bin

### CONTROL SCRIPTS AND DIRECTORIES ###

install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/httpd
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/ftpd

### HTTPD ###

cd $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/httpd
mkdir log
mkdir log/main
touch log/status
mkdir env
echo 127.0.0.1	>env/IP
echo 80		>env/PORT
echo 100	>env/MAXCONN

cat>run<<___
#!/bin/sh
exec 2>&1
exec envuidgid ftp softlimit -o20 -d50000 tcpserver -vDRHl0 -b50 -c\`cat env/MAXCONN\` \`cat env/IP\` \`cat env/PORT\` %{_libdir}/%{name}/bin/httpd /home/services/%{name}
___

cat>log/run<<___
#!/bin/sh
exec setuidgid ftplog multilog t ./main '-*' '+* * status: *' =status
___


### FTPD ###

cd $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/ftpd
mkdir log
mkdir log/main
touch log/status
mkdir env
echo 127.0.0.1	>env/IP
echo 21		>env/PORT
echo 40		>env/MAXCONN

cat>run<<___
#!/bin/sh
exec 2>&1
exec envuidgid ftp softlimit -o20 -d50000 tcpserver -vDRHl0 -b20 -c\`cat env/MAXCONN\` -B'220 Features: a p .
' \`cat env/IP\` \`cat env/PORT\` %{_libdir}/%{name}/bin/ftpd /home/services/%{name}
___

cat>log/run<<___
#!/bin/sh
exec setuidgid ftplog multilog t ./main '-*' '+* * status: *' =status
___


### HOME ###

install -d $RPM_BUILD_ROOT/home/services/%{name}
install -d $RPM_BUILD_ROOT/home/services/%{name}/0
cd $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
ln -s ../../home/services/%{name} file
cd $RPM_BUILD_ROOT/home/services/%{name}
ln -s 0 127.0.0.1
ln -s 0 localhost
ln -s 0 localhost.localdomain

### SERVICE INSTALLATION ###

install -d $RPM_BUILD_ROOT/service
cd $RPM_BUILD_ROOT/service
ln -s ..%{_sysconfdir}/%{name}/ftpd
ln -s ..%{_sysconfdir}/%{name}/httpd

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`/bin/id -u ftplog 2>/dev/null`" ]; then
	if [ "`/bin/id -u ftplog`" != "39" ]; then
		echo "Error: user ftplog doesn't have uid=39. Correct this before installing publicfile." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u 39 -g ftp -s /bin/false -d /usr/share/empty ftplog
fi

%preun
if [ "$1" = "0" ]; then
	svc -d /service/ftpd
	svc -d /service/httpd
fi

%postun
if [ "$1" = "0" ]; then
	%userremove ftplog
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}
%dir %attr(0755,root,root) %{_sysconfdir}/%{name}
%dir %attr(3755,root,root) %{_sysconfdir}/%{name}/httpd
%dir %attr(3755,root,root) %{_sysconfdir}/%{name}/ftpd
%dir %attr(2755,root,root) %{_sysconfdir}/%{name}/httpd/log
%dir %attr(2755,ftplog,ftp) %{_sysconfdir}/%{name}/httpd/log/main
%attr(644,ftplog,ftp) %{_sysconfdir}/%{name}/httpd/log/status
%dir %attr(2755,root,root) %{_sysconfdir}/%{name}/httpd/env
%config %attr(644,root,root) %{_sysconfdir}/%{name}/httpd/env/*
%attr(755,root,root) %{_sysconfdir}/%{name}/httpd/run
%attr(755,root,root) %{_sysconfdir}/%{name}/httpd/log/run
%dir %attr(2755,root,root) %{_sysconfdir}/%{name}/ftpd/log
%dir %attr(2755,ftplog,ftp) %{_sysconfdir}/%{name}/ftpd/log/main
%attr(644,ftplog,ftp) %{_sysconfdir}/%{name}/ftpd/log/status
%dir %attr(2755,root,root) %{_sysconfdir}/%{name}/ftpd/env
%config %attr(644,root,root) %{_sysconfdir}/%{name}/ftpd/env/*
%attr(755,root,root) %{_sysconfdir}/%{name}/ftpd/run
%attr(755,root,root) %{_sysconfdir}/%{name}/ftpd/log/run
%dir %attr(2755,root,root) /home/services/%{name}
%dir %attr(2755,root,root) /home/services/%{name}/0
/home/services/%{name}/l*
/home/services/%{name}/1*
%{_sysconfdir}/%{name}/file
/service/ftpd
/service/httpd
