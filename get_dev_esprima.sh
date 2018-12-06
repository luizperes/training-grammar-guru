#!/bin/sh

echo "Creating directory: tokenize-js/node_modules.."
mkdir -p tokenize-js/node_modules

echo "Cloning Esprima into tokenize-js/node_modules.."
git clone https://github.com/jquery/esprima.git tokenize-js/node_modules/esprima-dev

cd tokenize-js/node_modules/esprima-dev

echo "Installing Esprima dependencies.."
npm install

echo "Compiling Esprima.."
npm run compile

cd ../../..

echo "Done!"
exit 0
