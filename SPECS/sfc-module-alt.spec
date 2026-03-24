%define vendor_name Solarflare
%define vendor_label solarflare
%define driver_name sfc

# XCP-ng: install to the override directory
%define module_dir override

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{driver_name}-module-alt
Version: 5.3.18.1012
Release: 1%{?dist}
License: GPL-2.0-only

# Extracted from https://www.amd.com/content/dam/amd/en/support/downloads/solarflare/drivers-software/linux/XN-201161-LS-5-Solarflare-NET-v5-driver-source-RPM.zip
Source0: sfc-5.3.18.1012.tar.gz

BuildRequires: gcc
BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n sfc-%{version}

%build
%{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd)/linux_net/drivers/net/ethernet/sfc KSRC=/lib/modules/%{kernel_version}/build modules

%install
%{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd)/linux_net/drivers/net/ethernet/sfc INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko

%changelog
* Fri Mar 20 2026 Tu Dinh <ngoc-tu.dinh@vates.tech> - 5.3.18.1012-1
- Initial package, version 5.3.18.1012
