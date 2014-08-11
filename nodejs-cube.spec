%{?nodejs_find_provides_and_requires}

Name:           nodejs-cube
Version:        0.2.12
Release:        1%{?dist}
Summary:        Cube is a system for collecting timestamped events and deriving metrics.

Group:          Node
License:        Apache License, Version 2.0

URL:            http://square.github.io/cube/
Source0:        https://registry.npmjs.org/cube/-/cube-0.2.12.tgz

BuildArch:      noarch
ExclusiveArch:  %{ix86} x86_64 %{arm} noarch

BuildRequires:  nodejs-devel

%description
Cube is a system for collecting timestamped events and deriving metrics. 
By collecting events rather than metrics, Cube lets you compute aggregate 
statistics post hoc. It also enables richer analysis, such as quantiles 
and histograms of arbitrary event sets. Cube is built on MongoDB and 
available under the Apache License.

Want to learn more? See the wiki.

%prep
%setup -q -n package


%build
#nothing to do


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/cube
cp -pr bin lib package.json LICENSE README.md static %{buildroot}%{nodejs_sitelib}/cube

mkdir -p %{buildroot}%{_bindir}
ln -sf ../lib/node_modules/cube/bin/collector.js %{buildroot}%{_bindir}/cube-collector
ln -sf ../lib/node_modules/cube/bin/evaluator.js %{buildroot}%{_bindir}/cube-evaluator

%nodejs_symlink_deps

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/cube
%{_bindir}/cube-collector
%{_bindir}/cube-evaluator


%changelog
* Mon Aug 11 2014 Daniel Spinozzi <dspinoz@gmail.com> - 0.2.12-1
- packaged for installation on redhat using epel nodejs
