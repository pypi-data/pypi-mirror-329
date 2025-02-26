#! /usr/bin/env python3


import os
import re
import sys
import ast
import shlex
import argparse
import pathlib
import sysconfig
from .py3prov import generate_provides, search_for_provides, genprov_from_env


def _remove_reduntant_args(func):
    def remover(*args, **kwargs):
        return func(**dict(filter(lambda arg: arg[0] in func.__code__.co_varnames,
                           kwargs.items())))
    return remover


def is_import_stmt(node):
    '''
    Checks if statement is builtin import method - __init__()
    '''
    if type(node) == ast.Call and type(node.func) == ast.Name\
       and node.func.id == '__import__' and node.args\
       and type(node.args[0]) == ast.Constant:
        return node.args[0]


def is_importlib_call(node):
    '''
    Checks if statement is import function from module importlib -
    importlib.import_module()
    '''
    if type(node) == ast.Call and type(node.func) == ast.Attribute\
            and type(node.func.value) == ast.Name\
            and node.func.value.id == 'importlib'\
            and node.func.attr == 'import_module'\
            and type(node.args[0]) == ast.Constant:
        return node.args[0]


def build_full_qualified_name(path, level, dependency=None, prefixes=[]):
    '''
    Creates fully qualified name for the specified dependency name (usefull for relative imports)

    :param path: path to file with relative import
    :type path: str or pathlib.Path
    :param level: level of import (number of leading dots)
    :type level: int
    :param dependency: dependency name
    :type depdendency: int
    :param prefixes: list of prefixes by which the path will be trimmed
    :type prefixes: list[str] or list[pathlib.Path]
    :return: dependency name
    :rtype: str
    '''
    parent_path = pathlib.Path(path).absolute().parts[1:-level]
    parent_path = ''.join(f'/{p}' for p in parent_path)
    for pref in sorted(prefixes, key=lambda k: len(k.split('/')), reverse=True):
        if pref and (path_pref := re.match(r'%s/' % re.escape(pref), parent_path)):
            parent_path = re.sub(re.escape(path_pref.group()), '', parent_path)
    parent = '.'.join(name for name in parent_path.split('/') if name)

    if dependency:
        return f'{parent}.{dependency}' if parent else f'{dependency}'
    return parent


def _list_pkgs(path, level):
    path = pathlib.Path(path)
    pathes = [path.absolute().as_posix()]
    if level > 0:
        if path.is_dir():
            pathes.append(path.absolute().as_posix())
            for p in path.iterdir():
                pathes += _list_pkgs(p, level - 1)
    return pathes


def _form_std_provides():
    std_lib = set([sysconfig.get_paths()['stdlib'], sysconfig.get_paths()['platstdlib']])

    # It's possible that on OSes like Debian, std_lib may contain site(dist)-packages
    site_pkgs = set([sysconfig.get_paths()['purelib'], sysconfig.get_paths()['platlib']])
    to_exclude = sum(map(lambda path: [(pref, len(path.split('/')) - len(pref.split('/')))
                                       for pref in std_lib if path.startswith(pref)], site_pkgs), start=[])
    to_exclude = {pref: length for pref, length in sorted(to_exclude, key=lambda k: k[1])}
    pathes = list(std_lib)
    pathes += sum([_list_pkgs(path, level) for path, level in to_exclude.items()], start=[])
    pathes = list(filter(lambda p: p not in site_pkgs | set(to_exclude.keys()), pathes))

    return pathes


def get_text(path, size=-1, verbose=False):
    '''
    Returns text for giving path
    (will be hidden soon)

    :param path: path to the file
    :type path: str or pathlib.Path
    :param size: number of bytes to read
    :type size: int
    :param verbose: turn on verbose mode
    :type verbose: Bool
    :return: bytes from file or None if one of known exceptions occures
    :rtype: bytes or None
    '''
    try:
        with open(path, mode='rb') as f:
            return f.read(size)
    except FileNotFoundError:
        if verbose:
            print(f'No such file:{path}', file=sys.stderr)
        return None
    except PermissionError:
        if verbose:
            print(f'Permission denied:{path}', file=sys.stderr)
        return None
    except IsADirectoryError:
        return None


