\include "lilypond-book-preamble.ly"
\version "2.10.0"

\markup 
  \override #'(size . 1.25)
  \override #'(font-family . "Luxi Mono")
  \fret-diagram-terse #"%(chord_markup)s"