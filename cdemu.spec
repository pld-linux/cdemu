#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	smp		# without smp packages
%bcond_without	kernel		# without kernel packages
%bcond_with	verbose		# verbose build (V=1)
%bcond_without	userspace	# don't build userspace tools
#
%define		_rel	0.1
Summary:	Simulate a CD drive + CD with just simple cue/bin files
Summary(pl):	Symulacja napêdu CD z p³ytk± przy u¿yciu plików cue/bin
Name:		cdemu
Version:	0.8
Release:	%{_rel}
License:	GPL v2
Group:		Applications/System
Source0:	http://dl.sourceforge.net/cdemu/%{name}-%{version}.tar.bz2
# Source0-md5:	e5e60f73caf168936c38f115ecf4a144
URL:		http://www.cdemu.org/
%if %{with userspace}
%pyrequires_eq	python-libs
BuildRequires:	python-devel
%endif
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 3:2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.153
%endif
Requires:	cdemu(kernel)
Requires:	dev >= 2.9.0-16
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CDemu is a kernel module for Linux. It is designed to simulate a CD
drive + CD with just simple cue/bin files, which are pretty common in
the Windows world. It includes an user space program to control the
kernel module. You can use it to watch an SVCD or mount the data track
of an bin/cue. However, for watching an SVCD, we would recommend
MPlayer which can play bin/cue images directly with the patch a friend
and I made for it (more under History).

This package includes userspace tools for %{name}.

%description -l pl
CDemu to modu³ j±dra Linuksa. Zosta³ zaprojektowany do symulowania
napêdu CD z p³ytk± przy u¿yciu plików cue/bin, które s± do¶æ popularne
w ¶wiecie windowsowym. Zawiera program dzia³aj±cy w przestrzeni
u¿ytkownika s³u¿±cy do kontroli pracy modu³u. Mo¿na u¿ywaæ go do
ogl±dania SVCD lub montowania ¶cie¿ek danych z bin/cue. Mimo to
autorzy do ogl±dania SVCD polecaj± raczej MPlayera ze swoj± ³atk±,
który mo¿e odtwarzaæ obrazy bin/cur bezpo¶rednio.

Ten pakiet zawiera narzêdzia u¿ytkownika dla %{name}.

%package -n kernel-misc-%{name}
Summary:	Linux driver for %{name}
Summary(pl):	Sterownik dla Linuksa do %{name}
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif
Provides:	cdemu(kernel)

%description -n kernel-misc-%{name}
This is driver for %{name} for Linux.

This package contains Linux module.

%description -n kernel-misc-%{name} -l pl
Sterownik dla Linuksa do %{name}.

Ten pakiet zawiera modu³ j±dra Linuksa.

%package -n kernel-smp-misc-%{name}
Summary:	Linux SMP driver for %{name}
Summary(pl):	Sterownik dla Linuksa SMP do %{name}
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif
Provides:	cdemu(kernel)

%description -n kernel-smp-misc-%{name}
This is driver for %{name} for Linux.

This package contains Linux SMP module.

%description -n kernel-smp-misc-%{name} -l pl
Sterownik dla Linuksa do %{name}.

Ten pakiet zawiera modu³ j±dra Linuksa SMP.

%prep
%setup -q

%build
%if %{with kernel}
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -rf include
	install -d o/include/linux
	ln -sf %{_kernelsrcdir}/config-$cfg o/.config
	ln -sf %{_kernelsrcdir}/Module.symvers.h o/Module.symvers
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h o/include/linux/autoconf.h
%if %{with dist_kernel}
	%{__make} -j1 -C %{_kernelsrcdir} O=$PWD/o prepare scripts
%else
	install -d o/include/config
	touch o/include/config/MARKER
	ln -sf %{_kernelsrcdir}/scripts o/scripts
%endif

	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		M=$PWD O=$PWD/o MK_INC=$PWD \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
		CC="%{__cc}" CPP="%{__cpp}" \
		M=$PWD O=$PWD/o MK_INC=$PWD \
		%{?with_verbose:V=1}

	mv cdemu{,-$cfg}.ko
done
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -d $RPM_BUILD_ROOT%{py_sitedir}
install libcdemu.py $RPM_BUILD_ROOT%{py_sitedir}/libcdemu.py
%py_comp $RPM_BUILD_ROOT
%py_ocomp $RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{py_sitedir}/libcdemu.py
install -d $RPM_BUILD_ROOT%{_bindir}
install cdemu $RPM_BUILD_ROOT%{_bindir}/cdemu
%endif

%if %{with kernel}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc
install cdemu-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/cdemu.ko
%if %{with smp} && %{with dist_kernel}
install cdemu-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/cdemu.ko
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-misc-%{name}
%depmod %{_kernel_ver}

%postun	-n kernel-misc-%{name}
%depmod %{_kernel_ver}

%post	-n kernel-smp-misc-%{name}
%depmod %{_kernel_ver}smp

%postun	-n kernel-smp-misc-%{name}
%depmod %{_kernel_ver}smp

%if %{with kernel}
%files -n kernel-misc-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-misc-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/*.ko*
%endif
%endif

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog TODO
%attr(755,root,root) %{_bindir}/cdemu
%{py_sitedir}/*.py[co]
%endif