def catch_so(path, stderr):
    '''
    Process ELF and returns python3-ABI dependency
    :param path: path to ELF file
    :type path: str or pathlib.Path
    :param stderr: stderr (io)
    :type stderr: io
    :return: python3-ABI dependency
    :rtype: str or None
    '''
    dep_version = os.getenv('RPM_PYTHON3_VERSION', '%s.%s' % sys.version_info[0:2])
    try:
        bit_depth = get_text(path, size=5)[4]
    except IndexError:
        print(f'py3req.py:Catched error for ELF:{path}, possibly file is empty or broken', file=stderr)
        bit_depth = None

    match bit_depth:
        case 1:
            return f'python{dep_version}-ABI'
        case 2:
            return f'python{dep_version}-ABI(64bit)'
        case _:
            print(f'py3req.py: Wrong ELF-class for file {path}', file=stderr)
            return None


def _find_imports_in_ast(path, code, Node, prefixes, only_external_deps,
                         skip_subs, stderr, verbose):
    abs_deps = {}
    rel_deps = {}
    adv_deps = {}
    skip_deps = {}

    for node in ast.parse(code).body if code else ast.iter_child_nodes(Node):
        if isinstance(node, ast.Import):
            for name in node.names:
                abs_deps.setdefault(name.name, []).append(name.lineno)
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0:
                module = node.module
                if skip_subs:
                    abs_deps.setdefault(module, []).append(node.lineno)
                else:
                    for name in node.names:
                        mod_name = f'{module}.{name.name}'
                        abs_deps.setdefault(mod_name, []).append(name.lineno)
            else:
                module = build_full_qualified_name(path, node.level, node.module, prefixes)
                if skip_subs:
                    rel_deps.setdefault(module, []).append(node.lineno)
                else:
                    for name in node.names:
                        mod_name = f'{module}.{name.name}'
                        rel_deps.setdefault(mod_name, []).append(node.lineno)

        elif (dep := is_import_stmt(node)) or (dep := is_importlib_call(node)):
            if dep.value in adv_deps:
                adv_deps[dep.value].append(node.lineno)
            else:
                adv_deps[dep.value] = [node.lineno]

        elif only_external_deps:
            for tmp in _find_imports_in_ast(path=path, code=None, Node=node, prefixes=prefixes,
                                            only_external_deps=only_external_deps,
                                            skip_subs=skip_subs, stderr=stderr,
                                            verbose=verbose):
                for dep, line in tmp.items():
                    skip_deps.setdefault(dep, []).append(line)
        else:
            tmp_abs, tmp_rel, tmp_adv, tp =\
                _find_imports_in_ast(path=path, code=None, Node=node, prefixes=prefixes,
                                     only_external_deps=only_external_deps,
                                     skip_subs=skip_subs, stderr=stderr, verbose=verbose)
            abs_deps.update(tmp_abs)
            rel_deps.update(tmp_rel)
            adv_deps.update(tmp_adv)
    return abs_deps, rel_deps, adv_deps, skip_deps


def read_ast_tree(path, code=None, prefixes=[], only_external_deps=False,
                  skip_subs=True, stderr=sys.stderr, verbose=True):
    '''
    Read AST for code from given path or even code and detect dependencies

    :param path: path to the file
    :type path: str or pathlib.Path
    :param code: code from script
    :type code: AST body
    :param prefixes: list of prefixes by which the path will be trimmed
    :type prefixes: list[str] or list[pathlib.Path]
    :param only_external_deps: skip capsulated import statements
    :type only_external_deps: Bool
    :path skip_subs: skip dependecy attribute (skip B for "from A import B")
    :type skip_subs: Bool
    :param stderr: error stream
    :type stderr: io
    :param verbose: turn on verbose flag
    :type verbose: Bool
    :return: tuple of dictionaries for absolute, relative, advanced (__import__ stmt) and skipped dependncies
    :rtype: tuple({}, {}, {}, {})
    '''
    if not code and not (code := get_text(path)):
        return {}, {}, {}, {}
    try:
        return _find_imports_in_ast(path, code, None, prefixes, only_external_deps,
                                    skip_subs, stderr, verbose)
    except (SyntaxError, ValueError) as msg:
        if verbose:
            print(f'py3req: error:{path}: invalid syntax', file=stderr)
            head, ext = os.path.splitext(path)
            if ext == '.py':
                print(f'py3req:{path}:{msg.msg}', file=stderr)
            else:
                print(f'py3req:{path}: possibly not pythonish file',
                      file=stderr)
        return {}, {}, {}, {}


