# TODO:
#	- finish, kernel modules subpackages etc
Summary:	Simulate a CD drive + CD with just simple cue/bin files
Name:		cdemu
Version:	0.6
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://www.reviewedinfo.org/howtos/cdrecording/%{name}-%{version}_beta.tar.bz2
# Source0-md5:	1d58ee3989c0772d670732b1b10501c2
URL:		http://cdemu.sourceforge.net/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CDemu is a kernel module for Linux. It is designed to simulate a CD
drive + CD with just simple cue/bin files, which are pretty common in
the Windows world. It includes an user space program to control the
kernel module. You can use it to watch an SVCD or mount the data track
of an bin/cue. However, for watching an SVCD, we would recommend
MPlayer which can play bin/cue images directly with the patch a friend
and I made for it (more under History).

%prep
%setup -q -n %{name}-%{version}_beta

%build
ln -sf %{_kernelsrcdir}/config-up .config
install -d include/{linux,config}
ln -sf %{_kernelsrcdir}/include/linux/autoconf-up.h include/linux/autoconf.h
ln -sf %{_kernelsrcdir}/include/asm-%{_arch} include/asm
touch include/config/MARKER
%{__make} -C %{_kernelsrcdir} modules \
        SUBDIRS=$PWD \
        O=$PWD \
        V=1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog TODO
%attr(755,root,root) %{_bindir}/*
