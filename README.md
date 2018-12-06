# Grammar Guru
> Detects and fixes Javascript syntax errors.

### Installiing
Requires:
  - Python 3.6 `// other versions won't work (because of Tensorflow)`
  - Node.JS >= 4.0
  - Esprima
    - `npm i esprima`
    - [Use dev version of Esprima](#use-dev-version-of-esprima)
  - Tensorflow
    - `pip install --upgrade tensorflow`
  - pip
  - virtualenv (optional)
    - `pip install virtualenv`
    - Follow [these](#virtualenv) instructions.
  - Install dependencies
    - `pip install -r requirements.txt`
  - Download the [model data] and copy the `*.h5` and `*.json` files into the root directory (`/path/to/training-grammar-guru`).

[model data]: https://archive.org/details/lstm-javascript-tiny

#### virtualenv
If you are using `virtualenv`, follow the instructions above, otherwise skip it.
- `cd /path/to/training-grammar-guru`
- `virtualenv . -p /home/example_username/opt/python-3.6/bin/python3`
- `source ./bin/activate`

#### Use dev version of Esprima
Only the dev version of Esprima is able to [tokenize strings with a leading '/'](https://github.com/jquery/esprima/issues/1895).
```
$ ./patch_esprima.sh
```
Run this to get `tokenize-js` to use the latest dev version of Esprima.

### Usage
To suggest a fix for a file:

    $ ./detect.py suggest my-incorrect-file.js
    my-incorrect-file.js:1:1: try inserting a '{'
        if (name)
                  ^
                  {

To dump the model's token-by-token consensus about the file:

    $ ./detect.py dump my-incorrect-file.js


### License
Copyright 2016 Eddie Antonio Santos <easantos@ualberta.ca>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

<http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
