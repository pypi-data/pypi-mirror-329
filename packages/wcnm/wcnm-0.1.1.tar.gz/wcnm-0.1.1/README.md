## Dependencies

dh-python, python3-setuptools, python3-stdeb, lolcat

Use

```bash
sudo apt install dh-python python3-setuptools python3-stdeb lolcat
```

## Build

Use

```bash
python3 setup.py --command-packages=stdeb.command bdist_deb
```

to build the debian package.

It will be located in the `deb_dist` directory.
