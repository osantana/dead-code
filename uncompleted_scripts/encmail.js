/*
 * encmail.js - Hide e-mails from spammers.
 *
 * Copyright 2007 (c) Osvaldo Santana Neto <osantana@gmail.com>
 *
 * This library is licensed under LGPL.
 *
 * Usage examples:
 *    <a href="mailto:n90qe0q0p-y0ti_+ny" onClick="translate(this);">
 *       Osvaldo Santana Neto
 *    </a>
 *    <a href="mailto:n90qe0q0p-y0ti_+ny" onClick="translate(this);">
 *       <script>decode_mail("n90qe0q0p-y0ti_+ny");</script>
 *    </a>
 *    or
 *    <script>mailto("n90qe0q0p-y0ti_+ny", "Osvaldo Santana Neto");</script>
 *    <script>mailto("n90qe0q0p-y0ti_+ny");</script>
 *
 *    ... and you can use the code below to generate the server side
 *    encryption code:
 *
 *    <pre><script>gen_server_code("python");</script></pre>
 *
 * This library uses a simple and *unsecure* Substitution Cypher System. You
 * can change this reimplementing the decode() function.
 *
 * The main purpose of this library is to prove the concept of changing the
 * href attribute on mouse click.
 *
 */

var dec = "abcdefghijklmnopqrstuvwxyz@.-_+0123456789";
var enc = '0v+a8s-xt3hiyqnmbl9efw4@c.p_1j2kd56ou7rgz';

function gen_server_code(lang) {
    var code = "";
    if (lang == "python") {
        code = "import string\n\n";
        code += "dec = '" + dec + "'\n";
        code += "enc = '" + enc + "'\n\n";
        code += "trans = string.maketrans(dec, enc)\n"
        code += "encode = lambda s: s.translate(trans)\n";
    } else {
        code = "unknown language '" + lang + "'";
    }
    window.document.write(code);
}

function decode(str) {
    var char_pos;
    var current_char;
    var decoded_str = "";

    for (var i = 0; i < str.length; ++i) {
        current_char = str.charAt(i);
        char_pos = enc.indexOf(current_char);
        if (char_pos < 0) {
            decoded_str += current_char;
        } else {
            decoded_str += dec.charAt(char_pos);
        }
    }

    return decoded_str;
}

function translate(node) {
    if (!node.href && node.href.indexOf("mailto:"))
        return;

    var encmail = node.href.replace(/^mailto:/, "");
    node.href = "mailto:" + decode(encmail);
    return true;
}

function decode_mail(str) {
    window.document.write(decode(str));
}

function mailto(encoded_email, text) {
    var content = "";

    if (!text)
        text = decode(encoded_email);

    content = "<a href=\"mailto:" + decode(encoded_email) + "\">";
    content += text;
    content += "</a>";
    window.document.write(content);
}

// vim:ts=4:sw=4:tw=0:si:ai:et:sm
