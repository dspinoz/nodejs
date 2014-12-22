%{?nodejs_find_provides_and_requires}

Name:           nodejs-statsd-cube-backend
Version:        0.0.1
Release:        1%{?dist}
Summary:        Backend for submitting metrics from statsd to cube

Group:          Node
License:        Free

URL:            https://codeload.github.com/luthermonson/cube-statsd-backend/zip/master
Source0:        cube-statsd-backend-%{version}.zip

BuildArch:      noarch
ExclusiveArch:  %{ix86} x86_64 %{arm} noarch

BuildRequires:  nodejs-devel
Requires:       nodejs-cube nodejs-statsd

%description

%prep
%setup -q -n cube-statsd-backend-master

patch -p0 <<EOF
--- lib/index.js	2014-12-23 09:30:21.521075318 +1030
+++ lib/index.js-dspinoz	2014-12-23 09:36:55.000058443 +1030
@@ -11,9 +11,9 @@
  */
 var colPrefix = function(metric_type, metric) {
 	var ary = metric.split('.');
-	if (options.prefix) ary.shift();
 	ary.unshift(metric_type);
-	return ary.join('_')+'_'+options.rate;
+	if (options.prefix) ary.unshift(options.prefix);
+	return ary.join('.');
 };
 
 /**
@@ -113,7 +113,7 @@
       date.setUTCSeconds(utcSeconds);
       delete(obj.data.time);
 
-      if(obj.data.count > 0) {
+      if(obj.data) {
         emitter.send({
           type: obj.col,
           time: date,
@@ -134,6 +134,7 @@
 	if (!startup_time || !config || !events) return false;
 
 	options.debug = config.debug;
+        options.prefix = config.cube.typePrefix;
 
   emitter = cube.emitter(config.cube.dsn);

EOF

%build
#nothing to do

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/cube-statsd-backend
cp -pr README.md package.json lib %{buildroot}%{nodejs_sitelib}/cube-statsd-backend

%nodejs_symlink_deps

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/cube-statsd-backend

%changelog
* Thu Dec 18 2014 Daniel Spinozzi <dspinoz@gmail.com> - 0.0.1-1
- packaged for installation on redhat using epel nodejs
