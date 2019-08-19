#!/usr/bin/env python3
# encoding: utf-8

import os
import sys
import datetime
import argparse

import blacklist

parser = argparse.ArgumentParser(description="TCTautomated.")
parser.add_argument(
    "--name", "-n", default="tct", help="Test name and where look custom files."
)
parser.add_argument(
    "--dir", "-d", default="tests", help="Destination path to write generated files."
)
parser.add_argument("--efl", "-e", default=None, help="Efl Root Path")
parser.add_argument("--cls", "-c", default=None, help="Eolian Class")
parser.add_argument("--verbose", "-v", default=False, action="store_true")
args = parser.parse_args()
if not os.path.exists(args.dir):
    os.makedirs(args.dir)

script_path = os.path.dirname(os.path.realpath(__file__))
root_path = (
    args.efl if args.efl else os.environ["EFL_DIR"] if "EFL_DIR" in os.environ else "."
)
sys.path.insert(0, os.path.join(root_path, "src", "scripts"))

try:
    from pyolian import eolian
    from pyolian import pyratemp
    from testgen import suitegen
    from testgen import name_helpers
except ModuleNotFoundError as ex:
    if args.verbose:
        print(ex)
    print(
        "Efl root path not found, use EFL_DIR environment variable "
        "with efl root path in your system\n"
    )
    parser.print_help()
    sys.exit(-1)


class Template(pyratemp.Template):
    def __init__(
        self,
        filename,
        encoding="utf-8",
        loader_class=pyratemp.LoaderFile,
        parser_class=pyratemp.Parser,
        renderer_class=pyratemp.Renderer,
        eval_class=pyratemp.EvalPseudoSandbox,
    ):

        global_ctx = {}
        global_ctx.update(
            {
                # Template info
                "date": datetime.datetime.now(),
                "template_file": os.path.basename(filename),
            }
        )

        self.template_filename = filename
        pyratemp.Template.__init__(
            self,
            filename=filename,
            encoding=encoding,
            data=global_ctx,
            loader_class=loader_class,
            parser_class=parser_class,
            renderer_class=renderer_class,
            eval_class=eval_class,
        )

    def render(self, suite):
        # Build the context for the template
        ctx = {}
        ctx["suite"] = suite
        ctx["name_helpers"] = name_helpers
        ctx["skips"] = blacklist
        # render with the augmented context
        output = self(**ctx)

        if suite.filename is not None:
            # write to file
            with open(suite.filename, "w") as f:
                f.write(output)


def load_class(eocls):
    """Loads data for the given class and generate tests"""

    if blacklist.should_skip_class(eocls):
        return

    name = "_".join([args.name, eocls.name.replace(".", "_")])
    suite = suitegen.SuiteGen(
        args.name,
        name,
        "{}.cs".format(os.path.join(args.dir, name)),
        args.name,
        "tct_suite.template",
    )
    suite.loadObj(eocls)
    t = Template(suite.template)
    t.render(suite)


def main():
    """Main entry point"""

    # Use .eo files from the source tree (not the installed ones)
    scan_folder = os.path.join(root_path, "src", "lib")

    # create main eolian state
    eolian_db = eolian.Eolian_State()
    if not isinstance(eolian_db, eolian.Eolian_State):
        raise RuntimeError("Eolian, failed to create Eolian state")

    # eolian source tree scan
    if not eolian_db.directory_add(scan_folder):
        raise RuntimeError("Eolian, failed to scan source directory")

    # Parse all known eo files
    if not eolian_db.all_eot_files_parse():
        raise RuntimeError("Eolian, failed to parse all EOT files")

    if not eolian_db.all_eo_files_parse():
        raise RuntimeError("Eolian, failed to parse all EO files")

    if args.cls:
        eocls = eolian_db.class_by_name_get(args.cls)
        if not eocls:
            print("Eolian class {} Not found!!".format(args.cls))
        load_class(eocls)
    else:
        for eocls in eolian_db.classes:
            load_class(eocls)

    del eolian_db


if __name__ == "__main__":
    main()
