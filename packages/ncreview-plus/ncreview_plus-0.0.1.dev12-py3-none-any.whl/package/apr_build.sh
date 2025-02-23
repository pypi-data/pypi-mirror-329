#!/bin/sh

prefix=$APR_PREFIX
destdir=$APR_TOPDIR/package

export BUILD_PACKAGE_NAME="$APR_COMPONENT-$APR_PACKAGE"
export BUILD_PACKAGE_VERSION="$APR_VERSION"

cd $APR_TOPDIR

$APR_TOPDIR/build.sh --prefix=$prefix --destdir=$destdir --jenkins-build "$@"
