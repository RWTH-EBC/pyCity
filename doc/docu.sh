rm pycity_base.*.rst
sphinx-apidoc -F -H "pycity_base" -o "." "../pycity_base"
make clean
make html