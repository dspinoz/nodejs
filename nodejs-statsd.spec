%{?nodejs_find_provides_and_requires}

Name:           nodejs-statsd
Version:        0.7.2
Release:        1%{?dist}
Summary:        Simple daemon for easy stats aggregation

Group:          Node
License:        Free

URL:            http://github.com/etsy/statsd
Source0:        https://registry.npmjs.org/statsd/-/statsd-0.7.2.tgz

BuildArch:      noarch
ExclusiveArch:  %{ix86} x86_64 %{arm} noarch

BuildRequires:  nodejs-devel nodeunit nodejs-temp nodejs-underscore

%description

%prep
%setup -q -n package

%build
#nothing to do
./run_tests.sh


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/statsd
cp -pr .travis.yml .npmignore * %{buildroot}%{nodejs_sitelib}/statsd

%nodejs_symlink_deps

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/statsd

%changelog
* Thu Dec 18 2014 Daniel Spinozzi <dspinoz@gmail.com> - 0.7.2-1
- packaged for installation on redhat using epel nodejs
