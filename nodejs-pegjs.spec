%{?nodejs_find_provides_and_requires}

Name:           nodejs-pegjs
Version:        0.6.2
Release:        1%{?dist}
Summary:        Parser generator for JavaScript

Group:          Node
License:        Free

URL:            http://pegjs.majda.cz/
Source0:        https://registry.npmjs.org/pegjs/-/pegjs-0.6.2.tgz

BuildArch:      noarch
ExclusiveArch:  %{ix86} x86_64 %{arm} noarch

BuildRequires:  nodejs-devel

%description
PEG.js is a simple parser generator for JavaScript that produces fast 
parsers with excellent error reporting. You can use it to process 
complex data or computer languages and build transformers, interpreters, 
compilers and other tools easily.

%prep
%setup -q -n package


# patch error when writing to stdout (from 0.7.0)
patch -p0 <<EOF
--- bin.orig/pegjs	2014-08-17 11:51:25.409848979 +0930
+++ bin/pegjs	2014-08-17 11:51:46.586921853 +0930
@@ -138,5 +138,7 @@
   }
 
   outputStream.write(exportVar + " = " + parser.toSource() + ";\n");
+if (outputStream !== process.stdout) {
   outputStream.end();
+}
 });
EOF


%build
#nothing to do


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/pegjs
cp -pr bin lib package.json LICENSE VERSION README.md %{buildroot}%{nodejs_sitelib}/pegjs

mkdir -p %{buildroot}%{_bindir}
ln -sf ../lib/node_modules/pegjs/bin/pegjs %{buildroot}%{_bindir}/pegjs

%nodejs_symlink_deps

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/pegjs
%{_bindir}/pegjs


%changelog
* Sat Aug 16 2014 Daniel Spinozzi <dspinoz@gmail.com> - 0.6.2-1
- Version for nodejs-cube
* Mon Aug 11 2014 Daniel Spinozzi <dspinoz@gmail.com> - 0.7.0-1
- packaged for installation on redhat using epel nodejs
