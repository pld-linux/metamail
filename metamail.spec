Summary:	Collection of MIME handling utilities
Summary(de):	Sammlung von MIME-Behandlungs-Utilities
Summary(fr):	Ensemble d'utilitaires de gestion MIME
Summary(tr):	MIME iþleme araçlarý
Name:		metamail
Version:	2.7
Release:	19
Copyright:	Distributable
Group:		Applications/Mail
Source:		ftp://thumper.bellcore.com/pub/nsp/metamail/mm%{version}.tar.Z
Patch0:		mm-2.7-make.patch
Patch1:		mm-2.7-fonts.patch
Patch2:		mm-2.7-glibc.patch
Patch3:		mm-2.7-csh.patch
Patch4:		mm-2.7-uudecode.patch
Patch5:		mm-2.7-sunquote.patch
Patch6:		mm-2.7-tmpfile.patch
Patch7:		mm-2.7-ohnonotagain.patch
Patch8:		mm-2.7-arghhh.patch
Patch9:		mm-ncurses.patch
Requires:	mktemp sharutils csh
BuildRoot:	/tmp/%{name}-%{version}-root

%description
Metamail is an implementation of MIME, the Multipurpose Internet Mail
Extensions, a proposed standard for multimedia mail on the Internet.
Metamail implements MIME, and also implements extensibility and
configuration via the "mailcap" mechanism described in an informational RFC
that is a companion to the MIME document.

%description -l pl
Metamail obs³uguje standard MIME (rozszerzenie poczty internetowej dla
ró¿nych celów) u¿ywany do przesy³ania poczt± plików multimedialnych. MIME
jest te¿ wykorzystywany do kodowania znaków narodowych w listach i
artyku³ach news.

%prep
%setup -q -n mm2.7
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
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/metamail/fonts,%{_mandir}/man1}

cd src
make INSTROOT=$RPM_BUILD_ROOT%{_prefix} install-all

install fonts/*.pcf $RPM_BUILD_ROOT%{_libdir}/metamail/fonts
install fonts/fonts.alias $RPM_BUILD_ROOT%{_libdir}/metamail/fonts
mkfontdir $RPM_BUILD_ROOT%{_libdir}/metamail/fonts

rm -f $RPM_BUILD_ROOT%{_bindir}/*.orig

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man1/* \
	src/README src/CREDITS src/mailers.txt

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {src/README,src/CREDITS,src/mailers.txt}.gz
%{_libdir}/metamail
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*