def process_file(path, only_external_deps=False, skip_subs=False, prefixes=[],
                 stderr=sys.stderr, verbose=False):
    '''
    Generate dependencies for given path to file

    :param path: path to the file
    :type path: str or pathlib.Path
    :param only_external_deps: skip capsulated import statements
    :type only_external_deps: Bool
    :path skip_subs: skip dependecy attribute (skip B for "from A import B")
    :type skip_subs: Bool
    :param prefixes: list of prefixes by which the path will be trimmed
    :type prefixes: list[str] or list[pathlib.Path]
    :param stderr: error stream
    :type stderr: io
    :param verbose: turn on verbose flag
    :type verbose: Bool
    :return: tuple of dictionaries for absolute, relative, advanced (__import__ stmt) and skipped dependncies
    :rtype: tuple({}, {}, {}, {})
    '''
    if (code := get_text(path, verbose=verbose)):
        return read_ast_tree(path, code, prefixes=prefixes,
                             only_external_deps=only_external_deps,
                             skip_subs=skip_subs, stderr=stderr, verbose=verbose)
    return {}, {}, {}, {}


def filter_requirements(file, deps, provides=[], only_top_module=[], ignore_list=[],
                        skip_flag=False, stderr=sys.stderr,
                        verbose=False):
    '''
    This function filter requirements through self-provides, different rules and etc

    :param file: name of file, which contains dependencies
    :type file: str
    :param deps: list of dependencies
    :type deps: {str:[]}
    :param provides: list of provides (there can be self-provides)
    :type provides: list[str]
    :param only_top_module: for dependencies like a.b skip b
    :type only_top_module: Bool
    :param ignore_list: list of dependencies to be ignored
    :type ignore_list: list[str]
    :param skip_flag: with this flag deps will be skipped
    :type skip_flag: Bool
    :param stderr: messages output
    :type stderr: io
    :param verbose: verbose flag
    :type verbose: Bool
    :return: list of filtered deps
    :rtype: set[str]
    '''
    dependencies = set()

    for dep, lines in deps.items():
        if dep in ignore_list:
            if verbose:
                print(f'py3req:{file}: skipping "{dep}" lines:{lines}', file=stderr)
        elif dep in provides:
            if verbose:
                print(f'py3req:{file}: "{dep}" lines:{lines} is possibly a '
                      'self-providing dependency, skip it', file=stderr)
        elif skip_flag:
            if verbose:
                print(f'py3req:{file}: "{dep}" lines:{lines}: Ignore', file=stderr)
        else:
            if only_top_module:
                dep = dep.split('.')[0]
            dependencies.add(dep)

    return dependencies


