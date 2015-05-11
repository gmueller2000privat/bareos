%define __strip %{_mingw64_strip}
%define __objdump %{_mingw64_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw64_findrequires}
%define __find_provides %{_mingw64_findprovides}
%define __os_install_post %{_mingw64_debug_install_post} \
                          %{_mingw64_install_post}



#!BuildIgnore: post-build-checks
Name:           winbareos-nsi
Version:        15.2.0
Release:        0
Summary:        bareos
License:        LGPLv2+
Group:          Development/Libraries
URL:            http://bareos.org
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  mingw32-filesystem
BuildRequires:  mingw64-filesystem
BuildRequires:  mingw64-cross-nsis

BuildRequires:  mingw32-openssl
BuildRequires:  mingw64-openssl

BuildRequires:  mingw32-libopenssl
BuildRequires:  mingw64-libopenssl

BuildRequires:  mingw32-sed
BuildRequires:  mingw64-sed


BuildRequires:  sed
BuildRequires:  vim, procps, bc


BuildRequires:  mingw32-winbareos-prevista = %{version}
BuildRequires:  mingw64-winbareos-prevista = %{version}

BuildRequires:  mingw32-winbareos-postvista = %{version}
BuildRequires:  mingw64-winbareos-postvista = %{version}

BuildRequires:  mingw32-winbareos-prevista-debug = %{version}
BuildRequires:  mingw64-winbareos-prevista-debug = %{version}

BuildRequires:  mingw32-winbareos-postvista-debug = %{version}
BuildRequires:  mingw64-winbareos-postvista-debug = %{version}

BuildRequires:  mingw-debugsrc-devel = %{version}


BuildRequires:  mingw32-libgcc
BuildRequires:  mingw64-libgcc

BuildRequires:  mingw32-readline
BuildRequires:  mingw64-readline

BuildRequires:  mingw32-libstdc++
BuildRequires:  mingw64-libstdc++

BuildRequires:  mingw32-pthreads
BuildRequires:  mingw64-pthreads

BuildRequires:  mingw32-libqt4
BuildRequires:  mingw64-libqt4

BuildRequires:  mingw32-lzo
BuildRequires:  mingw64-lzo

BuildRequires:  mingw32-libfastlz
BuildRequires:  mingw64-libfastlz

BuildRequires:  osslsigncode
BuildRequires:  mingw32-cmocka
BuildRequires:  mingw64-cmocka

Source1:         winbareos.nsi
Source2:         clientdialog.ini
Source3:         directordialog.ini
Source4:         storagedialog.ini
Source5:         KillProcWMI.dll
Source6:         bareos.ico
Source7:         AccessControl.dll
Source8:         LogEx.dll
Source9:         databasedialog.ini

# code signing cert
Source10:        ia.p12
Source11:        signpassword
%description
bareos

%package devel
Summary:        bareos
Group:          Development/Libraries


%description devel
bareos

#{_mingw32_debug_package}

%prep


