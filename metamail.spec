# TODO
# - drop fonts and sun/apple/server stuff as did debian? (read debian/README.debian)
%define	_ver	2.7
%define	_debrel 52
Summary:	Collection of MIME handling utilities
Summary(de.UTF-8):	Sammlung von MIME-Behandlungs-Utilities
Summary(fr.UTF-8):	Ensemble d'utilitaires de gestion MIME
Summary(pl.UTF-8):	Zestaw narzędzi do obsługi standardu MIME
Summary(tr.UTF-8):	MIME işleme araçları
Name:		metamail
Version:	%{_ver}.%{_debrel}
Release:	6
License:	GPL v2
Group:		Applications/Mail
Source0:	ftp://thumper.bellcore.com/pub/nsb/mm%{_ver}.tar.Z
# Source0-md5:	fd5617ea87e20d7f2fa839e1d1fede60
Source1:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-non-english-man-pages.tar.bz2
# Source1-md5:	0ad0e591d536bc4e0d5ae97514ee6cc4
Source2:	htmlview
Source3:	ftp://ftp.debian.org/debian/pool/main/m/metamail/%{name}_%{_ver}-%{_debrel}.diff.gz
# Source3-md5:	43d21022f048b6610932cf6f6f46b516
Patch0:		%{name}-ncurses.patch
Patch1:		%{name}-pager.patch
Patch2:		%{name}-linux.patch
Patch3:		%{name}-fixawk.patch
Patch4:		%{name}-fonts.patch
Patch5:		%{name}-am.patch
Patch6:		%{name}-suggestedname.patch
Patch7:		%{name}-metasend_mktemp.patch
Patch8:		%{name}-procmail_warning.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	ncurses-devel >= 5.0
Requires:	/usr/lib/sendmail
Requires:	mktemp
Requires:	sharutils
Provides:	htmlview
Obsoletes:	htmlview
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_fontdir	%{_libdir}/metamail/fonts

%description
Metamail is an implementation of MIME, the Multipurpose Internet Mail
Extensions, a proposed standard for multimedia mail on the Internet.
Metamail implements MIME, and also implements extensibility and
configuration via the "mailcap" mechanism described in an
informational RFC that is a companion to the MIME document.

This version includes Debian patches.

%description -l pl.UTF-8
Metamail obsługuje standard MIME (rozszerzenie poczty internetowej dla
różnych celów) używany do przesyłania pocztą plików multimedialnych.
MIME jest też wykorzystywany do kodowania znaków narodowych w listach
i artykułach news. Metamail jest konfigurowalny poprzez mechanizm
"mailcap" opisany w informacyjnym RFC towarzyszącym dokumentacji MIME.

Ta wersja zawiera łaty z Debiana.

%prep
%setup -q -n mm%{_ver}
cd src

# there's {metamail,richmail} unused in debian patch and metamail is libmetamail sources
# but due debian patch patching (erronously probably) metamail/splitmail.c, we need to keep it first
rm -rf richmail
mv metamail metamail.org
mkdir metamail
mv metamail.org/splitmail.c metamail

%{__gzip} -dc %{SOURCE3} | %{__patch} -p1

# needed as file was created from patching
chmod +x configure

# same as mimeencode
rm man/mmencode.1

cd ..
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p0
%patch8 -p1

%build
cd src
%{__aclocal} -I config
%{__libtoolize}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-static
%{__make} -j1
%{__make} -C fonts

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_fontdir},%{_mandir}/man1}

cd src
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install man/* debian/mimencode.1 debian/mimeit.1 $RPM_BUILD_ROOT%{_mandir}/man1

install fonts/*.pcf 	  $RPM_BUILD_ROOT%{_fontdir}
install fonts/fonts.alias $RPM_BUILD_ROOT%{_fontdir}
bzip2 -dc %{SOURCE1} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}
mkfontdir $RPM_BUILD_ROOT%{_fontdir}

#ln -f $RPM_BUILD_ROOT%{_bindir}/mmencode $RPM_BUILD_ROOT%{_bindir}/mimencode
rm -rf $RPM_BUILD_ROOT%{_includedir}/metamail
rm -f $RPM_BUILD_ROOT%{_libdir}/libmetamail.la

# that site doesn't exist
rm $RPM_BUILD_ROOT{%{_bindir}/patch-metamail,%{_mandir}/man1/patch-metamail.1}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc src/{README,CREDITS,mailers.txt}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libmetamail.so.*.*.*
%{_libdir}/metamail
%{_mandir}/man1/*
%lang(fi) %{_mandir}/fi/man1/*
%lang(pl) %{_mandir}/pl/man1/*
