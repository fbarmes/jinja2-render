#!/usr/bin/env python3
#
# jinja-render <infile> <varfile> [... <varfile> ]
#
# TODO : add multiple -e for extra vars
#
#
# sudo pip3 install jinja2 pyyaml
#
#
#

import os
import sys;
import argparse
import logging


import jinja2
from jinja2.meta import find_undeclared_variables
import yaml


#-------------------------------------------------------------------------------
def handle_arguments():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )


    parser.add_argument(
        'infile',
        type=str,
        help='jinja2 template',
    )

    parser.add_argument(
        'varfiles',
        nargs='+',
        type=str,
        help='var file',
    )

    parser.add_argument(
        '-o', '--outfile',
        type=str,
        help='output file',
    )

    parser.add_argument(
        '-e', '--extra_vars',
        action='append',
        type=str,
        help='extra variables',
    )


    args = parser.parse_args();

    return args;


#-------------------------------------------------------------------------------
def render(jinja_env, template_file, varfiles, extra_vars):

    #-- load variables
    data = {}
    for varfile in varfiles:
        with open(varfile) as file:
            yaml_dict=yaml.load(file,Loader=yaml.FullLoader)
            data.update(yaml_dict)

    #-- handle extra vars
    if extra_vars:
        logging.info("in render extra_vars: " + ', '.join(extra_vars) )
        for extra_var in extra_vars:
            split=extra_var.split('=',1)
            if( len(split) != 2):
                error_msg="Malformated extra_var ["+extra_var+"]"
                logging.error(error_msg)
                exit(error_msg)
            data[split[0]]=split[1]

    #-- load template
    template = jinja_env.get_template(template_file)

    #-- render until all variables rendered
    result=iterative_render(template,data)
    return result;


#-------------------------------------------------------------------------------
def iterative_render(template, values):
    prev=template.render(values)
    while True:
        curr = jinja2.Template(prev).render(**values)
        if curr != prev:
            prev = curr
        else:
            return curr

#-------------------------------------------------------------------------------
def write_to_file(data,filename):
    #-- open file
    fh = open(filename,"w")
    #-- write data
    fh.write(data)
    #-- close file
    fh.close()


#-------------------------------------------------------------------------------
def main():

    #-- setup log level
    logging.getLogger().setLevel(os.environ.get("LOGLEVEL", "DEBUG"))

    #-- Title
    logging.info("======= JINJA Render ========")

    #-- handle arguments
    args=handle_arguments()
    infilePath=os.path.dirname(args.infile)
    infileName=os.path.basename(args.infile)


    logging.info("infile: " + args.infile)

    if(args.outfile):
        logging.info("varfiles: " + ', '.join(args.varfiles) )
        logging.info("outfile: " + args.outfile)

    if(args.extra_vars):
        logging.info("-- extra vars")
        logging.info("extra_vars: " + ', '.join(args.extra_vars) )

    #-- Setup jinja env
    logging.info("Setup jinja env")
    LoggingUndefined = jinja2.make_logging_undefined(logger=logging.getLogger(),base=jinja2.Undefined)
    jinja_env = jinja2.Environment(
        autoescape=False,
        trim_blocks=False,
        loader=jinja2.FileSystemLoader(infilePath),
        undefined=jinja2.StrictUndefined,
    )

    #-- Render template
    logging.info("Render")
    if args.extra_vars:
        extra_vars=args.extra_vars
    else:
        extra_vars=None

    result = render(jinja_env, infileName,args.varfiles,extra_vars);

    #-- check for errors
    ast = jinja_env.parse(args.infile)
    undefined = find_undeclared_variables(ast)
    if undefined:
        raise jinja2.UndefinedError(f'The following variables are undefined: {undefined!r}')

    #-- Output result
    if args.outfile:
        logging.info("Write result to "+args.outfile)
        write_to_file(result,args.outfile)
    else:
        logging.info("======= Output ========")
        print(result)

#-------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
