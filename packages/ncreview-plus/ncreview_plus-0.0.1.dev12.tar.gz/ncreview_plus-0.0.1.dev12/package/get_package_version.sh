#!/bin/sh

# Check for BUILD_PACKAGE_VERSION environment variable

version=$BUILD_PACKAGE_VERSION

if [ -z "$version" ]; then

    # Check for most recent package specific tag

    package=$BUILD_PACKAGE_NAME

    if [ -z "$package" ]; then
        # Use git project name for package name
        package=`git config --get remote.origin.url | \
                 sed 's/.*://;s/.git$//;s/^.*\///'`
    fi

    tag=`git describe --tags --long --dirty --match="${package}-v[0-9]*" 2>/dev/null`

    if [ -z "$tag" ]; then
        # Check for most recent tag
        tag=`git describe --tags --long --dirty 2>/dev/null`
    fi

    if [ -z "$tag" ]; then
        version="0.0-0-0-g0000000-dirty"
    else
        version=`echo $tag | \
                 sed -E "s/.*([0-9]+)\.([0-9]+)\.([0-9]+.*)$/\1.\2-\3/"`
    fi

    parts=(${version//-/ })

    # ${parts[0]} = major.minor
    # ${parts[1]} = build number
    # ${parts[2]} = number of commits since last tag
    # ${parts[3]} = git hash of last commit
    # ${parts[4]} = 'dirty' if local changes since last commit

    # major.minor-build
    version="${parts[0]}-${parts[1]}"

    # development version
    if [ ${parts[2]} != 0 ] || [ ${parts[4]} ]; then
        # add .dev<commit number>
        version+=".dev${parts[2]}"
    fi

    # uncommitted changes in code
    #if [ ${parts[4]} ]; then
        # add .dirty
     #   version+=".${parts[4]}"
    #fi

    # platform
    #system=`uname`

    #if [ $system == "Linux" ]; then
        # use 'el#'
    #    platform=`uname -r | sed 's/.*\(el[0-9]\).*/\1/'`
   # else
        # use system name
  #      platform=$system
 #   fi

#    version="$version.$platform"
fi

printf $version

exit 0
