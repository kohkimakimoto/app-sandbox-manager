Name:           %{_product_name}
Version:        %{_product_version}

Release:        1.el%{_rhel_version}
Summary:        Handlers set for crun.
Group:          Development/Tools
License:        MIT
# this is a dummy file to create RPM without tar.
Source0:        empty.tar.bz2
Source1:        app-sandbox-manager
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
Sandbox manager for running applications.

%prep
%setup -q -c

%install
mkdir -p %{buildroot}/%{_bindir}
cp %{SOURCE1} %{buildroot}/%{_bindir}

%pre

%post

%preun

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%attr(755, root, root) %{_bindir}/app-sandbox-manager

%doc
