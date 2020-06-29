Python PEX Demo
===============
This is a demo repo to show how to build a single Python executable that contains a complete virtual environment. This process has helped me maintain an untainted "system" Python environment while being able to ship the latest modules. If you are a developer or sysadmin concerned those sorts of things, then this demo is for you.

What is PEX?
------------
From the overview of the PEX Project's Github:

> pex is a library for generating .pex (Python EXecutable) files which are executable Python environments in the spirit of virtualenvs. pex is an expansion upon the ideas outlined in [PEP 441](https://legacy.python.org/dev/peps/pep-0441/) and makes the deployment of Python applications as simple as cp. pex files may even include multiple platform-specific Python distributions, meaning that a single pex file can be portable across Linux and OS X.

#### Related links:
* [PEX Github](https://github.com/pantsbuild/pex)
* [PEP 441](https://legacy.python.org/dev/peps/pep-0441/)
* [WTF is PEX?](https://www.youtube.com/watch?v=NmpnGhRwsu0)

What is the goal of this project?
---------------------------------
1. Demonstrate how to buidle a generic PEX file for executing arbitrary scripts (i.e. shippable virtualenv).
2. Embed a basic Flask + Gunicorn API into a PEX file and launch it instead of a Python Shell.

0 Checkout this repo
=====================
Checkout this repo to a location of your preference and `cd` to it, and then we can get started. I also encourage initializing a new Python Virtualenv for this demo, but that is optional.

1 Creating a PEX executable
===========================
First thing you are going to need is the `pex` Python module. This can be easily installed via `pip` as shown below.

```sh
pip install pex
```

Now that you have PEX module, lets use is to build a basic Python executable. In this case, I'm going to import just the `numpy` module and save the resulting file to `numpy_example.pex` with the `-o` option.

```sh
pex numpy -o numpy_example.pex
```

If everything goes according to plan, we should now be able to launch the `numpy_example.pex` executable. Upon running the file directly, we should expect a ordinary Python interperter shell as show below.

```sh
./numpy_example.pex
Python 3.7.7 (default, Mar 10 2020, 15:43:33)
[Clang 11.0.0 (clang-1100.0.33.17)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> import numpy
>>> numpy.zeros((2,3))
array([[0., 0., 0.],
       [0., 0., 0.]])
>>>
```

Also, like the normal Python interperter, we can tell it to execute an external script. Below is the result from running the `numpy_test.py` from the examples folder.

```sh
./numpy_example.pex examples/numpy_test.py
[[ 0  1  2  3  4]
 [ 5  6  7  8  9]
 [10 11 12 13 14]]
```

Hopefully at this point some gears are turning. Could I have a whole mess of modules from a large, complicated project bundled into a single file? Yes! Yes you can, and the `-r` option is how. Below shows how to load this projects `requirements.txt` file in, including `xmltodict` which I exercise later on.

```sh
pex -r requirements.txt -o xmltodict_example.pex
```

Functionality is exactly the same as before, and the executable can either be executed directly or used to execute an aribtrary script.

```sh
./xmltodict_example.pex examples/xmltodict_test.py
OrderedDict([('key', OrderedDict([('subkey1', 'thing1'), ('subkey2', 'thing2')]))])
```

2 Embedding more complicated apps
=================================
In the same vein as Golang's compiled executables, we can use PEX to bundle together modules with a wrapper to deliever a complete single-executable-app. The meat and potatoes of this repo consist of a fairly simple Flask application (called `babble`) that is served via the WSGI server Gunicorn. 

Babble's structure is fairly important. All of the necessary machinery to load Gunicorn's config and start it are included in the `babble/__init__.py` file. Specifically the `launcher` function.

Below shows the process of integrating a locally developed module (the wrapper itself) as well as the use of the `-e` option for PEX that sets the entrypoint whenever executed.

```sh
# Verify that all requirements are available
pip install -r requirements.txt
# Install the `babble` module included in this repo so PEX can address it
python setup.py develop
# Build the pex and name it `babble.pex`
pex . -o babble.pex -e babble:launcher
```

This process should yeild PEX file just a before; however, upon execution, we are greeded with the output from Gunicorn.

```
$ ./babble.pex
[2020-06-24 20:56:48 -0400] [22226] [INFO] Starting gunicorn 20.0.4
[2020-06-24 20:56:48 -0400] [22226] [INFO] Listening at: http://127.0.0.1:8080 (22226)
[2020-06-24 20:56:48 -0400] [22226] [INFO] Using worker: sync
[2020-06-24 20:56:48 -0400] [22229] [INFO] Booting worker with pid: 22229
[2020-06-24 20:56:48 -0400] [22230] [INFO] Booting worker with pid: 22230
[2020-06-24 20:56:48 -0400] [22231] [INFO] Booting worker with pid: 22231
```

Lets take at the component that make this tick. 

###### babble/__init__.py
This is the entry point used in the last `pex` command. Some special things worth noting:

1. This launcher contains the argument parsing and instantiation of the Gunicorn server. The Flask `app` is imported in the same file so it is ready to go as soon as Gunicorn is available.
2. There is a tendancy to obscure operational parameters like config files or options when wraping up a module like this. Resist the urge. In the example below, the `-c` option was exposed to allow one to specify a Gunicorn config file. Otherwise, we set reasonable defaults.
3. The launcher function could have been put into another file (i.e. not `__init__.py`). Best practice would has us put this in a seperate file. The important part is that it is addressable with the `-e` option.
4. The Flask `app` object is imported from `babble/web_api.py` and the `StandaloneApplication` class is from `babble/web_server.py` just in case you want to review those as well.

```python
def launcher(live_reload=False):
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')

    arg_parse = argparse.ArgumentParser(description="A super basic Flask + Gunicorn app")
    arg_parse.add_argument("-c", "--config-file", dest="config_file",
                           help="Config File location", default=None)
    args = arg_parse.parse_args()

    if not args.config_file:
        options = {
            'bind': '%s:%s' % ('127.0.0.1', '8080'),
            'workers': 3,
            'reload': live_reload,
        }
    else:
        options = config_importer(args.config_file)
    StandaloneApplication(app, options).run()
```

Hopefully between this crash course, plus the supplied code, you'll know a little more about PEX. It might not be the best option for your app delievery needs, but having another arrow in the quiver never hurts.

FAQ
===
#### Q - What is the Flask App discussed in the examples even do?
A - It is a super simple XML to JSON and JSON to XML converter. If you have it running still, you can test it with the following `curl` commands.

```
# XML to JSON
curl -i -H "Content-Type: application/xml" -X POST \
    -d '<?xml version="1.0" ?><person><name>john</name><age>20</age></person>' \
    http://127.0.0.1:8080/xml_to_json

# JSON to XML
curl -i -H "Content-Type: application/json" -X POST \
    -d '{"userId":"1", "username": "fizz bizz"}' \
    http://127.0.0.1:8080/json_to_xml
```

#### Q - Do I have to use this repo with PEX?
A - Nope. If you just want to use this as a reference on how to embed a simple Flask app into a Gunicorn server, feel free. I did most of my development for the project in a normal Python environment before I wrote up the PEX portion.