@_remove_reduntant_args
def generate_requirements(files, add_prov_path=[], prefixes=sys.path,
                          ignore_list=sys.builtin_module_names, read_prov_from_file=None,
                          skip_subs=True, only_external_deps=False, only_top_module=False,
                          exclude_stdlib=False, inspect_env=False, env_path=[], stderr=sys.stderr, verbose=True):
    '''
    Generate dependencies for given file-list, filter them through detected provides and return in specified format.

    :param files: list of files
    :type files: list[str]
    :param add_prov_path: list of additional pathes for provides searching
    :type add_prov_path: list[str]
    :param prefixes: list of prefixes by which the path will be trimmed
    :type prefixes: list[str] or list[pathlib.Path]
    :param ignore_list: list of dependencies to be ignored
    :type ignore_list: list[str]
    :param read_prov_from_file: path to file with additional provides
    :type read_prov_from_file: str or pathlib.Path
    :path skip_subs: skip dependecy attribute (skip B for "from A import B")
    :type skip_subs: Bool
    :param only_external_deps: skip capsulated import statements
    :type only_external_deps: Bool
    :param only_top_module: for dependencies like a.b skip b
    :type only_top_module: Bool
    :param exclude_stdlib: exclude from dependencies standard lib provides
    :type exclude_stdlib: Bool
    :param inspect_env: inspect environment for installed packages and match with them requirements
    :type inspect_env: Bool
    :param env_path: path to the environment (useful for inspect_env option)
    :type env_path: [str]
    :param stderr: messages output
    :type stderr: io
    :param verbose: verbose flag
    :type verbose: Bool
    :return: tuple of dictionaries for absolute, relative, advanced (__import__ stmt) and skipped dependncies
    :rtype: tuple({}, {}, {}, {})
    '''
    full_provides = set()
    abs_provides = set()
    add_provides = set()
    modules = {}
    if not inspect_env:
        dependencies = {}
    else:
        dependencies = set()
        tmp_dependencies = set()

    if read_prov_from_file:
        with open(read_prov_from_file) as f:
            full_provides |= set([prov.rstrip() for prov in f.readlines()])

    for module, prov in generate_provides(files, skip_pth=True, deep_search=False, prefixes=prefixes,
                                          abs_mode=False, verbose=verbose, skip_wrong_names=False,
                                          skip_namespace_pkgs=False).items():
        if prov['package'] is not None:
            modules[module] = prov['package']
        full_provides |= set(prov['provides'])

    for module, prov in generate_provides(files, skip_pth=True, deep_search=False, prefixes=prefixes,
                                          abs_mode=True, verbose=verbose, skip_wrong_names=False,
                                          skip_namespace_pkgs=False).items():
        if prov['package'] is not None:
            modules[module] = prov['package']
        abs_provides |= set(prov['provides'])

    for path in filter(lambda p: p, add_prov_path):
        prov = search_for_provides(path, abs_mode=False, skip_wrong_names=False, skip_namespace_pkgs=False,
                                   verbose=verbose)
        add_provides |= set(prov)

    if exclude_stdlib:
        add_provides |= set(sum([search_for_provides(p, abs_mode=False,
                                                     skip_wrong_names=False, skip_namespace_pkgs=False, verbose=verbose)
                                 for p in _form_std_provides()], start=[]))
        # This module is provided by different real modules which are platform specific, such as posixpath.py
        add_provides.add("os.path")

    if inspect_env:
        env_path = set([sysconfig.get_paths()['purelib'],
                        sysconfig.get_paths()['platlib']]) if env_path == [] else env_path
        env_provides = genprov_from_env(paths=env_path, verbose=verbose)

    for file in files:
        if file.endswith('.so'):
            if (dep := catch_so(file, stderr)):
                if not inspect_env:
                    dependencies[file] = set(), set(), set(), set([dep])
                continue

        abs_deps, rel_deps, adv_deps, skip =\
            process_file(file, prefixes=prefixes, only_external_deps=only_external_deps,
                         skip_subs=skip_subs, stderr=stderr, verbose=verbose)

        if file in modules.keys() and '-' not in modules[file]:
            abs_deps = filter_requirements(file, abs_deps, abs_provides | add_provides,
                                           only_top_module, ignore_list,
                                           stderr=stderr, verbose=verbose)
        else:
            abs_deps = filter_requirements(file, abs_deps, full_provides | add_provides,
                                           only_top_module, ignore_list,
                                           stderr=stderr, verbose=verbose)

        rel_deps = filter_requirements(file, rel_deps, full_provides | add_provides,
                                       only_top_module=False, ignore_list=ignore_list,
                                       stderr=stderr, verbose=verbose)

        adv_deps = filter_requirements(file, adv_deps, full_provides | add_provides,
                                       only_top_module=False, ignore_list=ignore_list,
                                       stderr=stderr, verbose=verbose)

        filter_requirements(file, skip, skip_flag=True, stderr=stderr, verbose=verbose)

        if not inspect_env:
            dependencies[file] = abs_deps, rel_deps, adv_deps, set()
        else:
            tmp_dependencies |= abs_deps | rel_deps | adv_deps

    if inspect_env:
        for pkg_ver, provs in env_provides.items():
            if (matched := provs.intersection(tmp_dependencies)):
                tmp_dependencies.difference_update(matched)
                dependencies.add("==".join(pkg_ver))
                if verbose:
                    print(f"The following deps:{",".join(matched)} was satisfied by package:{"==".join(pkg_ver)}",
                          file=sys.stderr)
                if not tmp_dependencies:
                    break
        else:
            if verbose:
                print("WARNING! Dependencies not matched to any package"
                      f"in your environment:{",".join(tmp_dependencies)}",
                      file=sys.stderr)

    return dependencies


