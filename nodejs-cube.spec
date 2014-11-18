%{?nodejs_find_provides_and_requires}

Name:           nodejs-cube
Version:        0.2.12
Release:        3%{?dist}
Summary:        Cube is a system for collecting timestamped events and deriving metrics.

Group:          Node
License:        Apache License, Version 2.0

URL:            http://square.github.io/cube/
Source0:        https://registry.npmjs.org/cube/-/cube-0.2.12.tgz

BuildArch:      noarch
ExclusiveArch:  %{ix86} x86_64 %{arm} noarch

Requires:       nodejs-ctype
BuildRequires:  nodejs-devel nodejs-vows nodejs-pegjs

%description
Cube is a system for collecting timestamped events and deriving metrics. 
By collecting events rather than metrics, Cube lets you compute aggregate 
statistics post hoc. It also enables richer analysis, such as quantiles 
and histograms of arbitrary event sets. Cube is built on MongoDB and 
available under the Apache License.

Want to learn more? See the wiki.

%package collectd
Summary:        Collectd configuration for posting events to cube
Requires:       collectd

%description collectd
Collectd configuration for posting events to cube

%prep
%setup -q -n package

patch <<EOF
--- Makefile.orig	2014-08-14 21:57:19.076924426 +0930
+++ Makefile	2014-08-14 21:57:37.110868644 +0930
@@ -1,5 +1,5 @@
-JS_TESTER = ./node_modules/vows/bin/vows
-PEG_COMPILER = ./node_modules/pegjs/bin/pegjs
+JS_TESTER = %{_bindir}/vows
+PEG_COMPILER = %{_bindir}/pegjs
 
 .PHONY: test

EOF


