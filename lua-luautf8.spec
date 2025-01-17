%global forgeurl https://github.com/starwing/luautf8
%global tag %{version}

%define lua_version %(lua -e 'print(_VERSION)' | cut -d ' ' -f 2)
%define lua_pkgdir %{_libdir}/lua/%{lua_version}

Name:      lua-luautf8
Version:   0.1.5
Release:   1
Summary:   A UTF-8 support module for Lua
Group:     Development/Other
License:   MIT
URL:       %{forgeurl}

%forgemeta
Source:    %{forgesource}

BuildRequires: lua-devel
BuildRequires: gcc

%description
This module adds UTF-8 support to Lua.

It uses data extracted from the
[Unicode Character Database](http://www.unicode.org/reports/tr44/),
and is tested on Lua 5.2.3, Lua 5.3.0 and LuaJIT.

parseucd.lua is a pure Lua script to generate unidata.h, to support conversion
of characters and to check the category of a characters.

It is compatible with Lua's own string module, and it passes all
string and pattern matching tests in the lua test suite.

It also add some useful routines for UTF-8 features, including:
- a convenient interface to escape Unicode sequences in string.
- string insert/remove, since UTF-8 substring extract may expensive.
- calculating the Unicode width, which can be useful when implementing a
  console emulator.
- an interface to translate Unicode offset and byte offset.


%prep
%forgesetup


%build
%{__cc} %{optflags} %{?__global_ldflags} -fPIC -c -o lutf8lib.o lutf8lib.c

%{__cc} %{?__global_ldflags} -shared -o lua-utf8.so lutf8lib.o


%install
install -dD %{buildroot}%{lua_libdir}
install -p -m 755 lua-utf8.so %{buildroot}%{lua_libdir}/


%check
LUA_CPATH="%{buildroot}%{lua_libdir}/?.so" \
lua -e 'local utf8 = require "lua-utf8"; assert(4 == utf8.len("test"));'

LUA_CPATH="%{buildroot}%{lua_libdir}/?.so" \
lua test.lua

%files
%license LICENSE
%doc README.md
%{lua_libdir}/lua-utf8.so
