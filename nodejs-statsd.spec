%{?nodejs_find_provides_and_requires}

Name:           nodejs-queue-async
Version:        1.0.7
Release:        1%{?dist}
Summary:        A little helper for asynchronous JavaScript

Group:          Node
License:        Free

URL:            http://github.com/mbostock/queue
Source0:        https://registry.npmjs.org/queue-async/-/queue-async-1.0.7.tgz

BuildArch:      noarch
ExclusiveArch:  %{ix86} x86_64 %{arm} noarch

BuildRequires:  nodejs-devel

%description

%prep
%setup -q -n package

%build
#nothing to do


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/queue-async
cp -pr src package.json LICENSE README.md component.json Makefile queue.js queue.min.js %{buildroot}%{nodejs_sitelib}/queue-async

%nodejs_symlink_deps

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/queue-async

%changelog
* Wed Dec 10 2014 Daniel Spinozzi <dspinoz@gmail.com> - 1.0.7-1
- packaged for installation on redhat using epel nodejs
