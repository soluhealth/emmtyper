"""
Automate deployment to PyPi
"""

import invoke


@invoke.task
def deploy_patch(ctx):
    """
    Automate deployment
    rm -rf build/* dist/*
    bumpversion patch --verbose
    python3 setup.py sdist bdist_wheel
    twine upload dist/*
    git push --tags
    """
    ctx.run("rm -rf build/* dist/*")
    ctx.run("bumpversion patch --verbose")
    ctx.run("python3 setup.py sdist bdist_wheel")
    ctx.run("twine check dist/*")
    ctx.run("twine upload dist/*")
    ctx.run("git push --tags")


@invoke.task
def check_for_unstaged_changes(ctx):
    """
    If unstaged changes raise an error
    """
    try:
        ctx.run("git diff-index --quiet HEAD")
    except invoke.exceptions.UnexpectedExit as error:
        print(("ERROR: There are unstaged changes."))
        raise error
    except Exception as error:
        raise error


@invoke.task(pre=[check_for_unstaged_changes])
def first_deploy(ctx):
    """
    First deployment
    """
    ctx.run("python3 setup.py sdist bdist_wheel")
    ctx.run("twine check dist/*")
    ctx.run("twine upload dist/*")
    ctx.run("git tag 'v1.0.0'")
    ctx.run("git push --tags")
