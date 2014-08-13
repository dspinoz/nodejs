%{?nodejs_find_provides_and_requires}

Name:           nodejs-websocket
Version:        1.0.8
Release:        1%{?dist}
Summary:        JavaScript implementation of the WebSocket protocol versions 8 and 13 for Node

Group:          Node
License:        Apache License Version 2.0

URL:            https://www.npmjs.org/package/websocket
Source0:        https://registry.npmjs.org/websocket/-/websocket-1.0.8.tgz

BuildArch:      noarch
ExclusiveArch:  %{ix86} x86_64 %{arm} noarch

BuildRequires:  nodejs-devel

%description
This is a (mostly) pure JavaScript implementation of the WebSocket 
protocol versions 8 and 13 for Node.

%prep
%setup -q -n package


%build
#nothing to do


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/websocket
cp -pr lib src vendor package.json LICENSE README.md Makefile index.js install.js %{buildroot}%{nodejs_sitelib}/websocket

%nodejs_symlink_deps

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/websocket


%changelog
* Mon Aug 14 2014 Daniel Spinozzi <dspinoz@gmail.com> - 0.6.5-1
- packaged for installation on redhat using epel nodejs
