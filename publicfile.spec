Summary:	DJB Publicfile - httpd & ftpd servers.
Summary(pl):	DJB Publicfile - serwery httpd i ftpd.
Name:		publicfile
Version:	0.52
Release:	1
License:	http://cr.yp.to/distributors.html (free to use)
Group:		Networking/Daemons
Group(cs):	S�ov�/D�moni
Group(da):	Netv�rks/D�moner
Group(de):	Netzwerkwesen/Server
Group(es):	Red/Servidores
Group(fr):	R�seau/Serveurs
Group(is):	Net/P�kar
Group(it):	Rete/Demoni
Group(no):	Nettverks/Daemoner
Group(pl):	Sieciowe/Serwery
Group(pt):	Rede/Servidores
Group(ru):	����/������
Group(sl):	Omre�ni/Stre�niki
Group(sv):	N�tverk/Demoner
Group(uk):	������/������
Source0:	http://cr.yp.to/publicfile/%{name}-%{version}.tar.gz
URL:		http://cr.yp.to/publicfile.html
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
publicfile supplies files to the public through HTTP and FTP.

%description -l pl
publicfile s�u�y do publikacji plik�w przez protoko�y HTTP i FTP.

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

##### ftplog user #####
%pre
if [ -n "`id -u ftplog`" ]; then
	if [ "`id -u ftplog`" != "39" ]; then
		echo "Warning: the user ftplog doesn't have uid=39. Correct this before installing publicfile" 1>&2
		exit 1
	fi
else
	%{_sbindir}/useradd -u 39 -g ftp -s /dev/null ftplog
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/
