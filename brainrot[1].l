%{
#include "y.tab.h"
#include <stdio.h>
%}

%%

"vibe"              { return VIBE; }
"spill"             { return SPILL; }
"funk"              { return FUNK; }
"delulu"            { return DELULU; }
"nah"               { return NAH; }

[0-9]+              { yylval.num = atoi(yytext); return NUMBER; }
\"[^\"]*\"          { yylval.str = strdup(yytext); return STRING; }

[a-zA-Z_][a-zA-Z0-9_]* { yylval.id = strdup(yytext); return ID; }

">="                { return GE; }
">"                 { return GT; }
"<="                { return LE; }
"<"                 { return LT; }
"=="                { return EQ; }

"="                 { return '='; }
";"                 { return ';'; }
","                 { return ','; }
"{"                 { return '{'; }
"}"                 { return '}'; }
"("                 { return '('; }
")"                 { return ')'; }

[ \t\r\n]+          ;  // Skip whitespace
.                   { return yytext[0]; }

%%

int yywrap() { return 1; }
