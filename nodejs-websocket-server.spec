%{?nodejs_find_provides_and_requires}

Name:           nodejs-websocket-server
Version:        1.4.04
Release:        1%{?dist}
Summary:        This is a server for drafts 75 and 76 of the WebSocket Protocol.

Group:          Node
License:        Free

URL:            https://www.npmjs.org/package/websocket-server
Source0:        https://registry.npmjs.org/websocket-server/-/websocket-server-1.4.04.tgz

BuildArch:      noarch
ExclusiveArch:  %{ix86} x86_64 %{arm} noarch

BuildRequires:  nodejs-devel

%description
%{summary}

%prep
%setup -q -n package


%build
#nothing to do


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/websocket-server
cp -pr lib docs tools package.json LICENSE.md README.md Makefile %{buildroot}%{nodejs_sitelib}/websocket-server

%nodejs_symlink_deps

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/websocket-server
%doc %{nodejs_sitelib}/websocket-server/docs


%changelog
* Mon Aug 14 2014 Daniel Spinozzi <dspinoz@gmail.com> - 0.6.5-1
- packaged for installation on redhat using epel nodejs
