/*!-----------------------------------------------------------------------------
 * Copyright (c) Microsoft Corporation. All rights reserved.
 * Version: 0.49.0(383fdf3fc0e1e1a024068b8d0fd4f3dcbae74d04)
 * Released under the MIT license
 * https://github.com/microsoft/monaco-editor/blob/main/LICENSE.txt
 *-----------------------------------------------------------------------------*/


// src/basic-languages/tcl/tcl.ts
var conf = {
  brackets: [
    ["{", "}"],
    ["[", "]"],
    ["(", ")"]
  ],
  autoClosingPairs: [
    { open: "{", close: "}" },
    { open: "[", close: "]" },
    { open: "(", close: ")" },
    { open: '"', close: '"' },
    { open: "'", close: "'" }
  ],
  surroundingPairs: [
    { open: "{", close: "}" },
    { open: "[", close: "]" },
    { open: "(", close: ")" },
    { open: '"', close: '"' },
    { open: "'", close: "'" }
  ]
};
var language = {
  tokenPostfix: ".tcl",
  specialFunctions: [
    "set",
    "unset",
    "rename",
    "variable",
    "proc",
    "coroutine",
    "foreach",
    "incr",
    "append",
    "lappend",
    "linsert",
    "lreplace"
  ],
  mainFunctions: [
    "if",
    "then",
    "elseif",
    "else",
    "case",
    "switch",
    "while",
    "for",
    "break",
    "continue",
    "return",
    "package",
    "namespace",
    "catch",
    "exit",
    "eval",
    "expr",
    "uplevel",
    "upvar"
  ],
  builtinFunctions: [
    "file",
    "info",
    "concat",
    "join",
    "lindex",
    "list",
    "llength",
    "lrange",
    "lsearch",
    "lsort",
    "split",
    "array",
    "parray",
    "binary",
    "format",
    "regexp",
    "regsub",
    "scan",
    "string",
    "subst",
    "dict",
    "cd",
    "clock",
    "exec",
    "glob",
    "pid",
    "pwd",
    "close",
    "eof",
    "fblocked",
    "fconfigure",
    "fcopy",
    "fileevent",
    "flush",
    "gets",
    "open",
    "puts",
    "read",
    "seek",
    "socket",
    "tell",
    "interp",
    "after",
    "auto_execok",
    "auto_load",
    "auto_mkindex",
    "auto_reset",
    "bgerror",
    "error",
    "global",
    "history",
    "load",
    "source",
    "time",
    "trace",
    "unknown",
    "unset",
    "update",
    "vwait",
    "winfo",
    "wm",
    "bind",
    "event",
    "pack",
    "place",
    "grid",
    "font",
    "bell",
    "clipboard",
    "destroy",
    "focus",
    "grab",
    "lower",
    "option",
    "raise",
    "selection",
    "send",
    "tk",
    "tkwait",
    "tk_bisque",
    "tk_focusNext",
    "tk_focusPrev",
    "tk_focusFollowsMouse",
    "tk_popup",
    "tk_setPalette"
  ],
  symbols: /[=><!~?:&|+\-*\/\^%]+/,
  brackets: [
    { open: "(", close: ")", token: "delimiter.parenthesis" },
    { open: "{", close: "}", token: "delimiter.curly" },
    { open: "[", close: "]", token: "delimiter.square" }
  ],
  escapes: /\\(?:[abfnrtv\\"'\[\]\{\};\$]|x[0-9A-Fa-f]{1,4}|u[0-9A-Fa-f]{4}|U[0-9A-Fa-f]{8})/,
  variables: /(?:\$+(?:(?:\:\:?)?[a-zA-Z_]\w*)+)/,
  tokenizer: {
    root: [
      // identifiers and keywords
      [
        /[a-zA-Z_]\w*/,
        {
          cases: {
            "@specialFunctions": {
              token: "keyword.flow",
              next: "@specialFunc"
            },
            "@mainFunctions": "keyword",
            "@builtinFunctions": "variable",
            "@default": "operator.scss"
          }
        }
      ],
      [/\s+\-+(?!\d|\.)\w*|{\*}/, "metatag"],
      // whitespace
      { include: "@whitespace" },
      // delimiters and operators
      [/[{}()\[\]]/, "@brackets"],
      [/@symbols/, "operator"],
      [/\$+(?:\:\:)?\{/, { token: "identifier", next: "@nestedVariable" }],
      [/@variables/, "type.identifier"],
      [/\.(?!\d|\.)[\w\-]*/, "operator.sql"],
      // numbers
      [/\d+(\.\d+)?/, "number"],
      [/\d+/, "number"],
      // delimiter
      [/;/, "delimiter"],
      // strings
      [/"/, { token: "string.quote", bracket: "@open", next: "@dstring" }],
      [/'/, { token: "string.quote", bracket: "@open", next: "@sstring" }]
    ],
    dstring: [
      [/\[/, { token: "@brackets", next: "@nestedCall" }],
      [/\$+(?:\:\:)?\{/, { token: "identifier", next: "@nestedVariable" }],
      [/@variables/, "type.identifier"],
      [/[^\\$\[\]"]+/, "string"],
      [/@escapes/, "string.escape"],
      [/"/, { token: "string.quote", bracket: "@close", next: "@pop" }]
    ],
    sstring: [
      [/\[/, { token: "@brackets", next: "@nestedCall" }],
      [/\$+(?:\:\:)?\{/, { token: "identifier", next: "@nestedVariable" }],
      [/@variables/, "type.identifier"],
      [/[^\\$\[\]']+/, "string"],
      [/@escapes/, "string.escape"],
      [/'/, { token: "string.quote", bracket: "@close", next: "@pop" }]
    ],
    whitespace: [
      [/[ \t\r\n]+/, "white"],
      [/#.*\\$/, { token: "comment", next: "@newlineComment" }],
      [/#.*(?!\\)$/, "comment"]
    ],
    newlineComment: [
      [/.*\\$/, "comment"],
      [/.*(?!\\)$/, { token: "comment", next: "@pop" }]
    ],
    nestedVariable: [
      [/[^\{\}\$]+/, "type.identifier"],
      [/\}/, { token: "identifier", next: "@pop" }]
    ],
    nestedCall: [
      [/\[/, { token: "@brackets", next: "@nestedCall" }],
      [/\]/, { token: "@brackets", next: "@pop" }],
      { include: "root" }
    ],
    specialFunc: [
      [/"/, { token: "string", next: "@dstring" }],
      [/'/, { token: "string", next: "@sstring" }],
      [/\S+/, { token: "type", next: "@pop" }]
    ]
  }
};
export {
  conf,
  language
};
