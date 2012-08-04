from songbook.export import songtree

%%

parser Lyrics:
    token EMPTY:     '\n'
    token VERSE:     'verse text (\\$chords)?\n'
    token PIPE:      'verse text | (\\$chords)?\n'
    token PIPETEXT:  'verse text | txt (\\$chords)?\n'
    token CHORUS_OP: '<chorus>'
    token CHORUS_CL: '</chorus>'
    token EOF: '$'

    rule entry: lyrics EOF                  {{ return songtree.Lyrics(lyrics) }}
    rule lyrics:  stanza lyrics_sep         {{ return [stanza] + lyrics_sep }}
                | chorus maybe_empty lyrics {{ return [chorus] + lyrics }}
                |                           {{ return [] }}

    rule lyrics_sep:  EMPTY lyrics              {{ return lyrics }}
                    | chorus maybe_empty lyrics {{ return [chorus] + lyrics }}
                    |                           {{ return [] }}

    rule maybe_empty: EMPTY
                    |

    rule chorus: CHORUS_OP maybe_empty stanza_lst CHORUS_CL {{ return songtree.Chorus(stanza_lst) }}

    rule stanza_lst:  stanza stanza_lst_sep {{ return [stanza] + stanza_lst_sep }}
                    |                       {{ return [] }}

    rule stanza_lst_sep:  EMPTY stanza_lst  {{ return stanza_lst }}
                        |                   {{ return [] }}

    rule stanza: group group_lst            {{ return songtree.Stanza([group] + group_lst)}}

    rule group_lst:   group group_lst       {{ return [group] + group_lst}}
                    |                       {{ return [] }}

    rule group:   VERSE                     {{ return VERSE }}
                | pipe_lst PIPETEXT         {{ return songtree.Group(pipe_lst + [PIPETEXT]) }}

    rule pipe_lst:    PIPE pipe_lst         {{ return [PIPE] + pipe_lst }}
                    |                       {{ return [] }}
