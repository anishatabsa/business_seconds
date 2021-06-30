#!/bin/bash
export LOCAL_DEV_MODE=yes
export ROLE=test
set -x
pserve ./business_seconds/configuration/pyramid/development.ini --reload
