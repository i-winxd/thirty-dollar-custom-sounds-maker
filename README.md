# 30 dollar custom extension saver

A program that compiles custom sounds for 
the [thirty dollar website.](https://thirtydollar.website/)
The file exported by this program, named by default `EXPORTED_THIRTYDOLLAR.json` can be directly loaded into 
the thirty dollar website using the extension below. The file contains all the image and sound data, so you can easily share it with others.

This is to be paired with my fork of this extension,
which is linked here: https://github.com/i-winxd/thirty-dollar-custom-fork

**WARNING**: Be careful when using files shared by other people, as you do not want to be loading anything that is malicious!!! I am not responsible for anything that happens due to you running other people's exports. If you really want to share this safely, you should just share the audio and image files you would put here instead of the JSON that was output by this program. The security vulnerabilities can be quite severe.

## Implementation and Usage

Prepare a new sound effect by:

- Adding an audio file to this directory/folder or any subdirectory here. For example, `sample.mp3` or `sample.wav`
- Adding an image file to this directory with the same name EXCEPT for the extension: `sample.png` or `sample.jpg`

Check `constants.py` for supported file extensions. You'll note that `.webp` files are not supported, so use the included script to convert them to png files. Note that renaming webp files to png files will not work. I would strongly recommend sticking to `.png, .jpeg` files and `.mp3, .wav` files as I have no idea if this works for any other formats. Let me know if they do.

For example, I may have these files in my current folder:

```
- parent
    ├─ constants.py
    ├─ main.py
    ├─ webp_to_png.py
    ├─ sound1.mp3
    ├─ sound1.png
    ├─ sound2.mp3
    ├─ sound2.mp3
    ├─ sound3.wav
    └─ sound3.jpg
```

It is also acceptable to have a file structure that looks like this:

```
- parent
    ├─ constants.py
    ├─ main.py
    ├─ webp_to_png.py
    ├─ sounds
    │   ├─ sound1.mp3
    │   ├─ sound2.mp3
    │   └─ sound3.wav
    └─ images
        ├─ sound1.png
        ├─ sound2.png
        └─ sound3.jpg

```

You may organize your image files and audio files however you like.

There is one caveat: **Do NOT put spaces or any of these symbols: `!@#$%^&*()"'` in your file names otherwise they will be
skipped.** (This does not apply to the parent directories of the files.)

The raw instrument name for each sound is the same as the name of the file (not including the extension). It may be all lowercase. This is useful information if you're using a MIDI converter.

## Running the program

You must have Python 3.9 or later installed. I strongly recommend that you use the latest version of Python.

If you want to run `webp_to_png.py`, you must have `Pillow` installed: [how to install it](https://pillow.readthedocs.io/en/stable/installation.html)

**HERE:** Run `main.py` to do the conversion process, which should output `EXPORTED_THIRTYDOLLAR.json`. If that file already exists, then it will overwrite it.

Run `webp_to_png.py` to convert all `.webp` files in this folder to `.png` files. Be aware that if you have `a.webp` and `a.png` in the same folder and run this program, what was `a.png` will be overwritten by `a.webp` converted to PNG.

To run a Python script, open up terminal with the current directory set to the folder the `.py` file is in (do this easily by typing "cmd" in the file search box with this folder open) and run `python main.py`, or run the `.bat` file here.
