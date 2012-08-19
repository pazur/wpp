\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{songbook}[2012/05/10 Songbook class]
\LoadClass{book}

\usepackage[utf8]{inputenc}

\RequirePackage{verse}
\RequirePackage{keycommand}
\RequirePackage{multind}
\RequirePackage{multicol}
\RequirePackage{ifmtarg}
\RequirePackage{ifthen}
\RequirePackage{tikz}
\usetikzlibrary{matrix,decorations.pathreplacing,calc}

\usepackage{needspace}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
% VARIOUS UTILS, METACOMMANDS, ETC.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Workaround to some bug in keycommand package (ifcommandkey not
% working properly)
\begingroup
\makeatletter
\catcode`\/=8 %
\@firstofone
{
  \endgroup
  \renewcommand{\ifcommandkey}[1]{%
    \csname @\expandafter \expandafter \expandafter 
    \expandafter \expandafter \expandafter  \expandafter
    \kcmd@nbk \commandkey {#1}//{first}{second}//oftwo\endcsname
  }
} 

\makeatletter
\newcommand{\isempty}[3]{%
  \@ifmtarg{#1}{#2}{#3}}
\newcommand{\isnotempty}[2]{%
  \@ifnotmtarg{#1}{#2}}
\makeatother
\newcommand{\ifckey}[2]{\ifcommandkey{#1}{#2}{}}

\newcommand{\ifnotzero}[2]{
  \ifthenelse{\equal{#1}{0}}{}{#2}
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
% INDICES
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newcommand{\firstwords}[1]{
  \ignorespaces#1\index{fwidx}{#1}\ignorespacesafterend
}
\newcommand{\indexheader}[1]{\large\textbf{#1}}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
% SONGS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% These can (and, if needed, should be) redefined by the user if they
% want to adjust the songbook to their specific needs (e.g. langauge)
\newcommand\songlyrics{Słowa}
\newcommand\songmusic{Muzyka}
\newcommand\unknown{Nieznany}
\newcommand\songdefaultline{L o r e m i p s u m, lorem lorem ipsum}
\newcommand{\stanzabreak}[1][0.1in]{ \vspace{#1}}

% These should be treaten rather as package internals
\makeatletter
\newcommand{\song@title}[1] {
  {\noindent\Huge\bfseries #1 \index{titidx}{#1}\par}
}
\newcommand{\song@alttitle}[1]{
  {\noindent \Large #1 \par}
}
\newenvironment{song@infobox}[1]
{\small\begin{flushright}\em #1}
  {\end{flushright}}

% These are main environments and commands to be used in songbooks
\newkeycommand{\song}[alt={},lyrics=\unknown,music=\unknown,lyricsyear={},musicyear={}][1]
  {
    \newpage
    \song@title{#1}
    \index{titidx}{#1}
    \ifckey{alt}{\song@alttitle{\commandkey{alt}}}
    \vspace{0.05in}    
    \begin{song@infobox}
      \songlyrics: \commandkey{lyrics}\ifckey{lyricsyear}{ (\commandkey{lyricsyear})}
      \par
      \songmusic: \commandkey{music}\ifckey{musicyear}{ (\commandkey{musicyear})}
    \end{song@infobox}
    
    \vspace{0.2in}
  }

\newkeyenvironment{lyrics}[bool multicol=false,longestline=\songdefaultline]
  {
    \let\par\stanzabreak
    \vspace{0.4in}
    \settowidth{\versewidth}{\commandkey{longestline}} 
    \ifnotzero{\commandkey{multicol}}{
      \setlength{\columnsep}{0pt}
      \begin{multicols}{2}
    }
    \begin{verse}[\versewidth]
      
    }
  {
    \end{verse}
    \ifnotzero{\commandkey{multicol}}{
      \end{multicols}
    }
}

\newenvironment{info}
  {\begin{small}}
  {\end{small}}

\makeatother

\newcommand{\tikzmark}[1]{\tikz[overlay,remember picture] \node (#1) {};}
% Repeat environment
\newenvironment{bis}
  {%
    \tikzmark{rright}%
    \tikzmark{1b}}%
  {%
   \tikzmark{1e}
   \begin{tikzpicture}[overlay, remember picture]
      \draw [decoration={brace,amplitude=0.5em},decorate,gray]
      ($($(rright)+(\versewidth,0)$)!(1b.north)!($($(rright)+(\versewidth,0)$)-(0,1)$)$)
      -- node[black, right=0.7em] {x2}
      ($($(rright)+(\versewidth,0)$)!(1e.south)!($($(rright)+(\versewidth,0)$)-(0,1)$)$);
    \end{tikzpicture}
  }%
