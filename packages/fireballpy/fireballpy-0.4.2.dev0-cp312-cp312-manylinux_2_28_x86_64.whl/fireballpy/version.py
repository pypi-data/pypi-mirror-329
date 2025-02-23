
"""
Module to expose more detailed version info for the installed `fireballpy`
"""
version = "0.4.2.dev0"
full_version = version
short_version = version.split('.dev')[0]
git_revision = ""
release = 'dev' not in version and '+' not in version

if not release:
    version = full_version
