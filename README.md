# pygments.formatters.context

This is a [Pygments](http://http://pygments.org/) formatter that formats tokens as  [ConTeXt](http://wiki.contextgarden.net/What_is_ConTeXt) 'verbatim' code.

## Installation

    sudo python setup.py install
   
## Using
To run Pygments, formatting as ConTeXt:

    pygmentize <input options> -f context -o out.tex

To run Pygments, and dump a 'stylesheet' for a given style

    pygmentize -f context -S <style>

The following options are supported:

* codename : the name of the type of typing block to create; defaults to `code`; e.g., if `foo` is specified, this will generate blocks like:
        
        \startfoo
        ...
        \stopfoo

* escapeopen : the tag to use to begin ConTeXt commands within the block; defaults to `/BTEX`
* escapeclose : the tag to use to end ConTeXt commands within the block; defaults to `/ETEX`
* commandprefix : a prefix for all generated colors and macros; defaults to `PYG`

## Details

This implementation registers the package as a proper Pygments plugin which you can use from within Python, e.g.:

    from pygments.formatters import (get_formatter_by_name)
    get_formatter_by_name('context', options)

should return `<pygments.formatters.ContextFormatter>`. 


