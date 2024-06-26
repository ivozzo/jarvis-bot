import os
from PIL import Image


def find_all_images(input_path, output_path, format, verbose=False, overwrite=False):
    images = []
    try:
        print("-"*40)
        print("The following images has been found:")
        for (root, dirs, file) in os.walk(input_path):
            for f in file:
                if format in f:
                    print("- %s " % f)

                    # Check if thumbnail has already been created, if not or overwriting create it again
                    if check_if_thumbnail_already_exists(output_path, filename=f, verbose=verbose) and not overwrite:
                        if verbose:
                            print("     Thumbnail already existing, skipping")
                        thumb = output_path + f
                    else:
                        print("     Generating thumbnail")
                        thumb = generate_thumbnails(input_path, output_path, f)

                    # Check if text has already been generated, if not or overwriting enqueue the item for generation
                    if not check_alt_file_existence(input_path, filename=f, format=format, verbose=verbose) or overwrite:
                        if verbose:
                            print("     Enqueueing image for Alt Text generation")
                        images.append(dict(thumbnail=thumb, filename=f))
                    else:
                        if verbose:
                            print("     Alt text has already been generated, skipping")
    except FileNotFoundError:
        print("ERROR: you haven't specified a valid path!")

    return images


def check_if_thumbnail_already_exists(output_path, filename, verbose=False):
    for (root, dirs, file) in os.walk(output_path):
        for f in file:
            if filename in f:
                return True
    return False


def check_alt_file_existence(output_path, filename, format, verbose=False):
    for (root, dirs, file) in os.walk(output_path):
        for f in file:
            if filename.replace(format, '.txt') in f:
                return True
    return False


def generate_thumbnails(input_path, output_path, filename):
    input_filepath = input_path + filename

    image = Image.open(input_filepath)
    image.thumbnail((720,720))
    output_filepath = output_path + filename
    image.save(output_filepath)

    return output_filepath


def generate_alt_text_file(output_path, filename, format, body, verbose=False):
    output_filepath = output_path + filename.replace(format, '.txt')
    print("Saving generated Alt Text for %s in %s " % (filename, output_filepath))
    with open(output_filepath, 'w') as f:
        f.write(body)
