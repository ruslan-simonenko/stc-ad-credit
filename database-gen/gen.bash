#!/bin/bash
TARGET_FILE="../server/persistence/schema/__init__.py"

echo "# DO NOT EDIT - autogenerated file. See database-gen project for details" > $TARGET_FILE
flask-sqlacodegen --flask sqlite:///../database/dev.db >> ../server/persistence/schema/__init__.py