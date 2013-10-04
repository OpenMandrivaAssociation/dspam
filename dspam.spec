%define _disable_ld_no_undefined 1

%define	major 7
%define libname %mklibname dspam %{major}
%define develname %mklibname dspam -d

Summary:	A library and Mail Delivery Agent for Bayesian spam filtering
Name:		dspam
Version:	3.10.1
Release:	2
License:	GPL
Group:		System/Servers
URL:		http://dspam.nuclearelephant.com/
Source0:	http://dspam.nuclearelephant.com/sources/%{name}-%{version}.tar.gz
Source1:	dspam_sa_trainer.tar.bz2
Source2:	dspam.cf
Source3:	dspam.cron
Source4:	dspam.sysconfig
Source5:	dspam.init
Patch0:		dspam-modules.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires:   apache-mod_socache_shmcb
Requires:	clamav clamd
BuildRequires:	autoconf2.5
BuildRequires:	automake
BuildRequires:	mysql-devel
BuildRequires:	sqlite3-devel
BuildRequires:	postgresql-devel
BuildRequires:	openldap-devel
BuildRequires:	libtool
#BuildConflicts:	sqlite-devel
Obsoletes:	dspam-amavis
Obsoletes:	dspam-db4
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
DSPAM (as in De-Spam) is an open-source project to create a new
kind of anti-spam mechanism, and is currently effective as both a
server-side agent for UNIX email servers and a developer's library
for mail clients, other anti-spam tools, and similar projects
requiring drop-in spam filtering.

The DSPAM agent masquerades as the email server's local delivery
agent and filters/learns spams using an advanced Bayesian
statistical approach (based on Baye's theorem of combined
probabilities) which provides an administratively
maintenance-free, easy-learning Anti-Spam service custom tailored
to each individual user's behavior. Advanced because on top of
standard Bayesian filtering is also incorporated the use of
Chained Tokens, de-obfuscation, and other enhancements. DSPAM
works great with Sendmail and Exim, and should work well with
any other MTA that supports an external local delivery agent
(postfix, qmail, etc.)

%package -n	%{libname}
Summary:	A library and Mail Delivery Agent for Bayesian spam filtering
Group:         	System/Libraries
Conflicts:	%{mklibname dspam 5}
Conflicts:	%{mklibname dspam 6}
Conflicts:	%{mklibname dspamdb4 6}
Conflicts:	%{mklibname dspamamavis 6}

%description -n	%{libname}
DSPAM (as in De-Spam) is an open-source project to create a new
kind of anti-spam mechanism, and is currently effective as both a
server-side agent for UNIX email servers and a developer's library
for mail clients, other anti-spam tools, and similar projects
requiring drop-in spam filtering.

The DSPAM agent masquerades as the email server's local delivery
agent and filters/learns spams using an advanced Bayesian
statistical approach (based on Baye's theorem of combined
probabilities) which provides an administratively
maintenance-free, easy-learning Anti-Spam service custom tailored
to each individual user's behavior. Advanced because on top of
standard Bayesian filtering is also incorporated the use of
Chained Tokens, de-obfuscation, and other enhancements. DSPAM
works great with Sendmail and Exim, and should work well with
any other MTA that supports an external local delivery agent
(postfix, qmail, etc.)

%package -n	%{develname}
Summary:	Development library and header files for the %{name} library
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel lib%{name}-devel
Obsoletes:	%{mklibname dspam 5 -d}
Obsoletes:	%{mklibname dspam 6 -d}
Obsoletes:	%{mklibname dspam 7 -d}

%description -n	%{develname}
DSPAM has had its core engine moved into a separate library,
libdspam. This library can be used by developers to provide
'drop-in' spam filtering for their mail client applications,
other anti-spam tools, or similar projects. 

%package	backend-mysql
Summary:	The mysql driver for dspam
Group:		System/Servers
Requires:	%{name} = %{version}
Obsoletes:	dspam-mysql
Obsoletes:	%{mklibname dspammysql 6}

