#!/bin/sh

pandoc --from=markdown --to=rst --output=README.rst README.md
pandoc --from=markdown --to=rst --output=CHANGES.rst CHANGES.md
