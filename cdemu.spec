# TODO:
#	- finish, kernel modules subpackages etc
#
# Conditional build:
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace tools
#
Summary:	Simulate a CD drive + CD with just simple cue/bin files
Summary(pl):	Symulacja napêdu CD z p³ytk± przy u¿yciu plików cue/bin
Name:		cdemu
Version:	0.6
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://www.reviewedinfo.org/howtos/cdrecording/%{name}-%{version}_beta.tar.bz2
# Source0-md5:	1d58ee3989c0772d670732b1b10501c2
URL:		http://cdemu.sourceforge.net/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel-module-build}
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CDemu is a kernel module for Linux. It is designed to simulate a CD
drive + CD with just simple cue/bin files, which are pretty common in
the Windows world. It includes an user space program to control the
kernel module. You can use it to watch an SVCD or mount the data track
of an bin/cue. However, for watching an SVCD, we would recommend
MPlayer which can play bin/cue images directly with the patch a friend
and I made for it (more under History).

%description -l pl
CDemu to modu³ j±dra Linuksa. Zosta³ zaprojektowany do symulowania
napêdu CD z p³ytk± przy u¿yciu plików cue/bin, które s± do¶æ popularne
w ¶wiecie windowsowym. Zawiera program dzia³aj±cy w przestrzeni
u¿ytkownika s³u¿±cy do kontroli pracy modu³u. Mo¿na u¿ywaæ go do
ogl±dania SVCD lub montowania ¶cie¿ek danych z bin/cue. Mimo to
autorzy do ogl±dania SVCD polecaj± raczej MPlayera ze swoj± ³atk±,
który mo¿e odtwarzaæ obrazy bin/cur bezpo¶rednio.

%prep
%setup -q -n %{name}-%{version}_beta

%build
%if %{with kernel}
ln -sf %{_kernelsrcdir}/config-up .config
install -d include/{linux,config}
ln -sf %{_kernelsrcdir}/include/linux/autoconf-up.h include/linux/autoconf.h
ln -sf %{_kernelsrcdir}/include/asm-%{_arch} include/asm
touch include/config/MARKER
%{__make} -C %{_kernelsrcdir} modules \
	SUBDIRS=$PWD \
	O=$PWD \
	V=1
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog TODO
%attr(755,root,root) %{_bindir}/*
%endif
