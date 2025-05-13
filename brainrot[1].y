%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void yyerror(const char *s);
int yylex();

typedef struct {
    char* id;
    int value;
} Var;

Var symbol_table[100];
int var_count = 0;

int get_value(char* id) {
    for (int i = 0; i < var_count; ++i) {
        if (strcmp(symbol_table[i].id, id) == 0)
            return symbol_table[i].value;
    }
    printf("Error: undeclared variable %s\n", id);
    exit(1);
}

void set_value(char* id, int value) {
    for (int i = 0; i < var_count; ++i) {
        if (strcmp(symbol_table[i].id, id) == 0) {
            symbol_table[i].value = value;
            return;
        }
    }
    symbol_table[var_count].id = strdup(id);
    symbol_table[var_count].value = value;
    var_count++;
}
%}

%union {
    int num;
    char* str;
    char* id;
}

%token <num> NUMBER
%token <str> STRING
%token <id> ID
%token VIBE SPILL DELULU NAH FUNK
%token GE GT LE LT EQ

%type <num> expr

%%

program:
    statements
    ;

statements:
    statements statement
    |
    ;

statement:
      VIBE ID '=' expr ';'     { set_value($2, $4); }
    | ID '=' expr ';'          { set_value($1, $3); }
    | SPILL STRING ';'         { printf("%s\n", $2); }
    | SPILL expr ';'           { printf("%d\n", $2); }
    | DELULU expr block NAH block { if ($2) { /* then block executed */ } else { /* else block */ } }

    | FUNK ID '(' ID ',' ID ')' block
                              { /* No actual function logic here, just parsing */ }
    | ID '(' expr ',' expr ')' ';'
                              { /* Call dummy function */ }
    ;

block:
    '{' statements '}'
    ;

expr:
      expr GE expr   { $$ = $1 >= $3; }
    | expr GT expr   { $$ = $1 > $3; }
    | expr LE expr   { $$ = $1 <= $3; }
    | expr LT expr   { $$ = $1 < $3; }
    | expr EQ expr   { $$ = $1 == $3; }
    | expr '+' expr  { $$ = $1 + $3; }
    | expr '-' expr  { $$ = $1 - $3; }
    | expr '*' expr  { $$ = $1 * $3; }
    | expr '/' expr  { $$ = $1 / $3; }
    | NUMBER         { $$ = $1; }
    | ID             { $$ = get_value($1); }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}
