#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define	pdir	HTTP
%define	pnam	Async
Summary:	HTTP::Async - process multiple HTTP requests in parallel without blocking.
#Summary(pl):	
Name:		perl-HTTP-Async
Version:	0.07
Release:	1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-authors/id/E/EV/EVDB/HTTP-Async-0.07.tar.gz
# Source0-md5:	d18d2c705ea8a2b1e3d40cb65ee73fbd
# generic URL, check or change before uncommenting
#URL:		http://search.cpan.org/dist/HTTP-Async/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl(HTTP::Request)
BuildRequires:	perl(HTTP::Response)
BuildRequires:	perl(HTTP::Status)
BuildRequires:	perl(Net::HTTP)
BuildRequires:	perl(Net::HTTP::NB)
BuildRequires:	perl(URI)
BuildRequires:	perl(HTTP::Server::Simple::CGI)
BuildRequires:	perl(LWP::UserAgent)
BuildRequires:	perl(Module::Build)
BuildRequires:	perl(Test::HTTP::Server::Simple)
BuildRequires:	perl(URI::Escape)
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Although using the conventional LWP::UserAgent is fast and easy it does
have some drawbacks - the code execution blocks until the request has been
completed and it is only possible to process one request at a time.
HTTP::Async attempts to address these limitations.

It gives you a 'Async' object that you can add requests to, and then get the
requests off as they finish. The actual sending and receiving of the requests
is abstracted. As soon as you add a request it is transmitted, if there are
too many requests in progress at the moment they are queued. There is no
concept of starting or stopping - it runs continuously.

Whilst it is waiting to receive data it returns control to the code that
called it meaning that you can carry out processing whilst fetching data from
the network. All without forking or threading - it is actually done using
select lists.

# %description -l pl
# TODO

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Build.PL \
	destdir=$RPM_BUILD_ROOT \
	installdirs=vendor
./Build

%{?with_tests:./Build test}

%install
rm -rf $RPM_BUILD_ROOT

./Build install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES README TODO
%{perl_vendorlib}/HTTP/*.pm
%{perl_vendorlib}/HTTP/Async
%{_mandir}/man3/*
