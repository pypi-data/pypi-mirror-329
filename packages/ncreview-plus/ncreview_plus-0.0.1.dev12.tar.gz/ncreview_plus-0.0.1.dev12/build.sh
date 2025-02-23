#!/bin/sh

# Print usage

script_name=$0

usage()
{
    cat <<EOM

DESCRIPTION

  Build script used to create a local install of ncreview.
  It can also be used to perform a staged installation by specifying a destdir,
  in which case the files are copied instead of linked. 

SYNOPSIS

  $script_name [-h|--help] [--prefix=path] [--destdir=path] [--env-update] [--py|--web] [--jenkins-build] [--env-update] [--env-clean] [--uninstall]

OPTIONS

    --prefix=path   absolute path to installation directory
                    default: \$DSUTIL_HOME

    --destdir=path  absolute path prepended to prefix
                    used to perform a staged installation

    --py            build Python package only

    --web           build web app only

    --jenkins-build build is in Jenkins

    --uv            manage dependencies with uv instead of Conda

    --env-update    update conda dependencies listed in the
                    environment.yml file.

    --env-clean     clean/remove conda environment before building it again

    --uninstall     uninstall locally installed package

    -h, --help      display this help message

EOM
}

# Parse command line

for i in "$@"
do
    case $i in
        --prefix=*)   prefix="${i#*=}"
                      ;;
        --destdir=*)  destdir="${i#*=}"
                      ;;
        --py)         pyonly=1
                      ;;
        --web)        webonly=1
                      ;;
        --jenkins-build) jenkins_build=1
                      ;;
        --uv)         USE_UV=1
                      ;;
        --env-update) env_update=1
                      ;;
        --env-clean)  env_clean=1
                      ;;
        --uninstall)  uninstall=1
                      ;;
        -h | --help)  usage
                      exit 0
                      ;;
        *)            usage
                      exit 1
                      ;;
    esac
done

# Get prefix from environment variables if necessary

if [ ! $prefix ]; then
    if [ $DSUTIL_HOME ]; then
        prefix=$DSUTIL_HOME
    else
        echo "Please pass 'prefix' argument or define DSUTIL_HOME environment variable, exiting"
        usage
        exit 1
    fi
fi

if [ $destdir ]; then
    echo "destdir: $destdir"
fi
echo "prefix:  $prefix"

# Function to echo and run commands

run() {
    echo "> $1"
    $1 || exit 1
}

src_dir=ncreview_plus/src

 

if [ -d web ] && [ ! $pyonly ]; then

    echo "------------------------------------------------------------------"
    confdir="$destdir$prefix/conf"
    webdir="$destdir$prefix/www"
    echo "webdir:  $webdir"

    cd $src_dir/web
    if [ $uninstall ]; then
        run "rm -rf $confdir"
        run "rm -rf $webdir"

        echo "uninstalled: $confdir"
        echo "uninstalled: $webdir"
    else
        confdir="$confdir/httpd"
        webdir="$webdir/Root/dsutil/ncreview"
        # ARM
        npm=/apps/base/bin/npm
        if [ ! -e "$npm" ]; then
            # code.a2e
            npm=/usr/lib/node_modules_20/npm/bin/npm
        fi
        if [ ! -e "$npm" ]; then
	    npm=$(which npm)
        fi

        PUBLIC_URL="/ncreview"
        export PUBLIC_URL
        export REACT_APP_URL_PREFIX=$PUBLIC_URL

        run "$npm ci"
        run "$npm run build"

        run "mkdir -p $confdir"
        run "mkdir -p $webdir"

        run "cp -R build/* $webdir"
        run "cp ncreview.conf $confdir"

        echo "installed: $confdir"
        echo "installed: $webdir"
    fi
    cd ..

    if [ -d web-legacy ]; then

        echo "------------------------------------------------------------------"
        webdir="$webdir/legacy"
        echo "webdir:  $webdir"

        cd web-legacy
        if [ $uninstall ]; then
            run "rm -rf $webdir"

            echo "uninstalled: $webdir"
        else
            run "mkdir -p $webdir"

            run "cp -R * $webdir"

            echo "installed: $webdir"
        fi
        cd ..
    fi
fi

if [ $webonly ]; then
    exit 0
fi

echo "------------------------------------------------------------------"

