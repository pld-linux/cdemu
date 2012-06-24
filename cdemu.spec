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
Summary(pl):	Symulacja nap�du CD z p�ytk� przy u�yciu plik�w cue/bin
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
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.330
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
CDemu to modu� j�dra Linuksa. Zosta� zaprojektowany do symulowania
nap�du CD z p�ytk� przy u�yciu plik�w cue/bin, kt�re s� do�� popularne
w �wiecie windowsowym. Zawiera program dzia�aj�cy w przestrzeni
u�ytkownika s�u��cy do kontroli pracy modu�u. Mo�na u�ywa� go do
ogl�dania SVCD lub montowania �cie�ek danych z bin/cue. Mimo to
autorzy do ogl�dania SVCD polecaj� raczej MPlayera ze swoj� �atk�,
kt�ry mo�e odtwarza� obrazy bin/cur bezpo�rednio.

Ten pakiet zawiera narz�dzia u�ytkownika dla %{name}.

%package -n kernel%{_alt_kernel}-misc-%{name}
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

%description -n kernel%{_alt_kernel}-misc-%{name}
This is driver for %{name} for Linux.

This package contains Linux module.

%description -n kernel%{_alt_kernel}-misc-%{name} -l pl
Sterownik dla Linuksa do %{name}.

Ten pakiet zawiera modu� j�dra Linuksa.

%package -n kernel%{_alt_kernel}-smp-misc-%{name}
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

%description -n kernel%{_alt_kernel}-smp-misc-%{name}
This is driver for %{name} for Linux.

This package contains Linux SMP module.

%description -n kernel%{_alt_kernel}-smp-misc-%{name} -l pl
Sterownik dla Linuksa do %{name}.

Ten pakiet zawiera modu� j�dra Linuksa SMP.

%prep
%setup -q
cat > Makefile <<'EOF'
obj-m := cdemu.o
cdemu-objs := cdemu_core.o cdemu_mod.o cdemu_proc.o
EOF

%build
%build_kernel_modules -m cdemu

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
%install_kernel_modules -m cdemu -d misc
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-misc-%{name}
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-misc-%{name}
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-smp-misc-%{name}
%depmod %{_kernel_ver}smp

%postun	-n kernel%{_alt_kernel}-smp-misc-%{name}
%depmod %{_kernel_ver}smp

%if %{with kernel}
%files -n kernel%{_alt_kernel}-misc-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/cdemu.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-misc-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/cdemu.ko*
%endif
%endif

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog TODO
%attr(755,root,root) %{_bindir}/cdemu
%{py_sitedir}/*.py[co]
%endif
