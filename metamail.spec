Summary:     Collection of MIME handling utilities
Summary(de): Sammlung von MIME-Behandlungs-Utilities
Summary(fr): Ensemble d'utilitaires de gestion MIME
Summary(tr): MIME iþleme araçlarý
Name:        metamail
Version:     2.7
Release:     19
Copyright:   Distributable
Group:       Applications/Mail
Source:      ftp://thumper.bellcore.com/pub/nsp/metamail/mm%{version}.tar.Z
Patch0:      mm-2.7-make.patch
Patch1:      mm-2.7-fonts.patch
Patch2:      mm-2.7-glibc.patch
Patch3:      mm-2.7-csh.patch
Patch4:      mm-2.7-uudecode.patch
Patch5:      mm-2.7-sunquote.patch
Patch6:      mm-2.7-tmpfile.patch
Patch7:      mm-2.7-ohnonotagain.patch
Patch8:      mm-2.7-arghhh.patch
Patch9:      mm-ncurses.patch
Requires:    mktemp sharutils csh
BuildRoot:   /tmp/%{name}-%{version}-root

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
mkdir -p $RPM_BUILD_ROOT/{usr/bin,usr/lib/metamail/fonts,usr/man/man1}

cd src
make INSTROOT=$RPM_BUILD_ROOT/usr install-all

install fonts/*.pcf $RPM_BUILD_ROOT%{_libdir}/metamail/fonts
install fonts/fonts.alias $RPM_BUILD_ROOT%{_libdir}/metamail/fonts
mkfontdir $RPM_BUILD_ROOT%{_libdir}/metamail/fonts

rm -f $RPM_BUILD_ROOT%{_bindir}/*.orig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc src/README src/CREDITS src/mailers.txt
%{_libdir}/metamail
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%changelog
* Sat Oct 17 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [2.7-19]
- added removing $RPM_BUILD_ROOT%{_bindir}/*.orig in %install,
- removed -b <sufix> from all %patch,
- added mm-ncurses.patch patch for compiling mm against libncurses.

* Tue Sep 01 1998 Marcin Korzonek <mkorz@shadow.eu.org>
- added pl translation,
- allow building from non-root account.

* Tue Aug  4 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Tue Jun 23 1998 Alan Cox <alan@redhat.com>
- Here we go again. One more quoting issue.

* Mon Jun 22 1998 Alan Cox <alan@redhat.com>
- If you want to know how not to write secure software
  then metamail is a good worked example. Mind you to
  be fair the original author wrote it as a prototype
  MIME tool and it stuck. Anyway it might actually be
  safe now. More from the Linux Security Audit Project.

* Tue Jun 16 1998 Alan Cox <alan@redhat.com>
- Round and round the tmp fixes go
  Where they stop nobody knows
- More holes in metamail fixed - (Linux Security Audit Project)

* Tue May 19 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Tue May 19 1998 Alan Cox <alan@redhat.com>
- Fixed the quoting bug in sun mail handling noted by Chris Evans and
  a while back via bugtraq.

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Oct 24 1997 Erik Troan <ewt@redhat.com>
- added security fix for uudecode 
- requires mktemp, sharutils

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc 

* Tue Apr 22 1997 Erik Troan <ewt@redhat.com>
- Added security patch from Olaf for csh escapes.
