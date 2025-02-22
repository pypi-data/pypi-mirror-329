/*!-----------------------------------------------------------------------------
 * Copyright (c) Microsoft Corporation. All rights reserved.
 * Version: 0.49.0(383fdf3fc0e1e1a024068b8d0fd4f3dcbae74d04)
 * Released under the MIT license
 * https://github.com/microsoft/monaco-editor/blob/main/LICENSE.txt
 *-----------------------------------------------------------------------------*/var e={comments:{lineComment:"#"},brackets:[["{","}"],["[","]"],["(",")"]],surroundingPairs:[{open:"{",close:"}"},{open:"[",close:"]"},{open:"(",close:")"},{open:"'",close:"'"},{open:'"',close:'"'}],autoClosingPairs:[{open:"'",close:"'",notIn:["string","comment"]},{open:'"',close:'"',notIn:["comment"]},{open:'"""',close:'"""'},{open:"`",close:"`",notIn:["string","comment"]},{open:"(",close:")"},{open:"{",close:"}"},{open:"[",close:"]"},{open:"<<",close:">>"}],indentationRules:{increaseIndentPattern:/^\s*(after|else|catch|rescue|fn|[^#]*(do|<\-|\->|\{|\[|\=))\s*$/,decreaseIndentPattern:/^\s*((\}|\])\s*$|(after|else|catch|rescue|end)\b)/}},t={defaultToken:"source",tokenPostfix:".elixir",brackets:[{open:"[",close:"]",token:"delimiter.square"},{open:"(",close:")",token:"delimiter.parenthesis"},{open:"{",close:"}",token:"delimiter.curly"},{open:"<<",close:">>",token:"delimiter.angle.special"}],declarationKeywords:["def","defp","defn","defnp","defguard","defguardp","defmacro","defmacrop","defdelegate","defcallback","defmacrocallback","defmodule","defprotocol","defexception","defimpl","defstruct"],operatorKeywords:["and","in","not","or","when"],namespaceKeywords:["alias","import","require","use"],otherKeywords:["after","case","catch","cond","do","else","end","fn","for","if","quote","raise","receive","rescue","super","throw","try","unless","unquote_splicing","unquote","with"],constants:["true","false","nil"],nameBuiltin:["__MODULE__","__DIR__","__ENV__","__CALLER__","__STACKTRACE__"],operator:/-[->]?|!={0,2}|\*{1,2}|\/|\\\\|&{1,3}|\.\.?|\^(?:\^\^)?|\+\+?|<(?:-|<<|=|>|\|>|~>?)?|=~|={1,3}|>(?:=|>>)?|\|~>|\|>|\|{1,3}|~>>?|~~~|::/,variableName:/[a-z_][a-zA-Z0-9_]*[?!]?/,atomName:/[a-zA-Z_][a-zA-Z0-9_@]*[?!]?|@specialAtomName|@operator/,specialAtomName:/\.\.\.|<<>>|%\{\}|%|\{\}/,aliasPart:/[A-Z][a-zA-Z0-9_]*/,moduleName:/@aliasPart(?:\.@aliasPart)*/,sigilSymmetricDelimiter:/"""|'''|"|'|\/|\|/,sigilStartDelimiter:/@sigilSymmetricDelimiter|<|\{|\[|\(/,sigilEndDelimiter:/@sigilSymmetricDelimiter|>|\}|\]|\)/,sigilModifiers:/[a-zA-Z0-9]*/,decimal:/\d(?:_?\d)*/,hex:/[0-9a-fA-F](_?[0-9a-fA-F])*/,octal:/[0-7](_?[0-7])*/,binary:/[01](_?[01])*/,escape:/\\u[0-9a-fA-F]{4}|\\x[0-9a-fA-F]{2}|\\./,tokenizer:{root:[{include:"@whitespace"},{include:"@comments"},{include:"@keywordsShorthand"},{include:"@numbers"},{include:"@identifiers"},{include:"@strings"},{include:"@atoms"},{include:"@sigils"},{include:"@attributes"},{include:"@symbols"}],whitespace:[[/\s+/,"white"]],comments:[[/(#)(.*)/,["comment.punctuation","comment"]]],keywordsShorthand:[[/(@atomName)(:)(\s+)/,["constant","constant.punctuation","white"]],[/"(?=([^"]|#\{.*?\}|\\")*":)/,{token:"constant.delimiter",next:"@doubleQuotedStringKeyword"}],[/'(?=([^']|#\{.*?\}|\\')*':)/,{token:"constant.delimiter",next:"@singleQuotedStringKeyword"}]],doubleQuotedStringKeyword:[[/":/,{token:"constant.delimiter",next:"@pop"}],{include:"@stringConstantContentInterpol"}],singleQuotedStringKeyword:[[/':/,{token:"constant.delimiter",next:"@pop"}],{include:"@stringConstantContentInterpol"}],numbers:[[/0b@binary/,"number.binary"],[/0o@octal/,"number.octal"],[/0x@hex/,"number.hex"],[/@decimal\.@decimal([eE]-?@decimal)?/,"number.float"],[/@decimal/,"number"]],identifiers:[[/\b(defp?|defnp?|defmacrop?|defguardp?|defdelegate)(\s+)(@variableName)(?!\s+@operator)/,["keyword.declaration","white",{cases:{unquote:"keyword","@default":"function"}}]],[/(@variableName)(?=\s*\.?\s*\()/,{cases:{"@declarationKeywords":"keyword.declaration","@namespaceKeywords":"keyword","@otherKeywords":"keyword","@default":"function.call"}}],[/(@moduleName)(\s*)(\.)(\s*)(@variableName)/,["type.identifier","white","operator","white","function.call"]],[/(:)(@atomName)(\s*)(\.)(\s*)(@variableName)/,["constant.punctuation","constant","white","operator","white","function.call"]],[/(\|>)(\s*)(@variableName)/,["operator","white",{cases:{"@otherKeywords":"keyword","@default":"function.call"}}]],[/(&)(\s*)(@variableName)/,["operator","white","function.call"]],[/@variableName/,{cases:{"@declarationKeywords":"keyword.declaration","@operatorKeywords":"keyword.operator","@namespaceKeywords":"keyword","@otherKeywords":"keyword","@constants":"constant.language","@nameBuiltin":"variable.language","_.*":"comment.unused","@default":"identifier"}}],[/@moduleName/,"type.identifier"]],strings:[[/"""/,{token:"string.delimiter",next:"@doubleQuotedHeredoc"}],[/'''/,{token:"string.delimiter",next:"@singleQuotedHeredoc"}],[/"/,{token:"string.delimiter",next:"@doubleQuotedString"}],[/'/,{token:"string.delimiter",next:"@singleQuotedString"}]],doubleQuotedHeredoc:[[/"""/,{token:"string.delimiter",next:"@pop"}],{include:"@stringContentInterpol"}],singleQuotedHeredoc:[[/'''/,{token:"string.delimiter",next:"@pop"}],{include:"@stringContentInterpol"}],doubleQuotedString:[[/"/,{token:"string.delimiter",next:"@pop"}],{include:"@stringContentInterpol"}],singleQuotedString:[[/'/,{token:"string.delimiter",next:"@pop"}],{include:"@stringContentInterpol"}],atoms:[[/(:)(@atomName)/,["constant.punctuation","constant"]],[/:"/,{token:"constant.delimiter",next:"@doubleQuotedStringAtom"}],[/:'/,{token:"constant.delimiter",next:"@singleQuotedStringAtom"}]],doubleQuotedStringAtom:[[/"/,{token:"constant.delimiter",next:"@pop"}],{include:"@stringConstantContentInterpol"}],singleQuotedStringAtom:[[/'/,{token:"constant.delimiter",next:"@pop"}],{include:"@stringConstantContentInterpol"}],sigils:[[/~[a-z]@sigilStartDelimiter/,{token:"@rematch",next:"@sigil.interpol"}],[/~([A-Z]+)@sigilStartDelimiter/,{token:"@rematch",next:"@sigil.noInterpol"}]],sigil:[[/~([a-z]|[A-Z]+)\{/,{token:"@rematch",switchTo:"@sigilStart.$S2.$1.{.}"}],[/~([a-z]|[A-Z]+)\[/,{token:"@rematch",switchTo:"@sigilStart.$S2.$1.[.]"}],[/~([a-z]|[A-Z]+)\(/,{token:"@rematch",switchTo:"@sigilStart.$S2.$1.(.)"}],[/~([a-z]|[A-Z]+)\</,{token:"@rematch",switchTo:"@sigilStart.$S2.$1.<.>"}],[/~([a-z]|[A-Z]+)(@sigilSymmetricDelimiter)/,{token:"@rematch",switchTo:"@sigilStart.$S2.$1.$2.$2"}]],"sigilStart.interpol.s":[[/~s@sigilStartDelimiter/,{token:"string.delimiter",switchTo:"@sigilContinue.$S2.$S3.$S4.$S5"}]],"sigilContinue.interpol.s":[[/(@sigilEndDelimiter)@sigilModifiers/,{cases:{"$1==$S5":{token:"string.delimiter",next:"@pop"},"@default":"string"}}],{include:"@stringContentInterpol"}],"sigilStart.noInterpol.S":[[/~S@sigilStartDelimiter/,{token:"string.delimiter",switchTo:"@sigilContinue.$S2.$S3.$S4.$S5"}]],"sigilContinue.noInterpol.S":[[/(^|[^\\])\\@sigilEndDelimiter/,"string"],[/(@sigilEndDelimiter)@sigilModifiers/,{cases:{"$1==$S5":{token:"string.delimiter",next:"@pop"},"@default":"string"}}],{include:"@stringContent"}],"sigilStart.interpol.r":[[/~r@sigilStartDelimiter/,{token:"regexp.delimiter",switchTo:"@sigilContinue.$S2.$S3.$S4.$S5"}]],"sigilContinue.interpol.r":[[/(@sigilEndDelimiter)@sigilModifiers/,{cases:{"$1==$S5":{token:"regexp.delimiter",next:"@pop"},"@default":"regexp"}}],{include:"@regexpContentInterpol"}],"sigilStart.noInterpol.R":[[/~R@sigilStartDelimiter/,{token:"regexp.delimiter",switchTo:"@sigilContinue.$S2.$S3.$S4.$S5"}]],"sigilContinue.noInterpol.R":[[/(^|[^\\])\\@sigilEndDelimiter/,"regexp"],[/(@sigilEndDelimiter)@sigilModifiers/,{cases:{"$1==$S5":{token:"regexp.delimiter",next:"@pop"},"@default":"regexp"}}],{include:"@regexpContent"}],"sigilStart.interpol":[[/~([a-z]|[A-Z]+)@sigilStartDelimiter/,{token:"sigil.delimiter",switchTo:"@sigilContinue.$S2.$S3.$S4.$S5"}]],"sigilContinue.interpol":[[/(@sigilEndDelimiter)@sigilModifiers/,{cases:{"$1==$S5":{token:"sigil.delimiter",next:"@pop"},"@default":"sigil"}}],{include:"@sigilContentInterpol"}],"sigilStart.noInterpol":[[/~([a-z]|[A-Z]+)@sigilStartDelimiter/,{token:"sigil.delimiter",switchTo:"@sigilContinue.$S2.$S3.$S4.$S5"}]],"sigilContinue.noInterpol":[[/(^|[^\\])\\@sigilEndDelimiter/,"sigil"],[/(@sigilEndDelimiter)@sigilModifiers/,{cases:{"$1==$S5":{token:"sigil.delimiter",next:"@pop"},"@default":"sigil"}}],{include:"@sigilContent"}],attributes:[[/\@(module|type)?doc (~[sS])?"""/,{token:"comment.block.documentation",next:"@doubleQuotedHeredocDocstring"}],[/\@(module|type)?doc (~[sS])?'''/,{token:"comment.block.documentation",next:"@singleQuotedHeredocDocstring"}],[/\@(module|type)?doc (~[sS])?"/,{token:"comment.block.documentation",next:"@doubleQuotedStringDocstring"}],[/\@(module|type)?doc (~[sS])?'/,{token:"comment.block.documentation",next:"@singleQuotedStringDocstring"}],[/\@(module|type)?doc false/,"comment.block.documentation"],[/\@(@variableName)/,"variable"]],doubleQuotedHeredocDocstring:[[/"""/,{token:"comment.block.documentation",next:"@pop"}],{include:"@docstringContent"}],singleQuotedHeredocDocstring:[[/'''/,{token:"comment.block.documentation",next:"@pop"}],{include:"@docstringContent"}],doubleQuotedStringDocstring:[[/"/,{token:"comment.block.documentation",next:"@pop"}],{include:"@docstringContent"}],singleQuotedStringDocstring:[[/'/,{token:"comment.block.documentation",next:"@pop"}],{include:"@docstringContent"}],symbols:[[/\?(\\.|[^\\\s])/,"number.constant"],[/&\d+/,"operator"],[/<<<|>>>/,"operator"],[/[()\[\]\{\}]|<<|>>/,"@brackets"],[/\.\.\./,"identifier"],[/=>/,"punctuation"],[/@operator/,"operator"],[/[:;,.%]/,"punctuation"]],stringContentInterpol:[{include:"@interpolation"},{include:"@escapeChar"},{include:"@stringContent"}],stringContent:[[/./,"string"]],stringConstantContentInterpol:[{include:"@interpolation"},{include:"@escapeChar"},{include:"@stringConstantContent"}],stringConstantContent:[[/./,"constant"]],regexpContentInterpol:[{include:"@interpolation"},{include:"@escapeChar"},{include:"@regexpContent"}],regexpContent:[[/(\s)(#)(\s.*)$/,["white","comment.punctuation","comment"]],[/./,"regexp"]],sigilContentInterpol:[{include:"@interpolation"},{include:"@escapeChar"},{include:"@sigilContent"}],sigilContent:[[/./,"sigil"]],docstringContent:[[/./,"comment.block.documentation"]],escapeChar:[[/@escape/,"constant.character.escape"]],interpolation:[[/#{/,{token:"delimiter.bracket.embed",next:"@interpolationContinue"}]],interpolationContinue:[[/}/,{token:"delimiter.bracket.embed",next:"@pop"}],{include:"@root"}]}};export{e as conf,t as language};
