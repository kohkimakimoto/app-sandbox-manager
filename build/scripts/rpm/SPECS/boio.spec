Name:           %{_product_name}
Version:        %{_product_version}

Release:        1.el%{_rhel_version}
Summary:        Another object storage server
Group:          Development/Tools
License:        MIT
Source0:        %{name}_linux_amd64.zip
Source1:        config.toml
Source2:        boio.sysconfig
Source3:        boio.service
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
Another object storage server

%prep
%setup -q -c

%install
mkdir -p %{buildroot}/%{_bindir}
cp %{name} %{buildroot}/%{_bindir}

mkdir -p %{buildroot}/%{_sysconfdir}/%{name}
cp %{SOURCE1} %{buildroot}/%{_sysconfdir}/boio/config.toml

mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
cp %{SOURCE2} %{buildroot}/%{_sysconfdir}/sysconfig/boio

mkdir -p %{buildroot}/var/lib/boio

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
mkdir -p %{buildroot}/%{_unitdir}
cp %{SOURCE3} %{buildroot}/%{_unitdir}/
%endif

%pre
getent group boio >/dev/null || groupadd -r boio
getent passwd boio >/dev/null || \
    useradd -r -g boio -d /var/lib/boio -s /sbin/nologin \
    -c "boio user" boio
exit 0

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
%post
%systemd_post boio.service

%preun
%systemd_preun boio.service
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%attr(755, root, root) %{_bindir}/%{name}
%dir %attr(755, boio, boio) /var/lib/boio
%config(noreplace) %{_sysconfdir}/boio/config.toml
%config(noreplace) %{_sysconfdir}/sysconfig/boio

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
%{_unitdir}/boio.service
%endif

%doc
