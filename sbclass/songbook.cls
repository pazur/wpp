\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{songbook}[2012/05/10 Songbook class]
\LoadClass[12pt]{book}
\usepackage[utf8]{inputenc}

\newif\ifprintfront
\printfronttrue
\DeclareOption{nofrontmatter}{\printfrontfalse}

\newif\ifprintinfo
\printinfotrue
\DeclareOption{noinfo}{\printinfofalse}
\ProcessOptions

\RequirePackage{verse}
\RequirePackage{keycommand}
\RequirePackage{multind}
\RequirePackage{multicol}
\RequirePackage{ifmtarg}
\RequirePackage{ifthen}
\RequirePackage{tikz}
\usetikzlibrary{matrix,decorations.pathreplacing,calc}
\RequirePackage{uniquecounter}
\RequirePackage{comment}
\RequirePackage{environ}
\RequirePackage[perpage,symbol*]{footmisc}

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

\newcommand{\ifzero}[2]{%
  \ifthenelse{\equal{#1}{0}}{#2}{}%
}
\newcommand{\ifnotzero}[2]{%
  \ifthenelse{\equal{#1}{0}}{}{#2}%
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
% INDICES
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\makeatletter
\newcommand{\firstwords}{\gdef\firstwordsmarked{1}\@ifstar%
                     \firstwordsStar%
                     \firstwordsNoStar%
}
\makeatother

\newcommand{\firstwordsNoStar}[1]{%
  \ignorespaces#1\index{fwidx}{#1}\ignorespacesafterend%
}
\newcommand{\firstwordsStar}[1]{%
  \ignorespaces\index{fwidx}{#1}\ignorespacesafterend%
}
\newcommand{\indexheader}[1]{\large\textbf{#1}}

\let\oldindexspace\indexspace

\renewcommand\indexspace{\oldindexspace\vspace{4pt}\pagebreak[3]}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
% SONGS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% These can (and, if needed, should be) redefined by the user if they
% want to adjust the songbook to their specific needs (e.g. langauge)
\newcommand\songlyrics{Słowa}
\newcommand\songmusic{Muzyka}
\newcommand\unknown{autor nieznany}
\newcommand\songdefaultline{L o r e m i p s u m, lorem lorem ipsum}
\newcommand{\defaultstanzabreak}[1][0.1in]{ \vspace{#1}}

% These should be treaten rather as package internals
\makeatletter
\newcommand{\song@title}[1] {
  {\noindent\huge\bfseries #1 \index{titidx}{#1}\par}
}
\newcommand{\song@alttitle}[1]{
  {\noindent \large #1 \index{titidx}{#1}\par }
}
\newenvironment{song@infobox}[1]
{\footnotesize\begin{flushright}\em #1}
  {\end{flushright}}


\newcommand*\cleartoleftpage{%
  \clearpage
  \ifodd\value{page}\hbox{}\newpage\fi
}


% These are main environments and commands to be used in songbooks
\newkeycommand{\song}[alt={},lyrics=\unknown,music=\unknown,lyricsyear={},musicyear={},bool beginonleft=false][1]
  {
    \ifzero{\commandkey{beginonleft}}{\newpage}
    \ifnotzero{\commandkey{beginonleft}}{\cleartoleftpage}
    \song@title{#1}
    \index{titidx}{#1}
    \ifckey{alt}{\song@alttitle{\commandkey{alt}}}
    \vspace{0.05in}    
    \begin{song@infobox}
      \songlyrics: \commandkey{lyrics}\ifckey{lyricsyear}{ (\commandkey{lyricsyear})}
      \par
      \songmusic: \commandkey{music}\ifckey{musicyear}{ (\commandkey{musicyear})}
    \end{song@infobox}
    
    \vspace{0.20in}
  }

\NewEnviron{info}{
  \ifprintinfo
  {\BODY}
  \fi
}
  
\newkeyenvironment{lyrics}[bool multicol=false,
                           bool vcenter=true,
                           longestline=\songdefaultline]
  {
    \ifnotzero{\commandkey{vcenter}}{\vfill}
    \let\par\defaultstanzabreak
    \settowidth{\versewidth}{\commandkey{longestline}} 
    \ifnotzero{\commandkey{multicol}}{
      \setlength{\columnsep}{2em}
      \begin{multicols}{2}
    }
    \begin{verse}[\versewidth]
      
    }
  {
    \end{verse}
    \ifnotzero{\commandkey{multicol}}{
      \end{multicols}
    }
    \ifnotzero{\commandkey{vcenter}}{\vfill}
    % Invalidate chorusfirstline
    \gdef\chorusfirstline{\PackageError{songbook}{chorusfirstwords macro should be used first}}
    %Invalidate firstwordsmark
    \gdef\firstwordsmarked{0}
  }
\makeatother

\newkeycommand{\breaklyrics}[bool vcenter=true]{%
    \ifnotzero{\commandkey{vcenter}}{\vspace*{\fill}}%
    \newpage%
    \ifnotzero{\commandkey{vcenter}}{\vspace*{\fill}}%
  }
% Mark environment
\definecolor{darkgray}{RGB}{90,90,90}
  
\newcommand\defaultmarktext{$\times2$}
\newcommand\markstyle{\color{darkgray}\scriptsize}
\newcommand\defaultmark{\color{darkgray}\scriptsize\defaultmarktext}
\newcommand\defaultmarkparen{\color{darkgray}\scriptsize(\defaultmarktext)}
\newlength{\markpos}
\UniqueCounterNew{bis}
\newcommand{\tikzmarktop}[1]{\tikz[overlay,remember picture] \node (#1) at ++(0,0.25\baselineskip) {};}
\newcommand{\tikzmarkbottom}[1]{\tikz[overlay,remember picture] \node (#1) at ++(0,-0.1\baselineskip){};}
\newcommand{\tikzmarkright}[1]{\tikz[overlay,remember picture] \node (#1) at ++(\versewidth + 1ex, 0) {};}
\newcommand{\tikzmarkrightnoalign}[2]{\settowidth{\markpos}{#2}\tikz[overlay,remember picture] \node (#1) at ++(\markpos + 1ex, 0) {};}

\newkeyenvironment{markverses}[marktext=\defaultmark,atwidthof={}]%
  {%
    \ifcommandkey{atwidthof}{%
      \tikzmarkrightnoalign{rright\UniqueCounterGet{bis}}{\commandkey{atwidthof}}%
      }{%
        \tikzmarkright{rright\UniqueCounterGet{bis}}%
      }%
    \tikzmarktop{bb\UniqueCounterGet{bis}}%
  }%
  {%
   \tikzmarkbottom{be\UniqueCounterGet{bis}}%
   \begin{tikzpicture}[overlay, remember picture]%
      \draw [decoration={brace,amplitude=0.3em},decorate,darkgray]%
      ($($(rright\UniqueCounterGet{bis})$)!(bb\UniqueCounterGet{bis}.north)!($($(rright\UniqueCounterGet{bis})$)$)$)%
      -- node[black, right=0.7em] {\emph{\commandkey{marktext}}}%
      ($($(rright\UniqueCounterGet{bis})$)!(be\UniqueCounterGet{bis})!($($(rright\UniqueCounterGet{bis})$)$)$);%
    \end{tikzpicture}%
    \UniqueCounterIncrement{bis}%
  }%

% Mark one line (no braces)
\newkeycommand{\markverse}[marktext=\defaultmarkparen, bool noalign=false][1]
{%
  \setlength{\markpos}{\versewidth}
  \ifnotzero{\commandkey{noalign}}{\settowidth\markpos{#1}}
  \tikz[overlay, remember picture] \node[anchor=base] at ++(\markpos + 2.1em,1pt){\emph{\commandkey{marktext}}};%
  {#1}%
  \UniqueCounterIncrement{bis}%
}

% Chorus environment
\newcommand{\chorusflag}{\flagverse{\small\textsc{Ref.}}}
\newcommand{\chorusflagskip}{1em}
\setlength{\vleftskip}{\chorusflagskip}
\newkeyenvironment*{chorus}[bool mark=false]%
{%
  \chorusflag%
  \ifnotzero{\commandkey{mark}}%
  {\begin{markverses}}%
}%
{%
  \ifnotzero{\commandkey{mark}}{\end{markverses}}%
}
\newcommand{\chorusfirstline}{\PackageError{songbook}{chorusfirstwords macro should be used first!}}
\newcommand{\chorusref}{\chorusflag\chorusfirstline\ldots}
\newcommand\chorusfirstwords[1]{%
  \ifzero{\firstwordsmarked}{\firstwords*{#1}}%
  #1\xdef\chorusfirstline{#1}%
}

%Indented environment
\newenvironment{indented}
  {%
    \addtolength{\leftmargini}{-14em}%
  }
  {%
    \addtolength{\leftmargini}{14em}%
  }
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% FRONTMATTER
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\let\oldfrontmatter\frontmatter
\renewcommand{\frontmatter}{%
\oldfrontmatter\pagestyle{empty}
}

\let\oldmainmatter\mainmatter
\renewcommand{\mainmatter}{
\oldmainmatter\pagestyle{headings}
}

\specialcomment{front}{\frontmatter}{\mainmatter}
\ifprintfront
  \includecomment{front}
\else
  \excludecomment{front}
\fi

\newenvironment{dedication}
{
   \pagestyle{empty}\cleardoublepage
   \thispagestyle{empty}
   \vspace*{0.8\textheight}
   \hfill\begin{minipage}[t]{0.4\textwidth}
   \raggedright\LARGE\it
}%
{
   \end{minipage}
   \cleardoublepage
}

\usepackage{anyfontsize}

\makeatletter
\newcommand\VERYHUGE{\@setfontsize\Huge{80}{100}}
\newcommand\HUGE{\@setfontsize\Huge{50}{70}}
\makeatother

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% MISC
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\setfnsymbol{wiley}

\renewcommand\smallskip{\vspace{2.4pt}}
\renewcommand\medskip{\vspace{4pt}}
\setlength{\vgap}{0.8em}

\newcommand{\intertitle}[1]{\textsc{#1}}