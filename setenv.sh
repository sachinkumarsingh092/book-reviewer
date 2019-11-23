#! /bin/bash
# Script to set up necessary environment variables

export DATABASE_URL=postgres://rorzmqnunwbxqz:2c4a49ddb3468a935ec9a0d3475e40c51382b09d27a22623253cafd7593737ef@ec2-107-21-97-5.compute-1.amazonaws.com:5432/d23uqnpja601mh;
echo "Database set";
export FLASK_APP=application.py;
echo "App set";
export FLASK_DEBUG=1;
echo "Debug set";
# To use api key and uncomment the following lines.
# export API_KEY=YOUR_API_KEY
