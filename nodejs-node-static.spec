%{?nodejs_find_provides_and_requires}

Name:           nodejs-node-static
Version:        0.6.5
Release:        1%{?dist}
Summary:        A simple, rfc 2616 compliant file streaming module for node

Group:          Node
License:        Free

URL:            https://github.com/cloudhead/node-static
Source0:        https://registry.npmjs.org/node-static/-/node-static-0.6.5.tgz

BuildArch:      noarch
ExclusiveArch:  %{ix86} x86_64 %{arm} noarch

BuildRequires:  nodejs-devel

%description
A simple, rfc 2616 compliant file streaming module for node. 
node-static understands and supports conditional GET and HEAD requests. 
node-static was inspired by some of the other static-file serving modules
 out there, such as node-paperboy and antinode.

%prep
%setup -q -n package


%build
#nothing to do


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/node-static
cp -pr bin etc lib package.json LICENSE README.md %{buildroot}%{nodejs_sitelib}/node-static

mkdir -p %{buildroot}%{_bindir}
ln -sf ../lib/node_modules/node-static/bin/cli.js %{buildroot}%{_bindir}/node-static-cli

%nodejs_symlink_deps

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/node-static
%{_bindir}/node-static-cli


%changelog
* Mon Aug 14 2014 Daniel Spinozzi <dspinoz@gmail.com> - 0.6.5-1
- packaged for installation on redhat using epel nodejs
