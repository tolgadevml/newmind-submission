#!/bin/sh
exec uvicorn main:app --host "${HOST}" --port "${PORT}"