%description	backend-mysql
The mysql driver for dspam

%package	backend-pgsql
Summary:	The pgsql driver for dspam
Group:		System/Servers
Requires:	%{name} = %{version}
Obsoletes:	dspam-pgsql
Obsoletes:	%{mklibname dspampgsql 6}

%description	backend-pgsql
The pgsql driver for dspam

%package	backend-sqlite3
Summary:	The sqlite3 driver for dspam
Group:		System/Servers
Requires:	%{name} = %{version}

%description	backend-sqlite3
The sqlite3 driver for dspam

%package	cgi
Summary:	Web administration GUI for DSPAM
Group:		System/Servers
Requires:	apache
Requires:	%{name} = %{version}

%description	cgi
Web administration GUI for DSPAM.

%prep

%setup -q -n %{name}-%{version} -a1
%patch0 -p1

# instead of maintaining patches...
find -type f -name "Makefile*" | xargs perl -pi -e "s|-static||g"

cp %{SOURCE2} dspam.cf
cp %{SOURCE3} dspam.cron
cp %{SOURCE4} dspam.sysconfig
cp %{SOURCE5} dspam.init

%build
export WANT_AUTOCONF_2_5=1
rm -f configure
autoreconf -fis
ln -snf %{_bindir}/libtool .

#sh ./autogen.sh

%configure2_5x \
    --enable-daemon \
    --enable-ldap \
    --enable-trusted-user-security \
    --enable-clamav \
    --enable-neural-networking \
    --enable-long-usernames \
    --enable-domain-scale \
    --enable-virtual-users \
    --with-dspam-home=%{_localstatedir}/lib/dspam \
    --with-logdir=/var/log/dspam \
    --with-storage-driver=hash_drv,mysql_drv,pgsql_drv,sqlite3_drv \
    --with-mysql-includes=%{_includedir}/mysql --with-mysql-libraries=%{_libdir} \
    --with-pgsql-includes=%{_includedir} --with-pgsql-libraries=%{_libdir} \
    --with-sqlite3-includes=%{_includedir} --with-sqlite3-libraries=%{_libdir}

%install
rm -rf %{buildroot} 

# make some dirs
install -d %{buildroot}%{_includedir}/dspam
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/mail/spamassassin
install -d %{buildroot}%{_sysconfdir}/cron.daily
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_sysconfdir}/ld.so.conf.d
install -d %{buildroot}%{_libdir}/dspam
install -d %{buildroot}%{_localstatedir}/lib/dspam/data
install -d %{buildroot}/var/log/dspam
install -d %{buildroot}/var/run/dspam
install -d %{buildroot}/var/www/icons
install -d %{buildroot}%{_datadir}/dspam/cgi-bin/templates
install -d %{buildroot}%{_datadir}/dspam-sqlite3
install -d %{buildroot}%{_datadir}/dspam-mysql
install -d %{buildroot}%{_datadir}/dspam-pgsql

%makeinstall_std

# install promo icon
install -m0644 webui/htdocs/dspam-logo-small.gif %{buildroot}/var/www/icons/dspam.gif

# install /etc stuff
install -m0755 dspam.cron %{buildroot}%{_sysconfdir}/cron.daily/dspam
install -m0644 dspam.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/dspam
install -m0755 dspam.init %{buildroot}%{_initrddir}/dspam

# nuke unwanted devel files
rm -f %{buildroot}%{_libdir}/dspam/lib*_drv.*a

