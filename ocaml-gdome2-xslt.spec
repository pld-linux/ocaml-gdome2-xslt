Summary:	gdome2-xslt binding for OCaml
Summary(pl):	Wi±zania gdome2-xslt dla OCamla
Name:		ocaml-gdome2-xslt
Version:	0.0.6
Release:	1
License:	LGPL
Vendor:		Claudio Sacerdoti Coen <sacerdot@cs.unibo.it>
Group:		Libraries
#Source0Download: http://helm.cs.unibo.it/gdome_xslt/
Source0:	http://helm.cs.unibo.it/gdome_xslt/dist/gdome2-xslt-%{version}.tar.gz
# Source0-md5:	cebe083a33bd0c4b44f32be897d3805d
URL:		http://helm.cs.unibo.it/gdome_xslt/
BuildRequires:	autoconf
BuildRequires:	libxslt-devel
BuildRequires:	ocaml-findlib
BuildRequires:	ocaml-gdome2-devel
BuildRequires:	ocaml >= 3.04-7
%requires_eq	ocaml-runtime
%requires_eq	ocaml-gdome2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This OCaml library provides an high level API for XSLT processing. The
underlying implementation is based on libxml, gdome2 and libxslt.

This package contains files needed to run bytecode executables using
this library.

%description -l pl
Biblioteka ta dostarcza wysoko-poziomowe API do przetwarzania
dokumentów przy u¿yciu XSLT dla OCamla. Implementacja bazowana jest na
libxml, gdome2 oraz libxslt.

Pakiet ten zawiera binaria potrzebne do uruchamiania programów
u¿ywaj±cych tej biblioteki.

%package devel
Summary:	gdome2-xslt binding for OCaml - development part
Summary(pl):	Wi±zania gdome2-xslt dla OCamla - cze¶æ programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml
%requires_eq	ocaml-gdome2-devel

%description devel
This OCaml library provides an high level API for XSLT processing. The
underlying implementation is based on libxml, gdome2 and libxslt.

This package contains files needed to develop OCaml programs using
this library.

%description devel -l pl
Biblioteka ta dostarcza wysoko-poziomowe API do przetwarzania
dokumentów przy u¿yciu XSLT dla OCamla. Implementacja bazowana jest na
libxml, gdome2 oraz libxslt.

Pakiet ten zawiera pliki niezbêdne do tworzenia programów u¿ywaj±cych
tej biblioteki.

%prep
%setup -q -n gdome2-xslt-%{version}

%build
cd C/gdome_xslt
sed -e 's/gcc/$(CC)/' Makefile > Makefile.tmp
mv -f Makefile.tmp Makefile
%{__make} CC="%{__cc} %{rpmcflags} -fPIC"
cd ../../ocaml/gdome_xslt
rm -f *.so *.a
%{__autoconf}
%configure
sed -e 's/gcc/$(CC)/' Makefile > Makefile.tmp
mv -f Makefile.tmp Makefile
%{__make} CC="%{__cc} %{rpmcflags}" all opt

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml
cd ocaml/gdome_xslt
%{__make} install \
	PREFIX=$RPM_BUILD_ROOT%{_libdir}/ocaml \
	OCAMLLIB=$RPM_BUILD_ROOT%{_libdir}/ocaml
(cd $RPM_BUILD_ROOT%{_libdir}/ocaml && ln -s gdome2-xslt/dll*.so .)

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -r ../test/*.ml ../../test_files/* \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/gdome2-xslt
echo 'directory = "+gdome2-xslt"' >> $RPM_BUILD_ROOT%{_libdir}/ocaml/gdome2-xslt/META
mv $RPM_BUILD_ROOT%{_libdir}/ocaml/gdome2-xslt/META \
	$RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/gdome2-xslt

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_libdir}/ocaml/gdome2-xslt
%attr(755,root,root) %{_libdir}/ocaml/gdome2-xslt/*.so
%{_libdir}/ocaml/*.so

%files devel
%defattr(644,root,root,755)
%doc ocaml/gdome_xslt/*.mli
%{_libdir}/ocaml/gdome2-xslt/*.cm[ixa]*
%{_libdir}/ocaml/gdome2-xslt/*.a
%{_examplesdir}/%{name}-%{version}
%{_libdir}/ocaml/site-lib/gdome2-xslt
