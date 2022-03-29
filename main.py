#!/usr/bin/python3
import argparse as ap
import jsonConfig, createTcl

def scan(args):
    config = jsonConfig.PdConfig()
    config.addIp(
        (args.ip, args.dir)
    )
    config.buildMmmcView()
    config.writeJson(args.output)
    return args

def view(args):
    config = jsonConfig.PdConfig().readJson(args.json)
    factory = createTcl.TclFactory(config)
    factory.printMMMCFile(args.output)
    return args

parser = ap.ArgumentParser()

subparsers = parser.add_subparsers(help="sub parser description")

scanParser = subparsers.add_parser("scan")
# scanParser.set_defaults(scanner=)
scanParser.add_argument("--ip", help="IP Name", required=True)
scanParser.add_argument("--dir", help="IP directory", required=True)
scanParser.add_argument("-o", "--output", help="output json config file name", required=False, default="config.json")
scanParser.set_defaults(func=scan)

viewParser = subparsers.add_parser("view")
viewParser.add_argument("-j", "--json", help="input config json file", required=False, default="config.json")
viewParser.add_argument('-o', '--output', help="output view file", required=True)
viewParser.set_defaults(func=view)

args = parser.parse_args()
args.func(args)