def main():
    description = 'Search for requiremnts for pyfile'
    args = argparse.ArgumentParser(description=description)
    args.add_argument('--add_prov_path', default="",
                      help='List of additional paths for provides (separated by ":")')
    args.add_argument('--prefixes',
                      help='Prefixes that will be removed from fully '
                      'qualified name for relative import (string separated by ":")')
    args.add_argument('--ignore_list', default="",
                      help='List of dependencies that should be ignored (separated by ":")')
    args.add_argument('--include_built-in', action="store_true",
                      help='Include built-in modules (like sys, time) to the dependencies list')
    args.add_argument('--read_prov_from_file',
                      default=None,
                      help='Read provides from file')
    args.add_argument('--exclude_hidden_deps', action='store_true',
                      help='Skip dependencies, that are used inside conditions')
    args.add_argument('--only_top_module', action='store_true',
                      help='For dependency like a.b skip b')
    args.add_argument('--include_stdlib', action='store_true',
                      help='Exclude dependencies that are provided by installed python3 standart library')
    args.add_argument("--inspect_env", action="store_true",
                      help="Inspect environment for installed packages and "
                      + "match required symbols to installed packages")
    args.add_argument("--env_path", default="",
                      help='Set path to the environment with installed packages (string separated by ":"). '
                      + "By default set to purelib and platlib")
    args.add_argument('--verbose', action='store_true',
                      help='Verbose stderr')
    args.add_argument('input', nargs='*',
                      help='List of files from which deps will be created', default=[])
    args = args.parse_args()

    if not args.input:
        args.input = shlex.split(sys.stdin.read())

    dirs = filter(lambda p: pathlib.Path(p).is_dir(), args.input)
    args.input += sum(map(lambda d: list(pathlib.Path(d).rglob("*")), dirs), start=[])
    args.input = list(map(lambda p: pathlib.Path(p).absolute().as_posix(), args.input))

    prefixes = args.prefixes.split(':') if args.prefixes else sys.path

    ignore_list = args.ignore_list.split(":")

    if not args.include_built_in:
        ignore_list += sys.builtin_module_names

    dependencies = generate_requirements(files=args.input, add_prov_path=args.add_prov_path.split(":"),
                                         ignore_list=ignore_list,
                                         read_prov_from_file=args.read_prov_from_file,
                                         skip_subs=True, prefixes=prefixes,
                                         only_external_deps=args.exclude_hidden_deps,
                                         only_top_module=args.only_top_module,
                                         exclude_stdlib=not args.include_stdlib,
                                         inspect_env=args.inspect_env, env_path=args.env_path.split(":"),
                                         verbose=args.verbose)

    if not args.inspect_env:
        for file, deps in dependencies.items():
            if any(deps) and args.verbose:
                print(f'{file}:{" ".join([" ".join(req) for req in deps if req])}')
            elif any(deps):
                print('\n'.join(['\n'.join(req) for req in deps if req]))
    else:
        try:
            with open("requirements.txt", "w") as w:
                print("\n".join(dependencies), file=w)
        except PermissionError:
            print("Failed to write requirements to requirements.txt due to permission error", file=sys.stderr)


if __name__ == '__main__':
    sys.exit(main())
