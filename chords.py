#!/usr/bin/env python
import os

from numpy import format_float_positional

CHORDS = {
    'Ab': ['4-(;6;6;5;4;4-);'],
    'Ab6': ['4-(;3;1;1;1;1-);'],
    'Ab7': ['x;x;1;1;1;2;'],
    'Ab9': ['x;x;1;3;1;2;'],
    'G#m': ['4-(;6;6;4;4;4-);'],
    'G#m6': ['x;x;3;4;4;4;'],
    'G#m7': ['x;x;1;1;o;2;'],
    'Abmaj7': ['x;x;1;1;1;3;'],
    'G#dim': ['x;x;o;1;o;1;'],
    'Abaug': ['x;x;2;1;1;o;'],
    'Absus': ['x;x;1;1;2;4;'],
    'A': ['o;o;2;2;2;o;', '5-(;7;7;6;5;5-);'],
    'A6': ['o;o;2-(;2;2;2-);'],
    'A7': ['x;o;2;o;2;o;', 'o;o;2;2;2;3;'],
    'Am': ['o;o;2;2;1;o;', '5-(;7;7;5;5;5-);'],
    'Am6': ['o;o;2;2;1;2;', '5-(;7;7;5;7;5-);'],
    'Am7': ['o;o;2;o;1;o;', '5-(;6;5;5;5;5-);'],
    'Am7/G': ['3;o;2;o;1;o;'],
    'Am7/F#': ['2;o;2;2;1;o;'],
    'A9': ['x;o;2;4;2;3;'],
    'Adim': ['x;x;1;2;1;2;'],
    'Aaug': ['x;o;3;2;2;1;'],
    'Asus': ['x;x;2;2;3;o;'],
    'Bb': ['x;1-(;3;3;3;1-);'],
    'Bbm': ['x;1-(;3;3;2;1-);'],
    'Bb6': ['1-(;1;3;3;3;3-);'],
    'Bb7': ['x;x;4-(;4;4;5-);'],
    'Bb9': ['1-(;1;3;1;1;1-);'],
    'Bbm6': ['x;x;3;3;2;3;'],
    'Bbm7': ['x;x;3;3;2;4;'],
    'Bbmaj7': ['x;1;3;2;3;x;'],
    'Bbdim': ['x;x;2;3;2;3;'],
    'Bbaug': ['x;x;o;3;3;2;'],
    'Bbsus': ['x;x;3;3;4;1;'],
    'B': ['x;1-(;3;3;3;1-);'],
    'Bm': ['x;1-(;3;3;2;1-);'],
    'B6': ['2-(;2;4;4;4;4-);'],
    'B7': ['x;2;1;2;o;2;', '1-(;1;2;1;2;1-);'],
    'B9': ['x;2;1;2-(;2;2-);'],
    'Bm6': ['x;x;6;6;5;6;'],
    'Bm7': ['x;2-(;4;2;3;2-);'],
    'Bdim': 'G#dim',
    'Baug': ['x;x;6;5;5;4;'],
    'Bsus': ['x;x;5;5;6;3;'],
    'C': ['x;3;2;o;1;o;', '3-(;3;5;5;5;3-);'],
    'C/B': ['x;2;2;x;1;o;'],
    'C/G': ['3;3;2;o;1;o;'],
    'C6': ['x;3;2;2;1;o;'],
    'C7': ['x;3;2;3;1;o;', '3-(;3;5;3;5;3-);'],
    'C9': ['x;3;2;3-(;3;3-);'],
    'Cm': ['3-(;3;5;5;4;3-);'],
    'Cm6': ['x;x;1;2;1;3;'],
    'Cm7': ['x;x;1;3;1;3;'],
    'Cmaj7': ['x;3;2;o;o;o;'],
    'Cdim': 'Adim',
    'Caug': ['x;x;2;1;1;o;'],
    'Csus': ['x;x;3;o;1;3;'],
    'Db': ['x;x;3;1;2;1;'],
    'C#m': ['x;x;2;1;2;o;'],
    'Db6': ['x;x;3;4;2;4;'],
    'Db9': ['x;4;3;4;4;4;'],
    'C#m6': ['x;x;2;3;2;4;'],
    'C#m7': ['x;x;2;4;2;4;'],
    'Dbmaj7': ['x;4;3;1-(;1;1-);'],
    'C#dim': 'Bbdim',
    'Dbaug': ['x;x;3;2;2;1;'],
    'Dbsus': ['x;x;3;3;4;1;'],
    'D': ['x;x;o;2;3;2;'],
    'D6': ['x;o;o;2;o;2;'],
    'D7': ['x;x;o;2;1;2;', '5-(;5;7;5;7;5-);'],
    'D7/F': ['2;x;o;2;1;2;'],
    'D9': ['2;o;o;2;1;o;'],
    'Dm': ['x;x;o;2;3;1;', '5-(;5;7;7;6;5-);'],
    'Dm/C#': ['x;x;o;2;2;1;'],
    'Dm6': ['x;x;o;2;o;1;'],
    'Dm7': ['x;x;o;2;1;1;', '5-(;5;7;5;6;5-);'],
    'Dmaj7': ['x;x;o;2;2;2;'],
    'Ddim': 'G#dim',
    'Daug': ['x;x;o;3;3;2;'],
    'Dsus': ['x;x;o;2;3;3;'],
    'Eb': ['x;o;6;4;5;4;'],
    'Ebm': ['x;x;4;3;4;2;'],
    'Eb6': ['x;x;1;3;1;3;'],
    'Eb7': ['x;x;1;3;2;3;'],
    'Eb9': ['1-(;1;1;3;2;1-);'],
    'Ebm6': ['x;x;1;3;1;2;'],
    'Ebm7': ['x;x;1;3;2;2;'],
    'Ebmaj7': ['x;x;1;3;3;3;'],
    'Ebdim': 'Adim',
    'Ebaug': ['x;x;1;o;o;3;'],
    'Ebsus': ['x;x;1;3;4;4;'],
    'E': ['o;3;3;2;o;o;'],
    'E6': ['o;2;2;1;2;o;'],
    'E7': ['o;2;o;1;o;o;', 'o;7;6;7;5;o;'],
    'E9': ['o;2;o;1;o;2;'],
    'Em': ['o;2;2;o;o;o;'],
    'Em6': ['o;2;2;o;2;o;'],
    'Em7': ['o;2;o;o;o;o;', 'o;2;2;o;3;o;'],
    'Emaj7': ['o;2;1;1;o;x;'],
    'Edim': 'Bbdim',
    'Esus': ['o;2;2;2;o;o;'],
    'F': ['1-(;3;3;2;1;1-);'],
    'Fm': ['1-(;3;3;1;1;1-);'],
    'F6': ['x;x;o;2;1;1;'],
    'F7': ['1-(;3;1;2;1;1-);', 'x;x;3;2;1;1;'],
    'F9': ['x;x;3;2;4;3;'],
    'Fm': ['1-(;3;3;1;1;1-);'],
    'Fm6': ['x;x;o;1;1;1;'],
    'Fm7': ['1-(;3;1;1;1;1-);'],
    'Fmaj7': ['o;x;3;2;1;o;'],
    'Fdim': 'Adim',
    'Faug': ['x;x;3;2;2;1;'],
    'Fsus': ['x;x;3;3;1;1;'],
    'F#': ['2-(;4;4;3;2;2-);'],
    'F#m': ['2-(;4;4;2;2;2-);'],
    'Gb6': ['x;4;4;3;4;x;'],
    'F#7': ['x;x;4;3;2;o;'],
    'F#9': ['x;x;5;4;6;5;'],
    'F#m6': ['x;x;1;2;2;2;'],
    'F#m7': ['x;x;2-(;2;2;2-);'],
    'Gbmaj7': ['x;x;4;3;2;1;'],
    'F#dim': 'Adim',
    'Gbaug': ['x;x;4;3;3;2;'],
    'Gbsus': ['x;x;4;4;2;2;'],
    'G': ['3;2;o;o;3;3;', '3-(;5;5;4;3;3-);'],
    'G/B': ['3;2;o;o;o;3;'],
    'Gm': ['3;5;5;3;3;3;'],
    'G6': ['3;2;o;o;3;o;'],
    'G7': ['3;2;o;o;o;1;', '3-(;5;3;4;3;3-);'],
    'G9': ['3;o;o;2;o;1;'],
    'Gm6': ['x;x;2;3;3;3;'],
    'Gm7': ['3-(;5;3;3;3;3-);'],
    'Gmaj7': ['3;2;o;o;o;2;'],
    'Gdim': 'Bbdim',
    'Gaug': ['x;x;1;o;o;3;'],
    'Gsus': ['x;x;o;o;1;3;'],
}
EQUIVALENCES = [('Ab', 'G#'), ('Bb', 'A#'), ('C#', 'Db'), ('F#', 'Gb'), ('Eb', 'D#')]
ACCIDENTALS_MAP = dict(EQUIVALENCES)
ACCIDENTALS_MAP.update(dict([(v,k) for k,v in EQUIVALENCES]))
CHORD_TEMPLATE_NAME = 'chords.ly'
LILYPOND_BIN = ''
LILYPOND_PARAMS = '--png -dbackend=eps'
LILYPOND_GARBAGE = ['-systems.count', '-1.eps', '-systems.tex', '-systems.texi', '.eps']

