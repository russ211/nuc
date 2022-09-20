#!/bin/bash
cd /data/workspace/muc
source .venv/bin/activate
waitress-serve --listen '*:9000' --call 'mysite:create_app'
