Summary:	Collection of MIME handling utilities
Summary(de):	Sammlung von MIME-Behandlungs-Utilities
Summary(fr):	Ensemble d'utilitaires de gestion MIME
Summary(pl):	Zestaw narzêdzi do obs³ugi standardu MIME
Summary(tr):	MIME iþleme araçlarý
Name:		metamail
Version:	2.7
Release:	21
Copyright:	distributable
Group:		Applications/Mail
Group(pl):	Aplikacje/Poczta
Source:		ftp://thumper.bellcore.com/pub/nsp/metamail/mm%{version}.tar.Z
Patch0:		mm-make.patch
Patch1:		mm-fonts.patch
Patch2:		mm-glibc.patch
Patch3:		mm-csh.patch
Patch4:		mm-uudecode.patch
Patch5:		mm-sunquote.patch
Patch6:		mm-tmpfile.patch
Patch7:		mm-ohnonotagain.patch
Patch8:		mm-arghhh.patch
Patch9:		mm-ncurses.patch
BuildRequires:	ncurses-devel >= 5.0
Requires:	mktemp
Requires:	sharutils
BuildRoot:	/tmp/%{name}-%{version}-root

%define		_fontdir	%{_libdir}/metamail/fonts

%description
Metamail is an implementation of MIME, the Multipurpose Internet Mail
Extensions, a proposed standard for multimedia mail on the Internet.
Metamail implements MIME, and also implements extensibility and
configuration via the "mailcap" mechanism described in an
informational RFC that is a companion to the MIME document.

%description -l pl
Metamail obs³uguje standard MIME (rozszerzenie poczty internetowej
dla ró¿nych celów) u¿ywany do przesy³ania poczt± plików 
multimedialnych. MIME jest te¿ wykorzystywany do kodowania znaków
narodowych w listach i artyku³ach news.

%prep
%setup -q -n mm%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

%build
cd src
make basics

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_fontdir},%{_mandir}/man1}

cd src
make install-all INSTROOT=$RPM_BUILD_ROOT%{_prefix} \
	MAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
	MAN4DIR=$RPM_BUILD_ROOT%{_mandir}/man4

install fonts/*.pcf 	  $RPM_BUILD_ROOT%{_fontdir}
install fonts/fonts.alias $RPM_BUILD_ROOT%{_fontdir}
mkfontdir $RPM_BUILD_ROOT%{_fontdir}

rm -f $RPM_BUILD_ROOT%{_bindir}/*.orig
rm -f $RPM_BUILD_ROOT%{_bindir}/*~

strip --strip-unneeded $RPM_BUILD_ROOT%{_bindir}/* || :

gzip -9nf README CREDITS mailers.txt \
	$RPM_BUILD_ROOT%{_mandir}/man1/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc src/{README,CREDITS,mailers.txt}.gz

%attr(755,root,root) %{_bindir}/*

%{_libdir}/metamail
%{_mandir}/man1/*
