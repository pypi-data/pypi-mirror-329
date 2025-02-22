# PyPNM - PPM and PGM image files reading and writing in pure Python

## Overview and Justification

PPM and PGM (particular cases of PNM format group) are simplest file formats for RGB and L images, correspondingly. This simplicity lead to some adverse consequences:

- lack of strict official specification. Instead, you may find words like "usual" in format description. Surely, there is someone who implement this part of image format in unprohibited, yet a totally unusual way.

- unwillingness of many software developers to provide any good support to for simple and open format. It took years for almighty Adobe Photoshop developers to include PNM module in distribution rather than count on third-party developers, and surely (see above) they used this chance to implement a separator scheme nobody else uses. What as to PNM support in Python, say, Pillow, it's often incomplete and requires counterintuitive measures when dealing with specific data types.

As a result, novice Python user (like me) may find it difficult to get reliable input/output modules for PPM and PGM image formats; therefore current PyPNM package was developed, combining input/output functions for 8-bits and 16-bits per channel binary and ascii PGM and PPM files, i.e. P2, P5, P3 and P6 PNM file types. Both greyscale and RGB with 16-bit per channel color depth (0...65535 range) are supported directly, without limitations and without any dances with tambourine like using separate methods etc.

Noteworthy that PyPNM module is pure Python module, which makes it pretty compact and OS-independent. No third-party imports, no Numpy version conflicts (some may find it surprising, but list reshaping in Python can be done with one line without Numpy) etc.

## Format compatibility

Current PyPNM module read and write capabilities are briefly summarized below.

| Image format | File format | Read | Write |
| ------ | ------ | ------ | ------ |
| 16 bits per channel RGB | P6 Binary PPM | YES | YES |
| 16 bits per channel RGB | P3 ASCII PPM | YES | YES |
| 8 bits per channel RGB | P6 Binary PPM | YES | YES |
| 8 bits per channel RGB | P3 ASCII PPM | YES | YES |
| 16 bits per channel L | P5 Binary PGM | YES | YES |
| 16 bits per channel L | P2 ASCII PGM | YES | YES |
| 8 bits per channel L | P5 Binary PGM | YES | YES |
| 8 bits per channel L | P2 ASCII PGM | YES | YES |
| 1 bit ink on/off | P4 Binary PBM | YES | NO |
| 1 bit ink on/off | P1 ASCII PBM | YES | NO |

## Target image representation

Main goal of module under discussion is not just bytes reading and writing but representing image as some logically organized structure for further image editing.

Is seems logical to represent an RGB image as nested 3D structure - (X, Y)-sized matrix of three-component RGB vectors. Since in Python list seem to be about the only variant for mutable structures like that, it is suitable to represent image as `list(list(list(int)))` structure. Therefore, it would be convenient to have module read/write image data to/from such a structure.

Note that for L images memory structure is still `list(list(list(int)))`, with innermost list having only one component, thus enabling further image editing with the same nested Y, X, Z loop regardless of color mode.

Note that for the same reason when reading 1 bit PBM files into image this module promotes data to 8 bit L, inverting values and multiplying by 255, so that source 1 (ink on) is changed to 0 (black), and source 0 (ink off) is changed to 255 (white).

## Installation

In case of installing using pip:

`pip install PyPNM`

then in your program import section:

`from pypnm import pnmlpnm`

then use functions as described in section *"pnmlpnm.py functions"* below.

In case you downloaded file **pnmlpnm.py** from Github or somewhere else as plain .py file and not a package, simply put this file into your program folder, then use `import pnmlpnm`.

## pnmlpnm.py functions

Module file **pnmlpnm.py** contains 100% pure Python implementation of everything one may need to read/write a variety of PGM and PPM files. No non-standard dependencies, no extra downloads, no dependency version conflict expected. I/O functions are written as functions/procedures, as simple as possible, and listed below:

- **pnm2list**  - reading binary or ascii RGB PPM or L PGM file and returning image data as nested list of int.
- **list2bin**  - getting image data as nested list of int and creating binary PPM (P6) or PGM (P5) data structure in memory. Suitable for generating data to display with Tkinter.
- **list2pnm** - getting image data as nested list of int and writing binary PPM (P6) or PGM (P5) file.
- **list2pnmascii** - alternative function to write ASCII PPM (P3) or PGM (P2) files.
- **create_image** - creating empty nested 3D list for image representation. Not used within this particular module but often needed by programs this module is supposed to be used with.

Detailed functions arguments description is provided below as well as in docstrings.

### pnm2list

`X, Y, Z, maxcolors, image3D = pnmlpnm.pnm2list(in_filename)`

Read data from PPM/PGM file to nested image data list, where:

- `X, Y, Z`   - image sizes (int);
- `maxcolors` - number of colors per channel for current image (int);
- `image3D`   - image pixel data as list(list(list(int)));
- `in_filename` - PPM/PGM file name (str).

### list2bin

`image_bytes = pnmlpnm.list2bin(image3D, maxcolors)`

Convert nested image data list to PGM P5 or PPM P6 (binary) data structure in memory, where:

- `image3D`   - `Y*X*Z` list (image) of lists (rows) of lists (pixels) of ints (channels);
- `maxcolors` - number of colors per channel for current image (int);
- `image_bytes` - PNM-structured binary data.

`image_bytes` object thus obtained is well compatible with Tkinter `PhotoImage(data=...)` method and therefore may be used to visualize any data represented as image-like 3D list. Note, however, that Tkinter used for Python 3.10 displays some hight-color images incorrectly; this was entirely a Tkinter problem, fixed with Python 3.11 release.

### list2pnm

`pnmlpnm.list2pnm(out_filename, image3D, maxcolors)`

Write PGM P5 or PPM P6 (binary) file from nested image data list, where:

- `image3D`   - `Y*X*Z` list (image) of lists (rows) of lists (pixels) of ints (channels);
- `maxcolors` - number of colors per channel for current image (int);
- `out_filename` - Name of PNM file to be written.

Note that unlike `lis2bit`, making big gulp to process whole image, `list2pnm` is developed for per row image writing to reduce memory requirements for large files.

### list2pnmascii

`pnmlpnm.list2pnmascii(out_filename, image3D, maxcolors)` where:

Write PGM P2 or PPM P3 (ASCII text) file from nested image data list, where:

- `image3D`   - `Y*X*Z` list (image) of lists (rows) of lists (pixels) of ints (channels);
- `maxcolors` - number of colors per channel for current image (int);
- `out_filename` - PNM file name.

Similar to `list2pnm` above but creates ascii pnm file instead of binary one. Note that `list2pnmascii` performs per sample image writing, providing minimal memory footprint for a price of potential extra file fragmentation (which may, or may not appear in reality, depending on system and hardware caching).

### create_image

`image3D = create_image(X, Y, Z)`

Create empty 3D nested list of `X*Y*Z` sizes. Not used within this particular module internally, but often needed by programs this module is supposed to be used with.

## References

1. [Netpbm file formats description](https://netpbm.sourceforge.net/doc/).

2. [PyPNM at Github](https://github.com/Dnyarri/PyPNM) containing example viewer application, illustrating using `list2bin` to produce data for Tkinter `PhotoImage(data=...)` to display, and opening/saving various portable map formats. Issues and discussions are open for possible bug reports.