%build
for flavor in postvista postvista-debug prevista prevista-debug;
do
   mkdir -p $RPM_BUILD_ROOT/$flavor/nsisplugins

   cp %SOURCE5 $RPM_BUILD_ROOT/$flavor/nsisplugins  #  KillProcWMI
   cp %SOURCE7 $RPM_BUILD_ROOT/$flavor/nsisplugins  #  AccessControl
   cp %SOURCE8 $RPM_BUILD_ROOT/$flavor/nsisplugins  #  LogEx

   for BITS in 32 64; do
      mkdir -p $RPM_BUILD_ROOT/$flavor/release${BITS}

      # copy the sql ddls over
      cp -av /etc/$flavor/mingw${BITS}-winbareos/ddl $RPM_BUILD_ROOT/$flavor/release${BITS}

      # copy the sources over if we create debug package
      WIN_DEBUG=$(echo $flavor | grep debug >/dev/null && echo yes || echo no)
      if [ "$WIN_DEBUG" == "yes" ]; then
      cp -av /bareos*  $RPM_BUILD_ROOT/$flavor/release${BITS}
      fi

   done

   for file in \
      bareos-fd.exe \
      bareos-sd.exe \
      bareos-dir.exe \
      bareos-dbcheck.exe \
      bconsole.exe \
      bsmtp.exe \
      bregex.exe \
      bwild.exe \
      btape.exe \
      bls.exe \
      bextract.exe \
      bscan.exe \
      bareos-tray-monitor.exe \
      bat.exe \
      bpipe-fd.dll \
      mssqlvdi-fd.dll \
      autoxflate-sd.dll \
      libbareos.dll \
      libbareosfind.dll \
      libbareoslmdb.dll \
      libbareoscats-postgresql.dll libbareoscats-sqlite3.dll libbareoscats.dll\
      libbareossd.dll \
      test_lib.exe \
      test_findlib.exe ;
   do
      cp %{_mingw32_bindir}/$flavor/$file $RPM_BUILD_ROOT/$flavor/release32
      cp %{_mingw64_bindir}/$flavor/$file $RPM_BUILD_ROOT/$flavor/release64

      osslsigncode verify -in $RPM_BUILD_ROOT/$flavor/release32/$file
      osslsigncode verify -in $RPM_BUILD_ROOT/$flavor/release64/$file
   done


   for file in \
      libcrypto-*.dll \
      libgcc_s_*-1.dll \
      libhistory6.dll \
      libreadline6.dll \
      libssl-*.dll \
      libstdc++-6.dll \
      libtermcap-0.dll \
      pthreadGCE2.dll \
      zlib1.dll \
      QtCore4.dll \
      QtGui4.dll \
      liblzo2-2.dll \
      libfastlz.dll \
      libpng*.dll \
      openssl.exe \
      libcmocka.dll \
      sed.exe;
   do
      cp %{_mingw32_bindir}/$file $RPM_BUILD_ROOT/$flavor/release32
      cp %{_mingw64_bindir}/$file $RPM_BUILD_ROOT/$flavor/release64
   done

   for BITS in 32 64; do

      for cfg in /etc/$flavor/mingw${BITS}-winbareos/*.conf; do
         cp $cfg $RPM_BUILD_ROOT/$flavor/release${BITS}
      done

      cp %SOURCE1 %SOURCE2 %SOURCE3 %SOURCE4 %SOURCE6 %SOURCE9 \
               %_sourcedir/LICENSE $RPM_BUILD_ROOT/$flavor/release${BITS}

      makensis -DVERSION=%version -DPRODUCT_VERSION=%version-%release -DBIT_WIDTH=${BITS} \
               -DWIN_DEBUG=${WIN_DEBUG} $RPM_BUILD_ROOT/$flavor/release${BITS}/winbareos.nsi
   done
done

%install

for flavor in postvista postvista-debug prevista prevista-debug;
do
   mkdir -p $RPM_BUILD_ROOT%{_mingw32_bindir}
   mkdir -p $RPM_BUILD_ROOT%{_mingw64_bindir}

   FLAVOR=`echo "%name" | sed 's/winbareos-nsi-//g'`
   DESCRIPTION="Bareos installer version %version"
   URL="http://www.bareos.com"

   for BITS in 32 64; do
      cp $RPM_BUILD_ROOT/$flavor/release${BITS}/Bareos*.exe \
           $RPM_BUILD_ROOT/winbareos-%version-$flavor-${BITS}-bit-r%release-unsigned.exe

      osslsigncode  -pkcs12 %SOURCE10 -pass `cat %SOURCE11` -n "${DESCRIPTION}" -i http://www.bareos.com/ \
                    -in  $RPM_BUILD_ROOT/winbareos-%version-$flavor-${BITS}-bit-r%release-unsigned.exe \
                    -out $RPM_BUILD_ROOT/winbareos-%version-$flavor-${BITS}-bit-r%release.exe

      osslsigncode verify -in $RPM_BUILD_ROOT/winbareos-%version-$flavor-${BITS}-bit-r%release.exe

      rm $RPM_BUILD_ROOT/winbareos-%version-$flavor-${BITS}-bit-r%release-unsigned.exe

      rm -R $RPM_BUILD_ROOT/$flavor/release${BITS}

   done

   rm -R $RPM_BUILD_ROOT/$flavor/nsisplugins
done

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
/winbareos-*.exe

#{_mingw32_bindir}
#{_mingw64_bindir}

%changelog
