Summary:	Collection of MIME handling utilities
Summary(de):	Sammlung von MIME-Behandlungs-Utilities
Summary(fr):	Ensemble d'utilitaires de gestion MIME
Summary(pl):	Zestaw narzêdzi do obs³ugi standardu MIME
Summary(tr):	MIME iþleme araçlarý
Name:		metamail
Version:	2.7
Release:	29
License:	Distributable
Group:		Applications/Mail
Group(de):	Applikationen/Post
Group(pl):	Aplikacje/Poczta
Group(pt):	Aplicações/Correio Eletrônico
Source0:	ftp://thumper.bellcore.com/pub/nsp/metamail/mm%{version}.tar.Z
Source1:	%{name}-non-english-man-pages.tar.bz2
Patch0:		%{name}-make.patch
Patch1:		%{name}-fonts.patch
Patch2:		%{name}-glibc.patch
Patch3:		%{name}-csh.patch
Patch4:		%{name}-uudecode.patch
Patch5:		%{name}-sunquote.patch
Patch6:		%{name}-tmpfile.patch
Patch7:		%{name}-ohnonotagain.patch
Patch8:		%{name}-arghhh.patch
Patch9:		%{name}-ncurses.patch
Patch10:	%{name}-nl.patch
Patch11:	%{name}-linux.patch
Patch12:	%{name}-fixawk.patch
Patch13:	%{name}-fixpartial.patch
Patch14:	%{name}-usesox.patch
BuildRequires:	ncurses-devel >= 5.0
BuildRequires:	XFree86
Requires:	mktemp
Requires:	sharutils
Requires:	/usr/lib/sendmail
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_fontdir	%{_libdir}/metamail/fonts

%description
Metamail is an implementation of MIME, the Multipurpose Internet Mail
Extensions, a proposed standard for multimedia mail on the Internet.
Metamail implements MIME, and also implements extensibility and
configuration via the "mailcap" mechanism described in an
informational RFC that is a companion to the MIME document.

%description -l pl
Metamail obs³uguje standard MIME (rozszerzenie poczty internetowej dla
ró¿nych celów) u¿ywany do przesy³ania poczt± plików multimedialnych.
MIME jest te¿ wykorzystywany do kodowania znaków narodowych w listach
i artyku³ach news.

%prep
%setup -q -n mm%{version}
%patch0  -p1
%patch1  -p1
%patch2  -p1
%patch3  -p1
%patch4  -p1
%patch5  -p1
%patch7  -p1
%patch8  -p1
%patch9  -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1

%build
cd src
%{__make} basics

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_fontdir},%{_mandir}/man1}

cd src
%{__make} install-all INSTROOT=$RPM_BUILD_ROOT%{_prefix} \
	MAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
	MAN4DIR=$RPM_BUILD_ROOT%{_mandir}/man4

install fonts/*.pcf 	  $RPM_BUILD_ROOT%{_fontdir}
install fonts/fonts.alias $RPM_BUILD_ROOT%{_fontdir}
bzip2 -dc %{SOURCE1} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}
mkfontdir $RPM_BUILD_ROOT%{_fontdir}

rm -f $RPM_BUILD_ROOT%{_bindir}/*.orig
rm -f $RPM_BUILD_ROOT%{_bindir}/*~

ln -f $RPM_BUILD_ROOT%{_bindir}/mmencode $RPM_BUILD_ROOT%{_bindir}/mimencode

gzip -9nf README CREDITS mailers.txt

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc src/{README,CREDITS,mailers.txt}.gz

%attr(755,root,root) %{_bindir}/*

%{_libdir}/metamail
%{_mandir}/man1/*
%{_mandir}/fi/man1/*
%{_mandir}/pl/man1/*
