#!/usr/bin/env bash
cd $API_FOLDER && flask db upgrade && flask run -h 0.0.0.0 -p 8000
