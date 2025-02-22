# MP3Art
A python module terminal command to add or remove art to MP3 files.


```
usage: mp3art [-h] {add,remove} ...

Add or remove cover art to MP3 files.

options:
  -h, --help    show this help message and exit

Subcommands:
  Which operation to perform.

  {add,remove}  Add or remove cover art for an MP3 file.
    add         Add cover art to an MP3 file.
    remove      Remove cover art to an MP3 file.
```

<br>

## Add Cover Art
```
usage: mp3art add [-h] mp3 cover

positional arguments:
  mp3         Path to the MP3 file.
  cover       Path to the cover art file.

options:
  -h, --help  show this help message and exit
```

<br>

## Remove Cover Art
```
usage: mp3art remove [-h] mp3

positional arguments:
  mp3         Path to the MP3 file.

options:
  -h, --help  show this help message and exit
```

<br>

### Other Links
- PyPi: https://pypi.org/project/mp3art/