#!/bin/bash

source krystal.rc

ssh -p 722 -i "${SSH_KEY}" "${HOST_USER}@${HOST_NAME}"
