# TODO
# - drop fonts and sun/apple/server stuff as did debian? (read debian/README.debian)
%define	ver	2.7
%define	debrel	54
Summary:	Collection of MIME handling utilities
Summary(de.UTF-8):	Sammlung von MIME-Behandlungs-Utilities
Summary(fr.UTF-8):	Ensemble d'utilitaires de gestion MIME
Summary(pl.UTF-8):	Zestaw narzędzi do obsługi standardu MIME
Summary(tr.UTF-8):	MIME işleme araçları
Name:		metamail
Version:	%{ver}.%{debrel}
Release:	3
License:	GPL v2
Group:		Applications/Mail
Source0:	mm%{ver}.tar.Z
# Source0-md5:	fd5617ea87e20d7f2fa839e1d1fede60
Source1:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-non-english-man-pages.tar.bz2
# Source1-md5:	0ad0e591d536bc4e0d5ae97514ee6cc4
Source2:	htmlview
Source3:	ftp://ftp.debian.org/debian/pool/main/m/metamail/%{name}_%{ver}-%{debrel}.diff.gz
# Source3-md5:	2071dc7b9c33345443ab9a619e640a69
Patch0:		%{name}-ncurses.patch
Patch1:		%{name}-pager.patch
Patch2:		%{name}-linux.patch
Patch3:		%{name}-fixawk.patch
Patch4:		%{name}-fonts.patch
Patch5:		%{name}-am.patch
Patch6:		%{name}-suggestedname.patch
Patch7:		%{name}-metasend_mktemp.patch
Patch8:		%{name}-procmail_warning.patch
Patch9:		%{name}-2.7.53.3-glibc-2.10.patch
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
%setup -q -n mm%{ver}
cd src

# there's {metamail,richmail} unused in debian patch and metamail is libmetamail sources
# but due debian patch patching (erronously probably) metamail/splitmail.c, we need to keep it first
%{__rm} -r richmail
mv metamail metamail.org
mkdir metamail
mv metamail.org/splitmail.c metamail

%{__gzip} -dc %{SOURCE3} | %{__patch} -p1

# needed as file was created from patching
chmod +x configure

# same as mimeencode
echo '.so mimencode.1' > man/mmencode.1

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
cd src
%patch9 -p1
cd ..

%build
cd src
%{__libtoolize}
%{__aclocal} -I config
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static
%{__make} -j1
%{__make} -C fonts

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_fontdir},%{_mandir}/man{1,5}}

cd src
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install man/*.1 debian/mimencode.1 debian/mimeit.1 $RPM_BUILD_ROOT%{_mandir}/man1
install man/*.5 $RPM_BUILD_ROOT%{_mandir}/man5

install fonts/*.pcf 	  $RPM_BUILD_ROOT%{_fontdir}
install fonts/fonts.alias $RPM_BUILD_ROOT%{_fontdir}
bzip2 -dc %{SOURCE1} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}
mkfontdir $RPM_BUILD_ROOT%{_fontdir}

# compatibility hardlink
ln -f $RPM_BUILD_ROOT%{_bindir}/mimencode $RPM_BUILD_ROOT%{_bindir}/mmencode

# just utility functions library for metamail, not exported metamail functionality - so kill it
%{__rm} -r $RPM_BUILD_ROOT%{_includedir}/metamail
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmetamail.{so,la}

# that site doesn't exist
%{__rm} $RPM_BUILD_ROOT{%{_bindir}/patch-metamail,%{_mandir}/man1/patch-metamail.1}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc src/{README,CREDITS,mailers.txt}
%attr(755,root,root) %{_bindir}/audiocompose
%attr(755,root,root) %{_bindir}/audiosend
%attr(755,root,root) %{_bindir}/extcompose
%attr(755,root,root) %{_bindir}/getfilename
%attr(755,root,root) %{_bindir}/htmlview
%attr(755,root,root) %{_bindir}/mailserver
%attr(755,root,root) %{_bindir}/mailto
%attr(755,root,root) %{_bindir}/mailto-hebrew
%attr(755,root,root) %{_bindir}/metamail
%attr(755,root,root) %{_bindir}/metasend
%attr(755,root,root) %{_bindir}/mimeit
%attr(755,root,root) %{_bindir}/mimencode
%attr(755,root,root) %{_bindir}/mmencode
%attr(755,root,root) %{_bindir}/rcvAppleSingle
%attr(755,root,root) %{_bindir}/richtext
%attr(755,root,root) %{_bindir}/richtoatk
%attr(755,root,root) %{_bindir}/showaudio
%attr(755,root,root) %{_bindir}/showexternal
%attr(755,root,root) %{_bindir}/shownonascii
%attr(755,root,root) %{_bindir}/showpartial
%attr(755,root,root) %{_bindir}/showpicture
%attr(755,root,root) %{_bindir}/sndAppleSingle
%attr(755,root,root) %{_bindir}/splitmail
%attr(755,root,root) %{_bindir}/sun-audio-file
%attr(755,root,root) %{_bindir}/sun-message
%attr(755,root,root) %{_bindir}/sun-message.csh
%attr(755,root,root) %{_bindir}/sun-to-mime
%attr(755,root,root) %{_bindir}/sun2mime
%attr(755,root,root) %{_bindir}/uudepipe
%attr(755,root,root) %{_bindir}/uuenpipe
%attr(755,root,root) %{_libdir}/libmetamail.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmetamail.so.0
%{_libdir}/metamail
%{_mandir}/man1/audiocompose.1*
%{_mandir}/man1/audiosend.1*
%{_mandir}/man1/extcompose.1*
%{_mandir}/man1/getfilename.1*
%{_mandir}/man1/mailto-hebrew.1*
%{_mandir}/man1/mailto.1*
%{_mandir}/man1/metamail.1*
%{_mandir}/man1/metasend.1*
%{_mandir}/man1/mime.1*
%{_mandir}/man1/mimeit.1*
%{_mandir}/man1/mimencode.1*
%{_mandir}/man1/mmencode.1*
%{_mandir}/man1/richtext.1*
%{_mandir}/man1/showaudio.1*
%{_mandir}/man1/showexternal.1*
%{_mandir}/man1/shownonascii.1*
%{_mandir}/man1/showpartial.1*
%{_mandir}/man1/showpicture.1*
%{_mandir}/man1/splitmail.1*
%{_mandir}/man1/uudepipe.1*
%{_mandir}/man1/uuenpipe.1*
%{_mandir}/man5/mailcap.5*
%lang(fi) %{_mandir}/fi/man1/*
%lang(pl) %{_mandir}/pl/man1/*
