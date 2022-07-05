#!/bin/bash

psql -h kmaster -p 32272 -U postgres web1 < web1.sql
