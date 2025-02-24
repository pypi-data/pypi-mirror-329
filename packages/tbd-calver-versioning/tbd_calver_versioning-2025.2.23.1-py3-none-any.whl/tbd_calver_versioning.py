from ShellUtilities import Shell
import os
import logging
from pathlib import Path
import sys
import platform
import tempfile

# This contains python functions which invokes the bash script to determine the version number.

def determine_version_number(repo_path=None, adjust_for_pep_440=True, adjust_for_pypi=False):
    
    # Determine if we are using conda
    try:
        if os.environ["CONDA_DEFAULT_ENV"]:
            logging.info("Detected that a conda environment is being used.")
            using_conda = True
            conda_env_name = os.environ["CONDA_DEFAULT_ENV"]
            conda_env_path = os.environ["CONDA_PREFIX"]
    except:
        using_conda = False
    
    script_name = "determine_tbd_calver_version_number.sh"
    script_installed = False
    script_path = None
    
    # Determine if we are inside a pip build environment
    # If we are in a pip build environment, the file paths will change to an "overlay"
    # directory that pipe creates and manages
    logging.debug("Checking if inside pip build environment.")
    current_dir = os.path.abspath(os.path.dirname(__file__))
    tmp_dir = tempfile.gettempdir()
    build_env_dir_prefix = os.path.join(tmp_dir, "pip-build-env-")
    logging.debug(f"Checking current dir '{current_dir}' for build env prfix '{build_env_dir_prefix}'.")
    if current_dir.startswith(build_env_dir_prefix):
        logging.debug("We are in a pip build environment")
        # Manipulate the directoy and reconstruct the path to the overlay
        parts = current_dir.split(os.sep)
        parts = parts[1:]
        parts = [os.path.abspath(os.sep)] + parts
        build_env_dir = os.path.join(*parts[:4])
        script_path = os.path.join(build_env_dir, "bin", script_name)
        logging.debug(f"The script should be found at: '{script_path}'.")
        if not os.path.exists(script_path):
            raise Exception(f"The script '{script_path}' could not be found. Debug: the build environment dir was identified as '{build_env_dir}'.")
        script_installed = True
    else:
        logging.debug("We are not in a pip build environment")
    
    # Assume regular install and determine the platform
    if not script_installed:
        if platform.system() == "Linux" and not using_conda:
            # Check the environment variable named PATH to see if the script was installed
            logging.debug("Searching PATH for installed bash script.")
            logging.debug(os.linesep + os.environ["PATH"])
            script_installed = False
            for path in os.environ["PATH"].split(":"):
                script_path = os.path.join(path, script_name)
                if os.path.exists(script_path):
                    script_installed = True
                    logging.debug(f"Found script at '{script_path}'")
                    break
            logging.warn("Script not found in environment PATH.")       
        elif platform.system() == "Windows" and not using_conda:
            # On windows, the user is expected to use a bash-like environment
            logging.warn("Script not found in windows environment.")
            pass
        elif using_conda:
            script_path = os.path.join(conda_env_path, "bin", script_name)
            logging.debug(f"Checking conda environment for: {script_path}")
            if os.path.exists(script_path):
                script_installed = True
                logging.debug(f"Found script at '{script_path}'")
            else:
                logging.warn("Script not found in conda environment.")
 
    # If the script is not installed into the PATH, assume we are running from inside the git repo
    # Check if the script can be found locally
    if not script_installed:
        logging.warn("Assuming script is being run from the local git repo instead.")  
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if not repo_path:
            repo_path = os.getcwd()
        logging.debug(f"Repo path set to: {repo_path}")
        src_root_dir = os.path.dirname(current_dir)
        bash_dir = os.path.join(src_root_dir, "bash", "bin")
        script_path = os.path.join(bash_dir, script_name)
        if os.path.exists(script_path):
            script_installed = True
            logging.debug(f"Found script at '{script_path}'")

    if not script_installed:
        raise Exception("Unable to determine location of determine_tbd_calver_version_number.sh.")
    
    # Now that we know where the script is, we can run it
    # Before we can run it however, we need to identify the bash interpreter we will use
    interpreter = ""
    try:
        Shell.execute_shell_command(f"bash --version", cwd=repo_path).Stdout
        interpreter = "bash"
    except:
        pass
    if not interpreter:
        logging.warning("The bash executable was not found or not configured properly. Checking for sh executable.")
        try:
            Shell.execute_shell_command(f"sh --version", cwd=repo_path).Stdout
            interpreter = "sh"
        except:
            pass
    if not interpreter:
        logging.fatal("Unable to find a working bash interpreter")
    
    logging.debug("Running shell script to calculate version number.")
    version_number = Shell.execute_shell_command(f"{interpreter} {script_path}", cwd=repo_path).Stdout
    logging.debug(f"Raw version number determined to be '{version_number}'.")
    
    if not adjust_for_pep_440 and not adjust_for_pypi:
        return version_number
    
    # With PEP 440 version specifier is `<public identifier>[+<local label>]`
    # This means we need to adjust our version number to use a + rather than a .
    # for the fourth element in the version number
    #
        
    parts = version_number.split(".")
    year = parts[0]
    month = parts[1]
    day = parts[2]
    branch_type = parts[3]
    build_or_commit = parts[4]
    
    if adjust_for_pep_440:
        version_number = f"{year}.{month}.{day}+{branch_type}.{build_or_commit}"
        logging.debug(f"Adjusted version number for PEP-440. New version number: '{version_number}'.")
    
    # Note that Pypi does not allow local labels to be used. It is very strict
    # that it is a public package repository meant to serve public packages.
    # As such, the version numbers output by this library will not be compliant
    # with pypi (though they will work with other systems like artifactory).
    # 
    # One of the main issues is that the PEP 440 scheme really only allows numbers
    # which it represents with N:
    #
    #        [N!]N(.N)*[{a|b|rc}N][.postN][.devN]
    #
    # This means that only integration branches can have version numbers because 
    # they are synchronous in nature. Asynchronous branches cannot be assigned 
    # sequential numbers because they are non-sequention by nature.
    
    if adjust_for_pypi:
        if branch_type == "master":
            version_number = f"{year}.{month}.{day}.rc{build_or_commit}"
        elif branch_type == "release":
            version_number = f"{year}.{month}.{day}.{build_or_commit}"
        else:
            raise Exception(f"Unable to determine version number for a branch of type {branch_type} as it is not compliant with pypi's enforcement of PEP 440. See notes in source code for more details.")

        logging.debug(f"Adjusted version number for PyPI. New version number: '{version_number}'.")

    return version_number