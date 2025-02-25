# dropboxdol

dropbox with a simple (dict-like or list-like) interface


To install:	```pip install dropboxdol```


# Setup

Note: To use `dropboxdol`, you'll need to have a dropbox access token. 
Additionally, that token should be allowed to do the operation that you are doing. 
For example, you only need the "sharing.write" permission to CREATE a (new) shared link. 

See more information in [Dropbox's Auth Guide](https://developers.dropbox.com/oauth-guide). 
Essentially, you need to make an "app" [here](https://www.dropbox.com/developers/apps) and get a token for it. 
No worries, it's quick and easy (just give the "app" a name) and give it a scope and permissions, 
then generate your token (and put it somewhere safe).

By default, `dropboxdol` looks for the access token in the `DROPBOX_ACCESS_TOKEN` environment variable. You can put your token there for easy interactions, but you can also specify another environment variable, or the access token itself, in the `access_token` argument of the functions and classes that need it. First, `dropboxdol` will look for the `access_token` string you gave it in the environment variables, and if it doesn't find it, it will assume you gave it the access token itself.


# Examples 

## Get dropbox links for local files/folders

(Your token needs the "sharing.write" permission to CREATE a (new) shared link.)

```python
>>> from dropboxdol import dropbox_link
>>> local_file = '/Users/thorwhalen/Dropbox/Apps/py2store/py2store_data/test.txt'
>>> dropbox_url = dropbox_link(local_file)
>>> print(dropbox_url)
```

    https://www.dropbox.com/scl/fi/3o8ooqje4f497npxdeiwg/test.txt?rlkey=x9jsd8u7k147x6fzc7stxozqe&dl=0

If you want to talk "relative" to the dropbox root dir, do this:

```python
>>> from functools import partial
>>> my_dropbox_link = partial(dropbox_link, dropbox_local_rootdir='/Users/thorwhalen/Dropbox')
```

If you want a "direct (download) link", do this:

```python
>>> dl1_link = my_dropbox_link('Apps/py2store/py2store_data/test.txt', dl=1)
```

    'https://www.dropbox.com/scl/fi/3o8ooqje4f497npxdeiwg/test.txt?rlkey=x9jsd8u7k147x6fzc7stxozqe&dl=1'


## Easy read/write access to your dropbox files 

A persister for dropbox.

```python
>>> import json
>>> import os
>>> from dropboxdol import DropboxPersister
>>> configs = json.load(open(os.path.expanduser('~/.py2store_configs.json')))
>>> s = DropboxPersister('/py2store_data/test/', **configs['dropbox']['__init__kwargs'])
>>> if '/py2store_data/test/_can_remove' in s:
...     del s['/py2store_data/test/_can_remove']
...
>>>
>>> n = len(s)
>>> if n == 1:
...     assert list(s) == ['/py2store_data/test/_can_remove']
...
>>> s['/py2store_data/test/_can_remove'] = b'this is a test'
>>> assert len(s) == n + 1
>>> assert s['/py2store_data/test/_can_remove'] == b'this is a test'
>>> '/py2store_data/test/_can_remove' in s
True
>>> del s['/py2store_data/test/_can_remove']
```


