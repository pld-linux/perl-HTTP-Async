#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%define	pdir	HTTP
%define	pnam	Async
Summary:	HTTP::Async - process multiple HTTP requests in parallel without blocking
Summary(pl.UTF-8):	HTTP::Async - równoległa obsługa wielu żądań HTTP bez blokowania
Name:		perl-HTTP-Async
Version:	0.09
Release:	1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-authors/id/E/EV/EVDB/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	231a496fba4502c5e1ecb1965b067a0f
URL:		http://search.cpan.org/dist/HTTP-Async/
BuildRequires:	perl-Module-Build
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl(HTTP::Request)
BuildRequires:	perl(HTTP::Response)
BuildRequires:	perl(HTTP::Server::Simple::CGI)
BuildRequires:	perl(HTTP::Status)
BuildRequires:	perl(LWP::UserAgent)
BuildRequires:	perl(Net::HTTP)
BuildRequires:	perl(Net::HTTP::NB)
BuildRequires:	perl(URI::Escape)
BuildRequires:	perl-Test-HTTP-Server-Simple
BuildRequires:	perl-URI
BuildRequires:	perl-libwww
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Although using the conventional LWP::UserAgent is fast and easy it
does have some drawbacks - the code execution blocks until the request
has been completed and it is only possible to process one request at a
time. HTTP::Async attempts to address these limitations.

It gives you a 'Async' object that you can add requests to, and then
get the requests off as they finish. The actual sending and receiving
of the requests is abstracted. As soon as you add a request it is
transmitted, if there are too many requests in progress at the moment
they are queued. There is no concept of starting or stopping - it runs
continuously.

Whilst it is waiting to receive data it returns control to the code
that called it meaning that you can carry out processing whilst
fetching data from the network. All without forking or threading - it
is actually done using select lists.

%description -l pl.UTF-8
Pomimo, że konwencjonalny moduł LWP::UserAgent jest szybki i łatwy
w użyciu, ma kilka wad - wykonywanie kodu blokuje inne operacje do
czasu zakończenia żądania HTTP i możliwa jest obsługa tylko
jednego w tym samym czasie. HTTP::Async stara się rozwiązać ten
problem.

Moduł udostępnia obiekt 'Async', do którego można dodawać
żądania HTTP i pobierać je z niego gdy te zostaną zakończone.
Wysyłanie i odbieranie żądań jest ukryte pod warstwą abstrakcji.
Po dodaniu żądania jest ono natychmiastowo wysyłane, a jeśli jest
ich zbyt dużo w danym momencie, kolejne wywołania są kolejkowane.

Podczas oczekiwania na odbiór danych kontrola przekazywana jest do
wywołującego kodu, umożliwiając dalsze przetwarzanie podczas
pobierania odpowiedzi z sieci. Wszystkie operacje przeprowadzane są
za pomocą list select(), bez użycia podprocesów i wątków.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Makefile.PL \
	destdir=$RPM_BUILD_ROOT \
	installdirs=vendor
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES README TODO
%{perl_vendorlib}/HTTP/*.pm
%{perl_vendorlib}/HTTP/Async
%{_mandir}/man3/*