# png names
filenames = {}

import re
ACCIDENTAL_RE = re.compile('^([A-G]b|#)')

def create_lilypond(chord_markup, lilypond_path):
    # read in the lilypond template
    template = open(CHORD_TEMPLATE_NAME, 'r')
    # populate the template with the chord markup
    template_format = ''.join(template.readlines())
    template_string = template_format % {'chord_markup': chord_markup}
    lilypond_lines = template_string.split('\n')
    # write out the template somewhere
    output = open(lilypond_path, 'w')
    output.writelines(lilypond_lines)
    # return true on success
    return True
    
def create_png(lilypond_path, png_path):
    # call the png creator on the lilypond path
    os.system('%(lilypond)s %(params)s -o %(output)s %(input)s' % {
        'lilypond': LILYPOND_BIN + 'lilypond',
        'params': LILYPOND_PARAMS,
        'output': png_path,
        'input': lilypond_path,
    })
    # clean up excess files
    files = ' '.join([png_path + garbage for garbage in LILYPOND_GARBAGE])
    os.system('rm ' + files)
    # return true on success
    return True
    
def get_output_filename(chord_name, variation_number):
    chord = chord_name.replace('#', 's').replace('/', '_')
    variation = str(variation_number)
    return variation_number > 0 and (chord + '_' + variation) or chord
    
def export_chords(output_directory_path, chords):
    # go through all chords
    for chord, shapes in chords.items():
        # chords can be defined in terms of one another. 
        # if value is a string, look up that string
        if type(shapes) == str:
            shapes = chords[shapes]
        # for each chord, go through all chord shapes:
        for shape_markup in shapes:
            # create the appropriate filename for each chord shape variation
            index = shapes.index(shape_markup)
            # create lilypond
            lilypond_path = '/tmp/tmp.ly'
            create_lilypond(shape_markup, lilypond_path)
            # create png
            output_filename = get_output_filename(chord, index)
            filenames[chord] = output_filename
            create_png(lilypond_path, output_directory_path + output_filename)
            # check if this chord has accidentals in it, and if so create the other named version
            match = ACCIDENTAL_RE.match(chord)
            # possibly create another png
            if match:
                original_root = match.group()
                synonym_root = ACCIDENTALS_MAP[original_root]
                alt_chord = chord.replace(original_root, synonym_root)
                alt_filename = get_output_filename(alt_chord, index)
                create_png(lilypond_path, output_directory_path + alt_filename)
            
    # return true on success
    return True