# install sql stuff
install -m0644 src/tools.sqlite_drv/*.sql %{buildroot}%{_datadir}/dspam-sqlite3/
install -m0644 src/tools.mysql_drv/*.sql %{buildroot}%{_datadir}/dspam-mysql/
install -m0644 src/tools.pgsql_drv/*.sql %{buildroot}%{_datadir}/dspam-pgsql/

# install the cgi stuff
install -m0755 webui/cgi-bin/*.cgi %{buildroot}%{_datadir}/dspam/cgi-bin/
install -m0755 webui/cgi-bin/configure.pl %{buildroot}%{_datadir}/dspam/cgi-bin/
install -m0644 webui/cgi-bin/*.txt %{buildroot}%{_datadir}/dspam/cgi-bin/
install -m0644 webui/cgi-bin/default.prefs %{buildroot}%{_datadir}/dspam/cgi-bin/
install -m0644 webui/cgi-bin/admins %{buildroot}%{_datadir}/dspam/cgi-bin/
install -m0644 webui/htdocs/*.css %{buildroot}%{_datadir}/dspam/cgi-bin/
install -m0644 webui/htdocs/*.gif %{buildroot}%{_datadir}/dspam/cgi-bin/
install -m0644 webui/cgi-bin/templates/*.html %{buildroot}%{_datadir}/dspam/cgi-bin/templates/

# fix webroot
perl -pi -e "s|\"\/\"\;|\"\/dspam\"\;|g" %{buildroot}%{_datadir}/dspam/cgi-bin/configure.pl

cat > dspam.apache2 << EOF

Alias /dspam %{_datadir}/dspam/cgi-bin

<Directory %{_datadir}/dspam/cgi-bin/>

    Options ExecCGI
    AllowOverride Limit AuthConfig
    DirectoryIndex dspam.cgi

    Require host 127.0.0.1

    AuthUserFile %{_datadir}/dspam/cgi-bin/.htpasswd
    AuthGroupFile /dev/null
    AuthName "Authorization required"
    AuthType Basic

    <Limit GET>
	require user root
	require user dspamadmin
    </Limit>

</Directory>
EOF
install -m0644 dspam.apache2 %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/dspam.conf
echo "dspamadmin:h7Sr5nPztyPjU" > %{buildroot}%{_datadir}/dspam/cgi-bin/.htpasswd
echo "dspamadmin" >> %{buildroot}%{_datadir}/dspam/cgi-bin/admins

cat > dspam.logrotate << EOF
/var/log/dspam/*.log {
    missingok
    monthly
    compress
    postrotate
	/bin/kill -HUP \`cat /var/run/dspam/dspam.pid 2> /dev/null\` || /bin/true
    endscript
}
EOF
install -m0644 dspam.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/dspam

# fix strange perms (strip cannot access setuid/sgid files...)
chmod 755 %{buildroot}%{_bindir}/*

# install spamassassin stuff
install -m0644 dspam.cf %{buildroot}%{_sysconfdir}/mail/spamassassin

# fix default config (patches won't apply here...)
perl -pi -e "s|^#ServerDomainSocketPath.*|ServerDomainSocketPath \"%{_localstatedir}/lib/dspam/dspam\.sock\"|g" %{buildroot}%{_sysconfdir}/dspam.conf
perl -pi -e "s|^#ClientHost.*|ClientHost \"%{_localstatedir}/lib/dspam/dspam\.sock\"|g" %{buildroot}%{_sysconfdir}/dspam.conf
perl -pi -e "s|^#ServerPID.*|ServerPID \"/var/run/dspam/dspam\.pid\"|g" %{buildroot}%{_sysconfdir}/dspam.conf
perl -pi -e "s|^#ServerMode.*|ServerMode dspam|g" %{buildroot}%{_sysconfdir}/dspam.conf

# fix strange perms
chmod 644 doc/*

# provide a  README.urpmi file
cat > README.urpmi << EOF

Due huge changes in the source an upgrade from 3.4.x to 3.6.x has to be done 
manually, please read these files:

%{_docdir}/%{name}-%{version}/RELEASE.NOTES
%{_docdir}/%{name}-%{version}/UPGRADING

The previous 3.4.x packages was specially handcrafted so that you could use each
driver and even toggle between them, or use them simultaneousely. This is not
nessesary anymore and that magic has therefore been removed.

The Berkley-DB backend driver has been removed as it is prone to give errors due 
lack of thread safety as outlined in the dspam documentation.

The amavis-new tailored package has been removed, it may reappear later on.

You will have to define a proper cron command to use for daily cleanups. Look
in the %{_sysconfdir}/sysconfig/dspam file for some examples.

For example when executing dspam with the mysql driver it is possible it will
complain that it cannot find a %{_localstatedir}/lib/dspam/mysql.data file. This
is for backward compatibility. Do not use this file, edit the %{_sysconfdir}/dspam.conf
file instead.

The dspam-cgi web interface is password protected and only accessable from 127.0.0.1,
login as dspamadmin (l/p=dspamadmin) and change this ASAP in the 
%{_datadir}/dspam/cgi-bin/.htpasswd file. Preferably you should use some other
authentication mechanish.
EOF

echo "%{_libdir}/dspam" > %{buildroot}%{_sysconfdir}/ld.so.conf.d/dspam.conf

%post
%_post_service dspam

%preun
%_preun_service dspam

%post cgi
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi
 
%postun cgi
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%if "%{distribution}" == "Mandriva Linux"
	%if %mdkversion < 200900
		%post -n %{libname} -p /sbin/ldconfig

		%postun -n %{libname} -p /sbin/ldconfig

		%post backend-mysql -p /sbin/ldconfig

		%postun backend-mysql -p /sbin/ldconfig

		%post backend-pgsql -p /sbin/ldconfig

		%postun backend-pgsql -p /sbin/ldconfig

		%post backend-sqlite3 -p /sbin/ldconfig

		%postun backend-sqlite3 -p /sbin/ldconfig
	%endif
%endif

%clean
rm -rf %{buildroot} 

%files
%defattr(-,root,root)
%doc README* RELEASE.NOTES CHANGELOG txt/*.txt dspam_sa_trainer
%doc doc/courier.txt doc/exim.txt doc/markov.txt doc/pop3filter.txt
%doc doc/postfix.txt doc/qmail.txt doc/relay.txt doc/sendmail.txt
%attr(0755,root,root) %{_initrddir}/dspam
%attr(0755,root,root) %{_sysconfdir}/cron.daily/dspam
%attr(0644,root,mail) %config(noreplace) %{_sysconfdir}/dspam.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/dspam
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/dspam
%attr(0644,root,mail) %config(noreplace) %{_sysconfdir}/mail/spamassassin/dspam.cf
%attr(0644,root,mail) %config(noreplace) %{_sysconfdir}/ld.so.conf.d/dspam.conf
%attr(0755,root,root) %{_bindir}/cssclean
%attr(0755,root,root) %{_bindir}/csscompress
%attr(0755,root,root) %{_bindir}/cssconvert
%attr(0755,root,root) %{_bindir}/cssstat
%attr(0755,root,mail) %{_bindir}/dspam_admin
%attr(0755,root,mail) %{_bindir}/dspam
%attr(0755,root,root) %{_bindir}/dspam_2sql
%attr(0755,root,root) %{_bindir}/dspam_clean
%attr(0755,root,root) %{_bindir}/dspam_crc
%attr(0755,root,root) %{_bindir}/dspamc
%attr(0755,root,root) %{_bindir}/dspam_dump
%attr(0755,root,root) %{_bindir}/dspam_logrotate
%attr(0755,root,root) %{_bindir}/dspam_merge
%attr(0755,root,root) %{_bindir}/dspam_stats
%attr(0755,root,root) %{_bindir}/dspam_train
%attr(0755,root,root) %{_bindir}/dspam_notify
%attr(0644,root,root) %{_mandir}/man1/dspam.1*
%attr(0644,root,root) %{_mandir}/man1/dspam_clean.1*
%attr(0644,root,root) %{_mandir}/man1/dspam_dump.1*
%attr(0644,root,root) %{_mandir}/man1/dspam_merge.1*
%attr(0644,root,root) %{_mandir}/man1/dspam_stats.1*
%attr(0644,root,root) %{_mandir}/man1/dspam_train.1*
%attr(0644,root,root) %{_mandir}/man1/dspam_admin.1*
%attr(0644,root,root) %{_mandir}/man1/dspam_crc.1*
%attr(0644,root,root) %{_mandir}/man1/dspam_logrotate.1*
%attr(0644,root,root) /var/www/icons/dspam.gif
%dir %attr(0750,root,mail) %{_localstatedir}/lib/dspam
%dir %attr(0750,root,mail) %{_localstatedir}/lib/dspam/data
%dir %attr(0755,root,root) %{_datadir}/dspam
%dir %attr(0750,root,mail) /var/log/dspam
%dir %attr(0750,root,root) /var/run/dspam

%files -n %{libname}
%defattr(-,root,root)
%attr(0755,root,root) %{_libdir}/libdspam.so.*
%attr(0755,root,root) %{_libdir}/dspam/libhash_drv.so

%files -n %{develname}
%defattr(-,root,root)
%attr(0755,root,root) %{_libdir}/libdspam.so
%attr(0644,root,root) %{_libdir}/libdspam.*a
%{_includedir}/dspam
%attr(0644,root,root) %{_libdir}/pkgconfig/dspam.pc
%attr(0644,root,root) %{_mandir}/man3/*

%files backend-mysql
%defattr(-,root,root)
%doc doc/mysql_drv.txt
%attr(0755,root,root) %{_libdir}/dspam/libmysql_drv.so
%dir %attr(0755,root,root) %{_datadir}/dspam-mysql
%attr(0644,root,root) %{_datadir}/dspam-mysql/*

%files backend-pgsql
%defattr(-,root,root)
%doc doc/pgsql_drv.txt
%attr(0755,root,root) %{_libdir}/dspam/libpgsql_drv.so
%attr(0755,root,root) %{_bindir}/dspam_pg2int8
%dir %attr(0755,root,root) %{_datadir}/dspam-pgsql
%attr(0644,root,root) %{_datadir}/dspam-pgsql/*

%files backend-sqlite3
%defattr(-,root,root)
%doc doc/sqlite_drv.txt
%attr(0755,root,root) %{_libdir}/dspam/libsqlite3_drv.so
%{_datadir}/dspam-sqlite3

%files cgi
%defattr(-,root,root)
%dir %attr(0755,root,root) %{_datadir}/dspam/cgi-bin
%dir %attr(0755,root,root) %{_datadir}/dspam/cgi-bin/templates
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/dspam.conf
%attr(0644,root,root) %config(noreplace) %{_datadir}/dspam/cgi-bin/default.prefs
%attr(0644,root,root) %config(noreplace) %{_datadir}/dspam/cgi-bin/admins
%attr(0644,root,root) %config(noreplace) %{_datadir}/dspam/cgi-bin/.htpasswd
%attr(0644,root,root) %{_datadir}/dspam/cgi-bin/*.txt
%attr(0644,root,root) %{_datadir}/dspam/cgi-bin/*.gif
%attr(0644,root,root) %{_datadir}/dspam/cgi-bin/*.css
%attr(0755,root,root) %{_datadir}/dspam/cgi-bin/*.cgi
%attr(0755,root,root) %{_datadir}/dspam/cgi-bin/*.pl
%attr(0644,root,root) %{_datadir}/dspam/cgi-bin/templates/*.html


%changelog
* Sun Aug 14 2011 Oden Eriksson <oeriksson@mandriva.com> 3.10.1-1mdv2012.0
+ Revision: 694462
- 3.10.1

* Thu Aug 04 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.10.0-3
+ Revision: 693119
- trying to make this SPEC compatible with mageia so it will be easier for me

* Thu Aug 04 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.10.0-2
+ Revision: 693118
- Init LSB compatible
- 3.10.0
  P0 rediffed

  + Oden Eriksson <oeriksson@mandriva.com>
    - relink against libmysqlclient.so.18

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 3.9.0-8mdv2011.0
+ Revision: 627772
- don't force the usage of automake1.7

* Sat Jan 01 2011 Oden Eriksson <oeriksson@mandriva.com> 3.9.0-7mdv2011.0
+ Revision: 627220
- rebuilt against mysql-5.5.8 libs, again

* Thu Dec 30 2010 Oden Eriksson <oeriksson@mandriva.com> 3.9.0-6mdv2011.0
+ Revision: 626514
- rebuilt against mysql-5.5.8 libs

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 3.9.0-4mdv2011.0
+ Revision: 610285
- rebuild

* Tue Feb 23 2010 Oden Eriksson <oeriksson@mandriva.com> 3.9.0-3mdv2010.1
+ Revision: 510219
- rebuild
- not really unmaintained...

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - unmaintained webapp cleaning

* Thu Feb 18 2010 Oden Eriksson <oeriksson@mandriva.com> 3.9.0-2mdv2010.1
+ Revision: 507483
- rebuild

* Wed Jan 13 2010 Oden Eriksson <oeriksson@mandriva.com> 3.9.0-1mdv2010.1
+ Revision: 490638
- 3.9.0
- fix deps (libtool)
- fix build
- rebuild

* Sat Dec 06 2008 Oden Eriksson <oeriksson@mandriva.com> 3.8.0-5mdv2009.1
+ Revision: 311299
- rebuilt against mysql-5.1.30 libs

* Tue Sep 30 2008 Oden Eriksson <oeriksson@mandriva.com> 3.8.0-4mdv2009.0
+ Revision: 290069
- fix #35349 (/etc/logrotate.d/dspam in wrong)

* Sun Jul 20 2008 Oden Eriksson <oeriksson@mandriva.com> 3.8.0-3mdv2009.0
+ Revision: 238913
- fix linkage

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Mon Dec 24 2007 Oden Eriksson <oeriksson@mandriva.com> 3.8.0-2mdv2008.1
+ Revision: 137505
- rebuilt against openldap-2.4.7 libs

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Sep 06 2007 Oden Eriksson <oeriksson@mandriva.com> 3.8.0-1mdv2008.0
+ Revision: 80906
- 3.6.8
- rediffed P0
- conform to the 2008 specs


* Fri Mar 02 2007 Oden Eriksson <oeriksson@mandriva.com> 3.6.8-3mdv2007.0
+ Revision: 131429
- rebuild
- bunzip sources

* Fri Dec 22 2006 Oden Eriksson <oeriksson@mandriva.com> 3.6.8-2mdv2007.1
+ Revision: 101696
- Import dspam

* Tue Sep 05 2006 Oden Eriksson <oeriksson@mandriva.com> 3.6.8-1mdv2007.0
- rebuilt against MySQL-5.0.24a-1mdv2007.0 due to ABI changes

* Sat Jun 10 2006 Oden Eriksson <oeriksson@mandriva.com> 3.6.8-1mdv2007.0
- 3.6.8

* Mon May 15 2006 Oden Eriksson <oeriksson@mandriva.com> 3.6.6-2mdk
- rebuild

* Mon May 15 2006 Oden Eriksson <oeriksson@mandriva.com> 3.6.6-1mdk
- 3.6.6
- rediffed P0
- fix the apache config

* Wed Apr 26 2006 Oden Eriksson <oeriksson@mandriva.com> 3.6.5-1mdk
- 3.6.5 (Minor bugfixes)

* Mon Feb 13 2006 Oden Eriksson <oeriksson@mandriva.com> 3.6.4-1mdk
- 3.6.4 (Minor bugfixes)

* Thu Jan 26 2006 Oden Eriksson <oeriksson@mandriva.com> 3.6.3-2mdk
- drop the "--enable-preferences-extension" as it's not supported by
  all the backends (fix #19470)

* Wed Jan 18 2006 Oden Eriksson <oeriksson@mandriva.com> 3.6.3-1mdk
- 3.6.3

* Tue Nov 29 2005 Oden Eriksson <oeriksson@mandriva.com> 3.6.2-1mdk
- 3.6.2 (Major bugfixes)

* Thu Nov 17 2005 Oden Eriksson <oeriksson@mandriva.com> 3.6.1-2mdk
- since we remove rpath use /etc/ld.so.conf.d/dspam.conf (#19470)

* Tue Nov 08 2005 Oden Eriksson <oeriksson@mandriva.com> 3.6.1-1mdk
- 3.6.1 (Minor bugfixes)

* Sun Oct 30 2005 Oden Eriksson <oeriksson@mandriva.com> 3.6.0-3mdk
- rebuilt against MySQL-5.0.15

* Sun Oct 23 2005 Oden Eriksson <oeriksson@mandriva.com> 3.6.0-2mdk
- fixed P0
- make it build on LE too

* Wed Oct 19 2005 Oden Eriksson <oeriksson@mandriva.com> 3.6.0-1mdk
- 3.6.0
- major spec file rework due huge changes in the source

* Sun Aug 14 2005 Oden Eriksson <oeriksson@mandriva.com> 3.4.9-1mdk
- fix #17511

* Wed Jun 15 2005 Oden Eriksson <oeriksson@mandriva.com> 3.4.8-1mdk
- 3.4.8 (Minor bugfixes)

* Sat Jun 04 2005 Oden Eriksson <oeriksson@mandriva.com> 3.4.7-1mdk
- 3.4.7
- use new rpm-4.4.x pre,post magic
- fix new apache config locations

* Tue May 10 2005 Oden Eriksson <oeriksson@mandriva.com> 3.4.6-1mdk
- 3.4.6
- build it against sqlite 3

* Wed Apr 27 2005 Oden Eriksson <oeriksson@mandriva.com> 3.4.5-1mdk
- 3.4.5

* Thu Apr 21 2005 Oden Eriksson <oeriksson@mandriva.com> 3.4.3-2mdk
- rebuilt against new postgresql libs

* Wed Apr 13 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 3.4.3-1mdk
- 3.4.3

* Thu Mar 31 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 3.4.2-1mdk
- 3.4.2

* Tue Mar 15 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 3.4.0-2mdk
- fix a bug in the update-alternatives stuff

* Tue Mar 15 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 3.4.0-1mdk
- 3.4.0
- fix the update-alternatives stuff, great thanks goes to Guillaume
  Rousse for explaining the update-alternatives.
- major spec file and overall changes
- added the cgi stuff as a sub package

* Sat Mar 12 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 3.2.7-2mdk
- fix #14010 and #12399 
- own directories
- use the %%mkrel macro

* Sat Feb 19 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 3.2.7-1mdk
- 3.2.7

* Mon Jan 24 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 3.2.5-2mdk
- rebuilt against MySQL-4.1.x system libs

* Wed Jan 19 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 3.2.5-1mdk
- 3.2.5

* Mon Jan 03 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 3.2.4-1mdk
- 3.2.4
- revert latest "lib64 fixes"

* Tue Dec 28 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 3.2.3-4mdk
- lib64 fixes

* Thu Dec 23 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 3.2.3-3mdk
- fix deps

* Thu Dec 23 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 3.2.3-2mdk
- provide binaries with different drivers
- added amavis-new + spamassassin integrations after ideas by Giuseppe Ghibo

* Mon Nov 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 3.2.3-1mdk
- 3.2.3

* Mon Nov 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 3.2.2-1mdk
- 3.2.2

* Mon Nov 01 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 3.2.1-1mdk
- 3.2.1
- drop P1, it's fixed upstream

* Sun Oct 31 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 3.2.0-2mdk
- make it compile on 9.2/10.0
- make the devel package obsolete the older one

* Sun Oct 24 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 3.2.0-1mdk
- 3.2.0
- fix P0
- new %%{major} (again!)
- misc spec file fixes
- drop the weekly purge script

* Fri Jun 18 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 3.0.0-1mdk
- 3.0.0
- fix P0
- new %%{major} (again!)
- use domain-scale instead
- two more binaries is gone

* Sat Apr 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.10.3-1mdk
- 2.10.3

* Sun Mar 07 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.10-0.2mdk
- 2.10-RC2