if [ ! $uninstall ] ; then
    if [ $USE_UV ]; then
        run "uv sync"
    else
        # Activate Conda Environment
        conda_base=$(conda info --base)
        conda_source=$conda_base/etc/profile.d/conda.sh
        if [ ! -e "$conda_source" ]; then
            echo "Cannot find Conda source file in ${conda_source}; exiting"
        exit 1
        fi

        run "source $conda_source"

        # VAP-specific Environment
        if [ -e "environment.yml" ]; then

            # echo "environment.yml file found"
            conda_env=$(head -n 1 environment.yml | cut -f2 -d ' ')

            creation_conda_env=$conda_env
            if [ $PRODUCTION = "false" ] || [ $jenkins_build ]; then
                creation_conda_env="dev-$conda_env"
            fi

            echo "Conda env is: $creation_conda_env"

            # Check if environment already exists
            env_exists=$(conda env list | grep $creation_conda_env)

            # Check that environment is not already activated
            if [[ $PATH != *$creation_conda_env* ]]; then

                # Remove the old environment, if appropriate
                if [ $env_clean ]; then
                    echo "Cleaning conda environment $creation_conda_env"
                    run "conda env remove -y -n $creation_conda_env"
                    env_exists=""
                fi

                # Create the environment and activate
                if [ -z "$env_exists" ]; then
                    echo "Conda env '$creation_conda_env' doesn't exist, creating."
                    run "conda env create -n $creation_conda_env -f environment.yml --solver=libmamba"
                fi

                run "conda activate $creation_conda_env"

            fi
        # Require environment file
        else
            echo "Could not find environment.yml file, required for running"
            exit 1
        fi

        if [ -z $CONDA_PREFIX ]; then
            echo "Conda activation did not work, exiting"
            exit 1
        fi

        if [ $env_update ]; then
            run "conda env update -n $creation_conda_env -f environment.yml --solver=libmamba"
        fi
    fi
fi

# Set Python Commands
if [ $USE_UV ]; then
    pyprefix=$CONDA_PREFIX
    python="$pyprefix/bin/python" # currently unused
    pip="uv pip"
else
    pyprefix=$CONDA_PREFIX
    python="$pyprefix/bin/python"
    pip="$pyprefix/bin/pip"
fi

# Takes 3 arguments, incl name of executable
create_wrapper_script () {
    execname=$1
    wrapper_file=$2
    conda_env=$3

    # Write wrapper script
    rm -f $wrapper_file
    echo "#!/bin/bash" >> $wrapper_file
    echo "# Activate environment and run VAP" >> $wrapper_file
    echo "source $conda_source"  >> $wrapper_file
    echo "conda activate $conda_env"  >> $wrapper_file
    echo "$execname \$@" >> $wrapper_file
    run "chmod +x $wrapper_file"
}

# Takes 2 arguments, incl name of executable
create_wrapper_script_uv () {
    execname=$1
    wrapper_file=$2

    # Write wrapper script
    rm -f $wrapper_file
    echo "#!/bin/bash" >> $wrapper_file
    echo "uv run $execname \$@" >> $wrapper_file
    run "chmod +x $wrapper_file"
}

# Install/Uninstall Python Package

execnames=("ncreview" "ncrplot" "ncrserver")
package=ncrpy
bindir="$destdir$prefix/bin"

if [ ! -d $bindir ]; then
    run "mkdir -p $bindir"
fi

set +e
for execname in ${execnames[@]}
do
    run "rm -f $bindir/$execname"
    if [ ! $? -eq 0 ]; then
        echo "(Hint: for local builds, define \"prefix\" or reset DSUTIL_HOME)"
        exit 1
    fi
done
set -e


if [ $uninstall ]; then
    run "$pip uninstall -y $package"
else
    run "$pip install -e ."

    wrapper_conda_env=$conda_env
    if [ $PRODUCTION = "false" ] && [ ! $jenkins_build ]; then
        wrapper_conda_env="dev-$conda_env"
    fi

    for execname in ${execnames[@]}
    do
        if [ $USE_UV ] ; then
            create_wrapper_script_uv $execname "${execname}_wrapper.sh"
        else
            create_wrapper_script $execname "${execname}_wrapper.sh" $wrapper_conda_env
        fi
        run "mv "${execname}_wrapper.sh" $bindir/$execname"
    done
fi

exit 0
