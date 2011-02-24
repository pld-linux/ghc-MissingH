%define		pkgname MissingH
Summary:	Large utility library
Name:		ghc-%{pkgname}
Version:	1.1.0.3
Release:	0.1
Group:		Libraries
# Data/Hash/CRC32/GZip.hs is BSD
# Data/Hash/CRC32/Posix.hs is GPL+
# System/Path/NameManip.hs is LGPLv2+
# System/Time/ParseDate.hs is GPLv2 (newer parsedate is now BSD)
# all 40 other src (and testsrc) files are GPLv2+
License:	GPL v2+
URL:		http://hackage.haskell.org/package/%{pkgname}
Source0:	http://hackage.haskell.org/packages/archive/%{pkgname}/%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	a64af1885d60523fe598b4dad086fa6e
BuildRequires:	ghc >= 6.12.3
#BuildRequires:	ghc-HUnit
#BuildRequires:	ghc-doc
#BuildRequires:	ghc-hslogger
#BuildRequires:	ghc-mtl
#BuildRequires:	ghc-network
#BuildRequires:	ghc-parsec
#BuildRequires:	ghc-prof
#BuildRequires:	ghc-regex-compat
#BuildRequires:	hscolour
%requires_releq	ghc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ghcdir		ghc-%(/usr/bin/ghc --numeric-version)

%description
MissingH is a library of all sorts of utility functions for Haskell
programmers. It is written in pure Haskell and thus should be
extremely portable and easy to use.

%prep
%setup -q -n %{pkgname}-%{version}

mv COPYRIGHT COPYRIGHT.orig
iconv -f iso8859-1 -t utf-8 COPYRIGHT.orig > COPYRIGHT

%build
runhaskell Setup.hs configure -v2 \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
rm -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT/%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