patch -p0 <<EOF
--- bin.orig/collector.js	2014-08-14 22:19:19.354877643 +0930
+++ bin/collector.js	2014-08-14 22:20:03.679190198 +0930
@@ -1,5 +1,7 @@
-var options = require("./collector-config"),
-    cube = require("../"),
+#!/usr/bin/env node
+
+var options = require("%{_sysconfdir}/cube/collector-config"),
+    cube = require("cube"),
     server = cube.server(options);
 
 server.register = function(db, endpoints) {
diff -ruN bin.orig/evaluator.js bin/evaluator.js
--- bin.orig/evaluator.js	2014-08-14 22:19:19.354877643 +0930
+++ bin/evaluator.js	2014-08-14 22:20:34.525930071 +0930
@@ -1,5 +1,7 @@
-var options = require("./evaluator-config"),
-    cube = require("../"),
+#!/usr/bin/env node
+
+var options = require("%{_sysconfdir}/cube/evaluator-config"),
+    cube = require("cube"),
     server = cube.server(options);
 
 server.register = function(db, endpoints) {
EOF


patch -p0 <<EOF
--- lib.orig/cube/server.js	2014-08-14 22:43:32.983917586 +0930
+++ lib/cube/server.js	2014-08-14 22:44:08.308170080 +0930
@@ -8,7 +8,7 @@
     database = require('./database');
 
 // And then this happened:
-websprocket.Connection = require("../../node_modules/websocket-server/lib/ws/connection");
+websprocket.Connection = require("websocket-server/lib/ws/connection");
 
 // Configuration for WebSocket requests.
 var wsOptions =  {
@@ -34,7 +34,7 @@
   var server = {},
       primary = http.createServer(),
       secondary = websprocket.createServer(),
-      file = new static.Server("static"),
+      file = new static.Server("%{nodejs_sitelib}/cube/static"),
       meta,
       endpoints = {ws: [], http: []},
       id = 0;
EOF

# allow query of all fields from event type
# use the syntax type(*)
# https://github.com/square/cube/pull/80
# requires a rebuild!
patch -p0 <<EOF
--- lib.orig/cube/event-expression.peg	2013-03-05 10:32:04.000000000 +1030
+++ lib/cube/event-expression.peg	2014-08-02 19:45:24.000000000 +0930
@@ -13,6 +13,10 @@
 
   function noop() {}
 
+function everything(fields) {
+  delete fields.t;
+}
+
   function filter(op) {
     return function(o, k, v) {
       var f = o[k];
@@ -90,7 +94,8 @@
   = op:filter_operator _ "(" _ member:event_member_expression _ "," _ value:literal _ ")" { return function(o) { op(o, member.field, value); }; }
 
 event_value_expression
-  = type:type _ "(" _ head:event_member_expression tail:(_ "," _ event_member_expression)* _ ")" { return compoundFields(type, head, tail); }
+  = type:type _ "(" _ "*" _ ")" { return {type: type, exists: noop, fields: everything}; }  
+  / type:type _ "(" _ head:event_member_expression tail:(_ "," _ event_member_expression)* _ ")" { return compoundFields(type, head, tail); }
   / type:type { return {type: type, exists: noop, fields: noop}; }
 
 event_member_expression
EOF
# update dependencies
patch <<EOF
--- package.json.orig	2014-08-17 11:56:29.028906242 +0930
+++ package.json	2014-08-17 11:56:44.621183483 +0930
@@ -18,7 +18,7 @@
   "dependencies": {
     "mongodb": "~1.3.18",
     "node-static": "0.6.5",
-    "pegjs": "0.7.0",
+    "pegjs": "0.6.2",
     "vows": "0.7.0",
     "websocket": "1.0.8",
     "websocket-server": "1.4.04"
EOF

# Event Subtyping
# Allow event types with dot notation ('.') to define sub-types
# Events are stored with main type (up to first dot), and then data field
# is modified to include sub type(s) 
# https://github.com/square/cube/pull/80
patch -p0 <<EOF
diff -ruN cube-0.2.12-orig/lib/cube/event.js cube-0.2.12/lib/cube/event.js
--- lib.orig/cube/event.js	2013-08-20 11:13:26.000000000 +0930
+++ lib/cube/event.js	2014-11-19 06:13:52.000000000 +1030
@@ -33,7 +33,15 @@
         type = request.type;
 
     // Validate the date and type.
-    if (!type_re.test(type)) return callback({error: "invalid type"}), -1;
+    var keys = type.split('.');
+    keys.forEach(function(t) {
+      if (!type_re.test(t)) {
+        return callback({error: "invalid type"}), -1;
+      }
+    });
+    var type = keys[0];
+    var key = keys.slice(1).join('.');
+    
     if (isNaN(time)) return callback({error: "invalid time"}), -1;
 
     // If an id is specified, promote it to Mongo's primary key.
@@ -41,7 +49,7 @@
     if ("id" in request) event._id = request.id;
 
     // If this is a known event type, save immediately.
-    if (type in knownByType) return save(type, event);
+    if (type in knownByType) return save(type, event, key);
 
     // If someone is already creating the event collection for this new type,
     // then append this event to the queue for later save.
@@ -77,7 +85,7 @@
       // Save any pending events to the new collection.
       function saveEvents() {
         knownByType[type] = true;
-        eventsToSaveByType[type].forEach(function(event) { save(type, event); });
+        eventsToSaveByType[type].forEach(function(event) { save(type, event, key); });
         delete eventsToSaveByType[type];
       }
     });
@@ -91,8 +99,32 @@
   // delay between saving the event and invalidating the metrics reduces the
   // likelihood of a race condition between when the events are read by the
   // evaluator and when the newly-computed metrics are saved.
-  function save(type, event) {
-    collection(type).events.save(event, handle);
+  function save(type, event, key) {
+    if (event._id !== undefined) {
+      var updater = {t: event.t};
+      updater[key !== '' ? 'd.' + key : 'd'] = event.d;
+      collection(type).events.update({_id: event._id}, {$set: updater}, {safe: true, upsert: true}, handle);
+    } else {
+
+      if (key !== '') {
+        // Convert sub-keys into event.d properties
+        var d = event.d;
+        delete event.d;
+
+        var prev = event['d'] = {};
+
+        var keys = key.split('.').forEach(function(k) {
+          prev = prev[ k ] = {};
+        });
+
+        Object.keys(d).forEach(function(p) {
+          prev[p] = d[p];
+        });
+      }
+      
+      collection(type).events.save(event, handle);
+    }
+    
     queueInvalidation(type, event);
   }
 
EOF

cat > collectd.conf <<EOF
LoadPlugin logfile
<Plugin logfile>
	LogLevel info
	File "/var/log/collectd.log"
	Timestamp true
</Plugin>

LoadPlugin write_http
<Plugin write_http>
	<URL "http://localhost:1080/collectd">
		Format "JSON"
	</URL>
</Plugin>
EOF

%build
make 

chmod +x bin/collector.js bin/evaluator.js

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/cube
mv bin/collector-config.js bin/evaluator-config.js %{buildroot}%{_sysconfdir}/cube

mkdir -p %{buildroot}%{nodejs_sitelib}/cube
cp -pr bin lib package.json LICENSE README.md static %{buildroot}%{nodejs_sitelib}/cube

mkdir -p %{buildroot}%{_bindir}
ln -sf %{nodejs_sitelib}/cube/bin/collector.js %{buildroot}%{_bindir}/cube-collector
ln -sf %{nodejs_sitelib}/cube/bin/evaluator.js %{buildroot}%{_bindir}/cube-evaluator

#collectd
install -D collectd.conf %{buildroot}%{_sysconfdir}/collectd.d/cube.conf


%nodejs_symlink_deps

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/cube
%config %_sysconfdir/cube/collector-config.js
%config %_sysconfdir/cube/evaluator-config.js
%{_bindir}/cube-collector
%{_bindir}/cube-evaluator

%files collectd
%config %_sysconfdir/collectd.d/cube.conf


%changelog
* Tue Nov 18 2014 Daniel Spinozzi <dspinoz@gmail.com> - 0.2.12-3
- Add pull request #86 to allow event subtyping
* Mon Aug 19 2014 Daniel Spinozzi <dspinoz@gmail.com> - 0.2.12-2
- optional package for posting collectd events to cube
* Mon Aug 11 2014 Daniel Spinozzi <dspinoz@gmail.com> - 0.2.12-1
- packaged for installation on redhat using epel nodejs
